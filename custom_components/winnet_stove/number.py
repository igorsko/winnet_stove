# ============================================================================
# FILE: custom_components/winnet_stove/number.py
# Controllo numerico per potenza e ventilazione
# ============================================================================

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup number entities per potenza e ventilazione."""
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    coordinator = data["coordinator"]

    async_add_entities([
        WinetStufaPowerNumber(coordinator, api, entry),
        WinetStufaFanNumber(coordinator, api, entry),
    ])


class WinetStufaPowerNumber(CoordinatorEntity, NumberEntity):
    """Controllo numerico della potenza (registro 12, valori 1-5)."""

    _attr_native_min_value = 1
    _attr_native_max_value = 5
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:fire-circle"

    def __init__(self, coordinator, api, entry):
        super().__init__(coordinator)
        self._api = api
        self._attr_name = "Potenza"
        self._attr_unique_id = f"{entry.entry_id}_power_number"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }

    @property
    def native_value(self):
        if self.coordinator.data and "registers" in self.coordinator.data:
            return self._api.get_power(self.coordinator.data["registers"])
        return None

    async def async_set_native_value(self, value: float) -> None:
        await self._api.async_set_power(int(value))
        await self.coordinator.async_request_refresh()


class WinetStufaFanNumber(CoordinatorEntity, NumberEntity):
    """Controllo numerico della ventilazione (registro 13, valori 0-5).
    0 = automatico, 1-5 = velocità manuale.
    """

    _attr_native_min_value = 0
    _attr_native_max_value = 5
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_icon = "mdi:fan"

    def __init__(self, coordinator, api, entry):
        super().__init__(coordinator)
        self._api = api
        self._attr_name = "Ventilazione"
        self._attr_unique_id = f"{entry.entry_id}_fan_number"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }

    @property
    def native_value(self):
        if self.coordinator.data and "registers" in self.coordinator.data:
            return self._api.get_fan_speed(self.coordinator.data["registers"])
        return None

    async def async_set_native_value(self, value: float) -> None:
        await self._api.async_set_fan_speed(int(value))
        await self.coordinator.async_request_refresh()
