# ============================================================================
# FILE: custom_components/winet_stufa/__init__.py
# ============================================================================

import asyncio
import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, CONF_HOST, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .api import WinetStufaAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CLIMATE, Platform.SENSOR, Platform.SWITCH]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura l'integrazione da config entry."""
    host = entry.data[CONF_HOST]
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    
    _LOGGER.info(f"Setup WiNET Stufa - Host: {host}, Scan: {scan_interval}s")
    
    # Crea l'API
    api = WinetStufaAPI(host)
    
    # Testa la connessione
    if not await api.async_test_connection():
        _LOGGER.error("Impossibile connettersi alla stufa su %s", host)
        return False
    
    _LOGGER.info("Connessione alla stufa riuscita")
    
    # Crea il coordinator QUI - prima di caricare le piattaforme
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="winet_stufa_data",
        update_method=api.async_get_data,
        update_interval=timedelta(seconds=scan_interval),
    )
    
    # Primo aggiornamento per popolare i dati
    await coordinator.async_config_entry_first_refresh()
    _LOGGER.info("Primo aggiornamento dati completato")
    
    # Salva API e coordinator nell'hass data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,  # Salvato QUI, disponibile per tutti
        "scan_interval": scan_interval
    }
    
    _LOGGER.info(f"Coordinator salvato in hass.data[{DOMAIN}][{entry.entry_id}]")
    
    # Setup delle piattaforme - ora il coordinator è già pronto
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    _LOGGER.info("Setup completato - piattaforme caricate")
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Scarica l'integrazione."""
    _LOGGER.info("Unload WiNET Stufa")
    
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        # Chiude la sessione API
        api = hass.data[DOMAIN][entry.entry_id]["api"]
        await api.async_close()
        
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Integrazione scaricata correttamente")
    
    return unload_ok