# SPDX-License-Identifier: GPL-3.0-only
"""Binary stove state entities, with native Home Assistant history."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .usage_logic import ACTIVE_STATES


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Register state binaries on the existing coordinator."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([
        StoveStateBinary(coordinator, entry, "active"),
        StoveStateBinary(coordinator, entry, "burning"),
    ])


class StoveStateBinary(CoordinatorEntity, BinarySensorEntity):
    """Active cycle versus confirmed working/combustion state."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, kind):
        super().__init__(coordinator)
        self._kind = kind
        self._attr_unique_id = f"{entry.entry_id}_{kind}"
        self._attr_name = "Stove active" if kind == "active" else "Stove burning"
        self._attr_icon = "mdi:fire" if kind == "burning" else "mdi:power"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}

    @property
    def is_on(self):
        if not self.coordinator.last_update_success or not self.coordinator.data:
            return None
        value = self.coordinator.data.get("registers", {}).get(6)
        if not isinstance(value, int) or (value & 0xFF) == 0:
            return None
        state = value & 0xFF
        if state not in ACTIVE_STATES | {1, 6, 7}:
            return None
        return (state in ACTIVE_STATES) if self._kind == "active" else (state == 3)
