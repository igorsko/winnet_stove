# ============================================================================
# FILE: custom_components/winet_stufa/system_health.py
# Mostra informazioni nell'area System Health di Home Assistant
# ============================================================================

from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback
import os

from .const import DOMAIN

@callback
def async_register(
    hass: HomeAssistant, register: system_health.SystemHealthRegistration
) -> None:
    """Registra le informazioni di system health."""
    register.async_register_info(system_health_info)

async def system_health_info(hass: HomeAssistant):
    """Get info for the system health card."""
    
    # Conta quante stufe sono configurate
    entry_count = len(hass.config_entries.async_entries(DOMAIN))
    
    # Verifica se Mushroom è installato (euristica)
    mushroom_installed = await check_mushroom_installed(hass)
    
    info = {
        "integration_version": "1.0.0",
        "configured_stoves": entry_count,
        "mushroom_cards": "✅ Installato" if mushroom_installed else "⚠️ Non rilevato (consigliato per card ottimizzate)",
    }
    
    # Aggiungi info per ogni stufa configurata
    for idx, entry in enumerate(hass.config_entries.async_entries(DOMAIN), 1):
        if entry.entry_id in hass.data.get(DOMAIN, {}):
            data = hass.data[DOMAIN][entry.entry_id]
            coordinator = data.get("coordinator")
            
            if coordinator and coordinator.last_update_success:
                info[f"stove_{idx}_status"] = "🟢 Connesso"
                info[f"stove_{idx}_host"] = entry.data.get("host", "N/D")
            else:
                info[f"stove_{idx}_status"] = "🔴 Non raggiungibile"
                info[f"stove_{idx}_host"] = entry.data.get("host", "N/D")
    
    return info

async def check_mushroom_installed(hass: HomeAssistant) -> bool:
    """Controlla euristicamente se Mushroom Cards è installato."""
    # Verifica se esiste la cartella di Mushroom in www o custom_components
    mushroom_paths = [
        "www/community/lovelace-mushroom",
        "custom_components/mushroom",
    ]
    
    config_dir = hass.config.config_dir
    
    for path in mushroom_paths:
        full_path = os.path.join(config_dir, path)
        if os.path.exists(full_path):
            return True
    
    # Verifica se mushroom è nei resources di lovelace
    # Nota: questo metodo non è affidabile al 100%
    try:
        lovelace_config = hass.data.get("lovelace")
        if lovelace_config:
            resources = lovelace_config.get("resources", [])
            for resource in resources:
                if "mushroom" in resource.get("url", "").lower():
                    return True
    except Exception:
        pass
    
    return False