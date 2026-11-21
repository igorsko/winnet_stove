# SPDX-License-Identifier: GPL-3.0-only
"""Persisted accounting for WiNET Stove."""

import logging
from datetime import datetime, timezone
from time import monotonic

from homeassistant.core import callback
from homeassistant.helpers.storage import Store

from .const import DOMAIN
from .usage_logic import UsageTracker

_LOGGER = logging.getLogger(__name__)


class StoveUsage:
    """Per-device usage counters backed by Home Assistant storage."""

    def __init__(self, hass, entry_id: str, scan_interval: int):
        self.tracker = UsageTracker()
        self._store = Store(hass, 1, f"{DOMAIN}_{entry_id}_usage")
        self._max_gap = 2 * scan_interval + 10
        self._subscribers = set()

    async def async_load(self):
        """Restore totals without assuming an ongoing prior session."""
        data = await self._store.async_load() or {}
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
            return
        state = coordinator.data.get("registers", {}).get(6)
        if not isinstance(state, int):
            self.tracker.interrupt()
            return
        changed = self.tracker.observe(
            state & 0xFF, monotonic(), datetime.now(timezone.utc), self._max_gap
        )
        if changed:
            self._store.async_delay_save(self._snapshot, 60)
            for listener in tuple(self._subscribers):
                listener()

    async def async_close(self):
        """Flush totals before integration unload."""
        await self._store.async_save(self._snapshot())
