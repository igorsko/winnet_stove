# SPDX-License-Identifier: GPL-3.0-only
"""Persisted accounting for WiNET Stove."""

import logging
from uuid import uuid4
from datetime import datetime, timezone
from time import monotonic

from homeassistant.core import callback
from homeassistant.helpers.storage import Store

from .const import DOMAIN
from .usage_logic import UsageTracker
from .pellet_logic import pellet_stats, validate_setting
from .auto_refill import AutoRefillDetector
from .refill_log import ledger_stats, remove_event, update_event, valid_kg, validate_events
from .insights_logic import (MAINTENANCE_DEFAULTS, calibrated_rate, daily_estimates,
                             effective_rate, maintenance_remaining, valid_positive,
                             profile_consumption, learned_power_profile)
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


class StoveUsage:
    """Per-device usage counters backed by Home Assistant storage."""

    def __init__(self, hass, entry_id: str, scan_interval: int):
        self.tracker = UsageTracker()
        self._entry_id = entry_id
        self._store = Store(hass, 1, f"{DOMAIN}_{entry_id}_usage")
        self._max_gap = 2 * scan_interval + 10
        self._subscribers = set()
        self.last_success_at = None
        self.communication_failures = 0
        self.consecutive_failures = 0
        self.refills = []
        self._legacy_bags = 0
        self.working_by_day = {}
        self.working_by_day_power = {}
        self.power_rates = {str(i): 0.0 for i in range(1, 6)}
        self.working_by_power = {}
        self.maintenance_baselines = {key: 0.0 for key in MAINTENANCE_DEFAULTS}
        self.maintenance_thresholds = dict(MAINTENANCE_DEFAULTS)
        self.price_per_bag = 0.0
        self._previous_working_power = None
        self._last_maintenance_notification = {}
        self._legacy_auto_bags = 0
        self._hass = hass
        self._auto_detector = AutoRefillDetector()
        self.auto_refill_enabled = False
        self.auto_bags_loaded = 0
        self.last_auto_refill = None
        self._legacy_last_auto_refill = None
        self.pellet = {
            'initial_hours': 0.0,
            'bag_weight_kg': 15.0,
            'rate_kg_h': 0.0,
            'bags_in_stock': 0,
            'bags_loaded': 0,
        }

    async def async_load(self):
        """Restore totals without assuming an ongoing prior session."""
        data = await self._store.async_load() or {}
        try:
            stamp = data.get("last_success_at")
            if stamp:
                parsed = datetime.fromisoformat(stamp)
                if parsed.tzinfo:
                    self.last_success_at = parsed
            self.communication_failures = max(
                0, int(data.get("communication_failures", 0))
            )
        except (TypeError, ValueError):
            _LOGGER.warning("Invalid WiNET diagnostics persisted data")
        self.auto_refill_enabled = data.get('auto_refill_enabled') is True
        self._auto_detector = AutoRefillDetector.restore(data.get('auto_refill_detector'))
        try:
            self.auto_bags_loaded = max(0, int(data.get('auto_bags_loaded', 0)))
            self.last_auto_refill = data.get('last_auto_refill')
        except (TypeError, ValueError):
            _LOGGER.warning('Invalid stored auto-refill metadata; resetting it')
            self.auto_bags_loaded = 0
            self.last_auto_refill = None
        self.refills = validate_events(data.get('refills', []))
        for name, value in data.get("power_rates", {}).items():
            if name in self.power_rates:
                try:
                    rate = float(value)
                    if 0 <= rate <= 20:
                        self.power_rates[name] = rate
                except (TypeError, ValueError):
                    pass
        for key, value in data.get("working_by_day", {}).items():
            if isinstance(key, str) and isinstance(value, (int, float)) and 0 <= value < 1e12:
                self.working_by_day[key] = value
        for day, breakdown in data.get("working_by_day_power", {}).items():
            if isinstance(day, str) and isinstance(breakdown, dict):
                self.working_by_day_power[day] = {
                    key: seconds for key, seconds in breakdown.items()
                    if isinstance(key, str) and isinstance(seconds, (int, float))
                    and 0 <= seconds < 1e10
                }
        for key, value in data.get("working_by_power", {}).items():
            if isinstance(key, str) and isinstance(value, (int, float)) and 0 <= value < 1e12:
                self.working_by_power[key] = value
        for key in MAINTENANCE_DEFAULTS:
            try:
                self.maintenance_baselines[key] = max(
                    0.0, float(data.get("maintenance_baselines", {}).get(key, 0.0))
                )
                self.maintenance_thresholds[key] = valid_positive(
                    data.get("maintenance_thresholds", {}).get(key, MAINTENANCE_DEFAULTS[key])
                )
            except (ValueError, TypeError):
                _LOGGER.warning("Invalid maintenance setting for %s", key)
        try:
            raw_price = float(data.get("price_per_bag", 0))
            if 0 <= raw_price <= 1000:
                self.price_per_bag = raw_price
        except (TypeError, ValueError):
            pass
        self._last_maintenance_notification = data.get("maintenance_notifications", {})
        if not isinstance(self._last_maintenance_notification, dict):
            self._last_maintenance_notification = {}
        self._legacy_last_auto_refill = data.get(
            "legacy_last_auto_refill", self.last_auto_refill
        )
        for name in self.pellet:
            if name in data:
                try:
                    self.pellet[name] = validate_setting(name, data[name])
                except (ValueError, TypeError):
                    _LOGGER.warning('Ignoring invalid stored WiNET pellet setting: %s', name)
        # Preserve legacy bag counts, whose dates and weights were not stored.
        self._legacy_bags = max(
            0, int(data.get("legacy_bags", self.pellet["bags_loaded"]))
        )
        self._legacy_auto_bags = max(
            0, int(data.get("legacy_auto_bags", self.auto_bags_loaded))
        )
        self._recount_refills()
        try:
            self.tracker.operating_seconds = max(
                0.0, float(data.get("operating_seconds", 0))
            )
            if "maintenance_baselines" not in data:
                for key in MAINTENANCE_DEFAULTS:
                    self.maintenance_baselines[key] = self.tracker.operating_seconds / 3600
            timestamp = data.get("last_ignition")
            if timestamp:
                parsed = datetime.fromisoformat(timestamp)
                if parsed.tzinfo is not None:
                    self.tracker.last_ignition = parsed
        except (TypeError, ValueError):
            _LOGGER.warning("Invalid stored WiNET Stove usage; resetting counters")

    async def async_recover_history(self):
        """Recover missing legacy snapshots without changing refill quantities."""
        if not any(e.get("full_hopper") and e.get("power_seconds") is None
                   for e in self.refills):
            return
        from .recorder_recovery import async_recover_refills
        try:
            recovered = await async_recover_refills(
                self._hass, self._entry_id, self.refills, self._max_gap
            )
            if not recovered:
                return
            # Preserve original persisted accounting before changing any event.
            backup = Store(self._hass, 1, f"{DOMAIN}_{self._entry_id}_pre_recorder_recovery")
            if await backup.async_load() is None:
                await backup.async_save(await self._store.async_load() or self._snapshot())
            original = self.refills
            self.refills = [
                {**event, "power_seconds": recovered[event["id"]],
                 "power_snapshot_source": "recorder"}
                if event["id"] in recovered and event.get("power_seconds") is None
                else event for event in original
            ]
            try:
                await self._store.async_save(self._snapshot())
            except Exception:
                self.refills = original
                raise
            _LOGGER.info("Recovered %s WiNET refill power snapshots from Recorder",
                         len(recovered))
        except Exception:
            _LOGGER.exception("Optional WiNET Recorder recovery failed; using existing data")

    def _snapshot(self):
        return {
            **self.pellet,
            "refills": self.refills,
            "working_by_day": self.working_by_day,
            "power_rates": self.power_rates,
            "working_by_power": self.working_by_power,
            "working_by_day_power": self.working_by_day_power,
            "maintenance_baselines": self.maintenance_baselines,
            "maintenance_thresholds": self.maintenance_thresholds,
            "maintenance_notifications": self._last_maintenance_notification,
            "price_per_bag": self.price_per_bag,
            "legacy_bags": self._legacy_bags,
            "legacy_auto_bags": self._legacy_auto_bags,
            "legacy_last_auto_refill": self._legacy_last_auto_refill,
            "auto_refill_enabled": self.auto_refill_enabled,
            "auto_refill_detector": self._auto_detector.snapshot(),
            "auto_bags_loaded": self.auto_bags_loaded,
            "last_auto_refill": self.last_auto_refill,
            "operating_seconds": self.tracker.operating_seconds,
            "last_success_at": self.last_success_at.isoformat() if self.last_success_at else None,
            "communication_failures": self.communication_failures,
            "last_ignition": self.tracker.last_ignition.isoformat()
            if self.tracker.last_ignition
            else None,
        }

    @callback
    def async_subscribe(self, listener):
        """Subscribe to local state changes."""
        self._subscribers.add(listener)
        return lambda: self._subscribers.discard(listener)

    @callback
    def async_update(self, coordinator):
        """Observe a coordinator result, excluding unavailable samples."""
        if not coordinator.last_update_success or not coordinator.data:
            self.communication_failures += 1
            self.consecutive_failures += 1
            self._store.async_delay_save(self._snapshot, 60)
            self._notify()
            self.tracker.interrupt()
            self._previous_working_power = None
            self._auto_detector.observe(None, None)
            return
        state = coordinator.data.get("registers", {}).get(6)
        if not isinstance(state, int):
            self.communication_failures += 1
            self.consecutive_failures += 1
            self._store.async_delay_save(self._snapshot, 60)
            self._notify()
            self.tracker.interrupt()
            self._auto_detector.observe(None, None)
            return
        recovered = self.consecutive_failures > 0
        self.consecutive_failures = 0
        self.last_success_at = datetime.now(timezone.utc)
        previous_operating = self.tracker.operating_seconds
        changed = self.tracker.observe(
            state & 0xFF, monotonic(), datetime.now(timezone.utc), self._max_gap
        )
        registers = coordinator.data.get("registers", {})
        if self.auto_refill_enabled:
            # Both alarm registers must be present: missing is not "cleared".
            alarm_code = (
                (registers[9] << 16) | registers[8]
                if isinstance(registers.get(8), int)
                and isinstance(registers.get(9), int)
                else None
            )
            observed, refill = self._auto_detector.observe(
                state & 0xFF, alarm_code
            )
            changed = changed or observed
            if refill:
                # Store the inferred event and detector state in the same
                # snapshot; the UI can later correct an inaccurate inference.
                self._append_refill(self.pellet["bag_weight_kg"], "auto")
                self.last_auto_refill = datetime.now(timezone.utc).isoformat()
                _LOGGER.info(
                    "Inferred one pellet bag after alarm and confirmed restart. "
                    "Alarm bit 0 may also mean CLEAN BURNER."
                )
                # Save the counter and consumed alarm together to prevent
                # repeated counting after restart.
                self._hass.async_create_task(
                    self._store.async_save(self._snapshot())
                )
                changed = True
        # Accounting uses only consecutive observations of state 3. The
        # existing tracker rejects offline gaps and invalid state mappings.
        elapsed = self.tracker.operating_seconds - previous_operating
        if elapsed > 0:
            today = dt_util.as_local(datetime.now(timezone.utc)).date().isoformat()
            self.working_by_day[today] = self.working_by_day.get(today, 0) + elapsed
            if len(self.working_by_day) > 400:
                for day in sorted(self.working_by_day)[:-400]:
                    del self.working_by_day[day]
                    self.working_by_day_power.pop(day, None)
            # Label with the previously observed power; never infer power
            # during a disconnected period.
            power = self._previous_working_power
            if power is not None:
                key = str(power)
                self.working_by_power[key] = self.working_by_power.get(key, 0) + elapsed
                by_day = self.working_by_day_power.setdefault(today, {})
                by_day[key] = by_day.get(key, 0) + elapsed
            changed = True
            self._notify_maintenance()
        self._previous_working_power = registers.get(12) if state & 0xFF == 3 else None
        if changed or recovered:
            self._store.async_delay_save(self._snapshot, 60)
            for listener in tuple(self._subscribers):
                listener()
        else:
            # Refresh the connection-health entity without storing every poll.
            self._notify()

    def pellet_statistics(self):
        """Derived estimates, with explicit provenance of the kg/h rate."""
        stats = pellet_stats(self.tracker.operating_seconds, self.pellet)
        rate, source = effective_rate(self.pellet["rate_kg_h"], self.refills)
        learned = learned_power_profile(self.refills)
        # A complete user-defined profile takes precedence, preserving existing
        # behavior. In its absence, use learned per-power rates when every
        # observed power level is identifiable from independent refill cycles.
        profile_rates = self.power_rates
        profile_source = "configured_power_profile"
        all_power_seconds = sum(self.working_by_power.values())
        profile_kg = profile_consumption(self.working_by_power, profile_rates)
        if profile_kg is None and learned["status"] == "learned":
            profile_rates = learned["rates"]
            profile_source = "learned_power_profile"
            profile_kg = profile_consumption(self.working_by_power, profile_rates)
        # Never treat a partly observed power distribution as complete.
        if all_power_seconds < self.tracker.operating_seconds * 0.98:
            profile_kg = None
        if profile_kg is not None and self.tracker.operating_seconds > 0:
            rate = profile_kg / (self.tracker.operating_seconds / 3600)
            source = profile_source
        learned["recovered_snapshots"] = sum(
            e.get("power_snapshot_source") == "recorder" for e in self.refills
        )
        stats["calibration"] = learned
        stats["profile_rates"] = profile_rates if profile_kg is not None else {}
        stats["rate_source"] = source
        stats["effective_rate_kg_h"] = round(rate, 4) if rate is not None else None
        if rate is not None:
            hours = self.tracker.operating_seconds / 3600
            weight = self.pellet["bag_weight_kg"]
            stats.update(
                pellet_used=profile_kg if profile_kg is not None else round(hours * rate, 3),
                estimated_bags=round(hours * rate / weight, 3),
                bags_per_hour=round(rate / weight, 4),
                hours_per_bag=round(weight / rate, 2),
            )
        stats["price_per_bag"] = self.price_per_bag
        stats["cost_per_hour"] = (
            round(rate / self.pellet["bag_weight_kg"] * self.price_per_bag, 3)
            if rate is not None and self.price_per_bag > 0 else None
        )
        return stats

    def daily_statistics(self):
        """Local-day working hours, power-aware estimates where calibrated."""
        stats = self.pellet_statistics()
        rate = stats["effective_rate_kg_h"]
        source = stats["rate_source"]
        days = daily_estimates(self.working_by_day, rate,
                               self.pellet["bag_weight_kg"], self.price_per_bag)
        if source in ("configured_power_profile", "learned_power_profile"):
            for day in days:
                power = self.working_by_day_power.get(day["date"], {})
                estimated = profile_consumption(power, stats["profile_rates"])
                if sum(power.values()) < self.working_by_day.get(day["date"], 0) * 0.98:
                    estimated = None
                day["estimated_kg"] = estimated
                day["estimated_cost"] = (
                    round(estimated / self.pellet["bag_weight_kg"]
                          * self.price_per_bag, 2)
                    if estimated is not None and self.price_per_bag > 0 else None
                )
        return {
            "days": days, "rate_source": source, "rate_kg_h": rate,
            "calibration": stats["calibration"],
            "power_hours": {key: round(seconds / 3600, 2)
                            for key, seconds in self.working_by_power.items()},
        }

    def maintenance_statistics(self):
        hours = self.tracker.operating_seconds / 3600
        return {
            key: {
                "remaining_hours": maintenance_remaining(
                    hours, self.maintenance_baselines[key], self.maintenance_thresholds[key]
                ),
                "interval_hours": self.maintenance_thresholds[key],
                "since_reset_hours": round(max(0, hours - self.maintenance_baselines[key]), 2),
            }
            for key in MAINTENANCE_DEFAULTS
        }

    def _notify_maintenance(self):
        """One persistent HA notification per maintenance cycle."""
        from homeassistant.components import persistent_notification
        for key, data in self.maintenance_statistics().items():
            token = str(self.maintenance_baselines[key])
            if data["remaining_hours"] <= 0 and self._last_maintenance_notification.get(key) != token:
                persistent_notification.async_create(
                    self._hass,
                    f"WiNET Stove: {key.replace('_', ' ')} due after "
                    f"{data['since_reset_hours']:.1f} hours.",
                    title="WiNET Stove · Maintenance",
                    notification_id=f"winnet_stove_{self._entry_id}_{key}",
                )
                self._last_maintenance_notification[key] = token

    async def async_reset_maintenance(self, kind):
        """User confirms completed work; hardware remains untouched."""
        if kind not in MAINTENANCE_DEFAULTS:
            raise ValueError("Unknown maintenance kind")
        self.maintenance_baselines[kind] = self.tracker.operating_seconds / 3600
        self._last_maintenance_notification.pop(kind, None)
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_reset_legacy_bags(self):
        """One-time correction, preserving detailed refill event history."""
        self._legacy_bags = 0
        self._legacy_auto_bags = 0
        self._legacy_last_auto_refill = None
        self._recount_refills()
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_set_power_rate(self, level, value):
        """Rate for a raw reported controller power level, not an assumed P number."""
        if level not in self.power_rates:
            raise ValueError("Unknown reported power level")
        rate = float(value)
        if not __import__("math").isfinite(rate) or not 0 <= rate <= 20:
            raise ValueError("Invalid rate")
        self.power_rates[level] = rate
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_set_price(self, value):
        """Update bag price for estimated expenses; 0 means unknown."""
        price = float(value)
        if price < 0 or price > 1000 or not __import__("math").isfinite(price):
            raise ValueError("Invalid bag price")
        self.price_per_bag = price
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_set_threshold(self, kind, value):
        if kind not in MAINTENANCE_DEFAULTS:
            raise ValueError("Unknown maintenance kind")
        self.maintenance_thresholds[kind] = valid_positive(value)
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_set_pellet(self, name, value):
        """Apply a user-supplied value, store it, and notify entities."""
        value = validate_setting(name, value)
        self.pellet[name] = value
        await self._store.async_save(self._snapshot())
        for listener in tuple(self._subscribers):
            listener()

    def _recount_refills(self):
        """Keep legacy bag counts and new editable refill events separate."""
        full_bags = sum(
            abs(event["kg"] - event["bag_weight_kg"]) < 0.001
            for event in self.refills
        )
        self.pellet["bags_loaded"] = self._legacy_bags + full_bags
        self.auto_bags_loaded = (
            self._legacy_auto_bags
            + sum(event["source"] == "auto" for event in self.refills)
        )
        last_auto = next(
            (e["at"] for e in reversed(self.refills) if e["source"] == "auto"),
            None,
        )
        self.last_auto_refill = last_auto or self._legacy_last_auto_refill

    def refill_statistics(self):
        """Accessible to the frontend via the refill log entity."""
        return ledger_stats(self.refills)

    def _append_refill(self, kg, source):
        """Record a timestamped, editable refill without any stove writes."""
        kg = valid_kg(kg)
        entry = {
            "id": str(uuid4()),
            "runtime_h": round(self.tracker.operating_seconds / 3600, 6),
            # A snapshot is essential: past cumulative power totals cannot
            # be reconstructed at previously saved refills.
            "power_seconds": {str(level): self.working_by_power.get(str(level), 0)
                              for level in range(1, 6)},
            "full_hopper": False,
            "at": datetime.now(timezone.utc).isoformat(),
            "kg": kg,
            "bag_weight_kg": self.pellet["bag_weight_kg"],
            "source": source,
            "stock_debit": False,
        }
        if len(self.refills) >= 5000:
            raise ValueError("Refill history is full")
        # Only one full bag can debit whole-bag stock. A partial refill
        # has no reliable whole-bag stock impact.
        if abs(kg - self.pellet["bag_weight_kg"]) < 0.001 and self.pellet["bags_in_stock"] > 0:
            self.pellet["bags_in_stock"] -= 1
            entry["stock_debit"] = True
        self.refills.append(entry)
        self._recount_refills()
        return entry

    async def async_record_refill(self, kg, full_hopper=False):
        """Add manual pellet in kilograms and immediately persist the ledger."""
        event = self._append_refill(kg, "manual")
        event["full_hopper"] = full_hopper is True
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_edit_refill(self, event_id, kg, full_hopper=None):
        """Correct a recorded quantity, including false automatic inferences."""
        event = next((e for e in self.refills if e["id"] == event_id), None)
        if event is None:
            raise ValueError("Refill event not found")
        valid = valid_kg(kg)
        # Reconcile the recorded stock debit on a corrected full-bag event.
        if event.get("stock_debit"):
            self.pellet["bags_in_stock"] += 1
        self.refills = update_event(self.refills, event_id, valid)
        corrected = next(e for e in self.refills if e["id"] == event_id)
        corrected["stock_debit"] = False
        if full_hopper is not None:
            corrected["full_hopper"] = full_hopper is True
        if (
            abs(corrected["kg"] - corrected["bag_weight_kg"]) < 0.001
            and self.pellet["bags_in_stock"] > 0
        ):
            self.pellet["bags_in_stock"] -= 1
            corrected["stock_debit"] = True
        self._recount_refills()
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_remove_refill(self, event_id):
        """Remove an incorrect event and restore its full-bag stock debit."""
        event = next((e for e in self.refills if e["id"] == event_id), None)
        if event is None:
            raise ValueError("Refill event not found")
        self.refills = remove_event(self.refills, event_id)
        if event.get("stock_debit"):
            self.pellet["bags_in_stock"] += 1
        self._recount_refills()
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_record_bag_loaded(self):
        """Preserve the existing HA button as an automation-compatible alias."""
        await self.async_record_refill(self.pellet["bag_weight_kg"])

    def _notify(self):
        for listener in tuple(self._subscribers):
            listener()

    async def async_set_auto_refill(self, enabled: bool):
        """Explicitly opt in or out and reset candidate alarm state."""
        enabled = bool(enabled)
        if self.auto_refill_enabled == enabled:
            return
        self.auto_refill_enabled = enabled
        self._auto_detector.reset()
        await self._store.async_save(self._snapshot())
        for listener in tuple(self._subscribers):
            listener()

    async def async_close(self):
        """Flush totals before integration unload."""
        await self._store.async_save(self._snapshot())
