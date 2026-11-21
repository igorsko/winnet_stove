# SPDX-License-Identifier: GPL-3.0-only
"""WiNET Stove integration."""

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import WinetStufaAPI
from .usage import StoveUsage
from .ui import async_update_ui
from .const import DOMAIN, CONF_HOST, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.CLIMATE, Platform.SENSOR, Platform.SWITCH, Platform.BINARY_SENSOR, Platform.NUMBER, Platform.BUTTON]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WiNET Stove."""
    host = entry.data[CONF_HOST]
    interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    api = WinetStufaAPI(host)

    async def async_update_data():
        try:
            return await api.async_get_data()
        except Exception as err:
            raise UpdateFailed(f"Unable to read WiNET stove: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="winnet_stove_data",
        update_method=async_update_data,
        update_interval=timedelta(seconds=interval),
    )
    try:
        await coordinator.async_config_entry_first_refresh()
        usage = StoveUsage(hass, entry.entry_id, interval)
        await usage.async_load()
        unsubscribe = coordinator.async_add_listener(lambda: usage.async_update(coordinator))
        usage.async_update(coordinator)
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
            "api": api,
            "coordinator": coordinator,
            "scan_interval": interval,
            "usage": usage,
            "usage_unsubscribe": unsubscribe,
        }
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        try:
            await async_update_ui(hass)
        except Exception:
            _LOGGER.exception('Unable to configure optional WiNET user interface')
    except Exception:
        data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if data:
            data['usage_unsubscribe']()
            await data['usage'].async_close()
        await api.async_close()
        raise
    entry.async_on_unload(entry.add_update_listener(async_update_options))
    return True


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload when polling settings change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the integration and close its HTTP client."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        data = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
        if data:
            data["usage_unsubscribe"]()
            await data["usage"].async_close()
            await data["api"].async_close()
        try:
            await async_update_ui(hass)
        except Exception:
            _LOGGER.exception("Unable to hide WiNET user interface after unload")
    return unloaded
