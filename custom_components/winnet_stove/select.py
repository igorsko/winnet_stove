# SPDX-License-Identifier: GPL-3.0-only
"""Capture-limited local controls, separate from read-only stove sensors."""

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .controls import FAN_REGISTER, POWER_REGISTER, encode_level


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        WinetPilotLevel(data["coordinator"], data["api"], entry, "power"),
        WinetPilotLevel(data["coordinator"], data["api"], entry, "fan"),
    ])


class WinetPilotLevel(CoordinatorEntity, SelectEntity):
    """Only expose the two levels positively captured on this controller."""

    _attr_has_entity_name = True
    _attr_options = ["1", "2"]

    def __init__(self, coordinator, api, entry, kind):
        super().__init__(coordinator)
        self._api = api
        self._kind = kind
        self._register = POWER_REGISTER if kind == "power" else FAN_REGISTER
        self._attr_name = "Pilot power level" if kind == "power" else "Pilot air fan level"
        self._attr_unique_id = f"{entry.entry_id}_pilot_{kind}"
        self._attr_icon = "mdi:fire" if kind == "power" else "mdi:fan"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}

    @property
    def available(self):
        return super().available and self.coordinator.data is not None and (
            self._register in self.coordinator.data.get("registers", {})
        )

    @property
    def current_option(self):
        if not self.available:
            return None
        level = self.coordinator.data["registers"].get(self._register)
        return str(level) if level in (1, 2) else None

    async def async_select_option(self, option: str) -> None:
        try:
            level = encode_level(option)
        except ValueError as err:
            raise HomeAssistantError("Unsupported pilot control level") from err
        if not self.available:
            raise HomeAssistantError("WiNET controller unavailable")
        success = (
            await self._api.async_set_power_level(level)
            if self._kind == "power"
            else await self._api.async_set_room_fan_level(level)
        )
        if not success:
            raise HomeAssistantError("WiNET stove rejected pilot level change")
        await self.coordinator.async_request_refresh()
