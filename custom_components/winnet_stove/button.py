# SPDX-License-Identifier: GPL-3.0-only
"""Manually log a bag of pellet loaded into the stove."""

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Register the per-device log action."""
    usage = hass.data[DOMAIN][entry.entry_id]["usage"]
    async_add_entities([StoveBagLoadedButton(usage, entry)])


class StoveBagLoadedButton(ButtonEntity):
    """Track physical pellet loading; does not send a stove command."""

    _attr_has_entity_name = True
    _attr_name = "Log one pellet bag loaded"
    _attr_icon = "mdi:plus-circle-outline"

    def __init__(self, usage, entry):
        self._usage = usage
        self._attr_unique_id = f"{entry.entry_id}_pellet_action_load_bag"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}

    async def async_press(self) -> None:
        """Record one bag in Home Assistant's local storage."""
        await self._usage.async_record_bag_loaded()
