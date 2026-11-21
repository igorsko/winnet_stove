# SPDX-License-Identifier: GPL-3.0-only
"""Editable, locally persisted pellet accounting values."""

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .pellet_logic import LIMITS


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add user-configurable values; none control the physical stove."""
    usage = hass.data[DOMAIN][entry.entry_id]["usage"]
    async_add_entities([
        StovePelletNumber(usage, entry, kind)
        for kind in ("initial_hours", "bag_weight_kg", "rate_kg_h", "bags_in_stock")
    ])


class StovePelletNumber(NumberEntity):
    """An editable pellet setting backed by per-device Home Assistant storage."""

    _attr_has_entity_name = True
    _attr_mode = NumberMode.BOX

    def __init__(self, usage, entry, kind):
        self._usage = usage
        self._kind = kind
        self._attr_unique_id = f"{entry.entry_id}_pellet_setting_{kind}"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}
        minimum, maximum = LIMITS[kind]
        self._attr_native_min_value = minimum
        self._attr_native_max_value = maximum
        if kind == "initial_hours":
            self._attr_name = "Initial stove operating hours"
            self._attr_native_unit_of_measurement = "h"
            self._attr_native_step = 1
            self._attr_icon = "mdi:clock-edit-outline"
        elif kind == "bag_weight_kg":
            self._attr_name = "Pellet bag weight"
            self._attr_native_unit_of_measurement = "kg"
            self._attr_native_step = 0.5
            self._attr_icon = "mdi:weight-kilogram"
        elif kind == "rate_kg_h":
            self._attr_name = "Estimated pellet consumption rate"
            self._attr_native_unit_of_measurement = "kg/h"
            self._attr_native_step = 0.1
            self._attr_icon = "mdi:fire"
        else:
            self._attr_name = "Pellet bags in stock"
            self._attr_native_step = 1
            self._attr_icon = "mdi:package-variant"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(self._usage.async_subscribe(self.async_write_ha_state))

    @property
    def native_value(self):
        return self._usage.pellet[self._kind]

    async def async_set_native_value(self, value: float) -> None:
        """Persist a change without contacting the stove."""
        await self._usage.async_set_pellet(self._kind, value)
