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

_LOGGER = logging.getLogger(__name__)


class StoveUsage:
    """Per-device usage counters backed by Home Assistant storage."""

    def __init__(self, hass, entry_id: str, scan_interval: int):
        self.tracker = UsageTracker()
        self._store = Store(hass, 1, f"{DOMAIN}_{entry_id}_usage")
        self._max_gap = 2 * scan_interval + 10
        self._subscribers = set()
        self.refills = []
        self._legacy_bags = 0
        self._legacy_auto_bags = 0
        self._hass = hass
        self._auto_detector = AutoRefillDetector()
        self.auto_refill_enabled = False
        self.auto_bags_loaded = 0
        self.last_auto_refill = None
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
            timestamp = data.get("last_ignition")
            if timestamp:
                parsed = datetime.fromisoformat(timestamp)
                if parsed.tzinfo is not None:
                    self.tracker.last_ignition = parsed
        except (TypeError, ValueError):
            _LOGGER.warning("Invalid stored WiNET Stove usage; resetting counters")

    def _snapshot(self):
        return {
            **self.pellet,
            "refills": self.refills,
            "legacy_bags": self._legacy_bags,
            "legacy_auto_bags": self._legacy_auto_bags,
            "auto_refill_enabled": self.auto_refill_enabled,
            "auto_refill_detector": self._auto_detector.snapshot(),
            "auto_bags_loaded": self.auto_bags_loaded,
            "last_auto_refill": self.last_auto_refill,
            "operating_seconds": self.tracker.operating_seconds,
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
            self.tracker.interrupt()
            self._auto_detector.observe(None, None)
            return
        state = coordinator.data.get("registers", {}).get(6)
        if not isinstance(state, int):
            self.tracker.interrupt()
            self._auto_detector.observe(None, None)
            return
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
        if changed:
            self._store.async_delay_save(self._snapshot, 60)
            for listener in tuple(self._subscribers):
                listener()

    def pellet_statistics(self):
        """Derived estimates; never claim actual measured pellet mass."""
        return pellet_stats(self.tracker.operating_seconds, self.pellet)

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
            event["source"] == "auto" or
            abs(event["kg"] - event["bag_weight_kg"]) < 0.001
            for event in self.refills
        )
        self.pellet["bags_loaded"] = self._legacy_bags + full_bags
        self.auto_bags_loaded = (
            self._legacy_auto_bags
            + sum(event["source"] == "auto" for event in self.refills)
        )

    def refill_statistics(self):
        """Accessible to the frontend via the refill log entity."""
        return ledger_stats(self.refills)

    def _append_refill(self, kg, source):
        """Record a timestamped, editable refill without any stove writes."""
        kg = valid_kg(kg)
        entry = {
            "id": str(uuid4()),
            "at": datetime.now(timezone.utc).isoformat(),
            "kg": kg,
            "bag_weight_kg": self.pellet["bag_weight_kg"],
            "source": source,
            "stock_debit": False,
        }
        # Only one full bag can debit whole-bag stock. A partial refill
        # has no reliable whole-bag stock impact.
        if abs(kg - self.pellet["bag_weight_kg"]) < 0.001 and self.pellet["bags_in_stock"] > 0:
            self.pellet["bags_in_stock"] -= 1
            entry["stock_debit"] = True
        if len(self.refills) >= 5000:
            raise ValueError('Refill history is full; export it before adding more')
        self.refills.append(entry)
        self._recount_refills()
        return entry

    async def async_record_refill(self, kg):
        """Add manual pellet in kilograms and immediately persist the ledger."""
        self._append_refill(kg, "manual")
        await self._store.async_save(self._snapshot())
        self._notify()

    async def async_edit_refill(self, event_id, kg):
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
