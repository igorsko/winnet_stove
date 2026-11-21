# SPDX-License-Identifier: GPL-3.0-only
"""Persisted accounting for WiNET Stove."""

import logging
from datetime import datetime, timezone
from time import monotonic

from homeassistant.core import callback
from homeassistant.helpers.storage import Store

from .const import DOMAIN
from .usage_logic import UsageTracker
from .pellet_logic import pellet_stats, validate_setting
from .auto_refill import AutoRefillDetector

_LOGGER = logging.getLogger(__name__)


class StoveUsage:
    """Per-device usage counters backed by Home Assistant storage."""

    def __init__(self, hass, entry_id: str, scan_interval: int):
        self.tracker = UsageTracker()
        self._store = Store(hass, 1, f"{DOMAIN}_{entry_id}_usage")
        self._max_gap = 2 * scan_interval + 10
        self._subscribers = set()
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
        for name in self.pellet:
            if name in data:
                try:
                    self.pellet[name] = validate_setting(name, data[name])
                except (ValueError, TypeError):
                    _LOGGER.warning('Ignoring invalid stored WiNET pellet setting: %s', name)
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
                self.pellet["bags_loaded"] += 1
                self.pellet["bags_in_stock"] = max(
                    0, self.pellet["bags_in_stock"] - 1
                )
                self.auto_bags_loaded += 1
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

    async def async_record_bag_loaded(self):
        """Record one physical bag; stock never becomes negative."""
        self.pellet["bags_loaded"] += 1
        self.pellet["bags_in_stock"] = max(0, self.pellet["bags_in_stock"] - 1)
        await self._store.async_save(self._snapshot())
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
