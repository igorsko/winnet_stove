# SPDX-License-Identifier: GPL-3.0-only
# ============================================================================
# FILE: custom_components/winet_stufa/switch.py
# ============================================================================

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging
import asyncio
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup switch entity per controllo crono."""
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    coordinator = data["coordinator"]
    
    _LOGGER.info("Setup Switch - Crono")
    
    async_add_entities([
        WinetStufaCronoSwitch(coordinator, api, entry),
        WinetAutoPelletRefillSwitch(data['usage'], entry),
    ])

class WinetStufaCronoSwitch(CoordinatorEntity, SwitchEntity):
    """Switch per attivare/disattivare il crono."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator)
        self._api = api
        self._attr_name = "Crono"
        self._attr_unique_id = f"{entry.entry_id}_crono_switch"
        self._attr_icon = "mdi:clock-check-outline"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }
    
    @property
    def is_on(self):
        """Ritorna True se il crono è attivo."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            registers = self.coordinator.data["registers"]
            return self._api.get_crono_state(registers)
        return None
    
    @property
    def icon(self):
        """Icona dinamica."""
        if self.is_on:
            return "mdi:clock-check"
        return "mdi:clock-outline"
    
    @property
    def extra_state_attributes(self):
        """Attributi extra."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            registers = self.coordinator.data["registers"]
            reg7_value = registers.get(7, 0)
            
            return {
                "register_7": reg7_value,
                "register_7_binary": f"{reg7_value:08b}",
                "register_7_hex": f"0x{reg7_value:02X}",
            }
        return {}
    
    async def async_turn_on(self, **kwargs):
        """Attiva il crono."""
        _LOGGER.info("Switch: Attivazione crono richiesta")
        success = await self._api.async_set_crono_on()
        
        if success:
            _LOGGER.info("Switch: Crono attivato")
            # Forza aggiornamento immediato
            await asyncio.sleep(2)  # Aspetta che la stufa applichi il cambiamento
            await self.coordinator.async_request_refresh()
        else:
            raise HomeAssistantError("WiNET stove rejected cron enable")
    
    async def async_turn_off(self, **kwargs):
        """Disattiva il crono."""
        _LOGGER.info("Switch: Disattivazione crono richiesta")
        success = await self._api.async_set_crono_off()
        
        if success:
            _LOGGER.info("Switch: Crono disattivato")
            # Forza aggiornamento immediato
            await asyncio.sleep(2)
            await self.coordinator.async_request_refresh()
        else:
            raise HomeAssistantError("WiNET stove rejected cron disable")

# Importa asyncio per il sleep
import asyncio
class WinetAutoPelletRefillSwitch(SwitchEntity):
    """Opt-in automatic refill inference based on a stove alarm and recovery."""

    _attr_has_entity_name = True
    _attr_name = "Infer pellet refill after alarm"
    _attr_icon = "mdi:bag-checked"

    def __init__(self, usage, entry):
        self._usage = usage
        self._attr_unique_id = f"{entry.entry_id}_pellet_auto_refill"
        self._attr_device_info = {"identifiers": {(DOMAIN, entry.entry_id)}}

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(self._usage.async_subscribe(self.async_write_ha_state))

    @property
    def is_on(self):
        return self._usage.auto_refill_enabled

    @property
    def extra_state_attributes(self):
        return {
            "alarm": "NO PELLET / CLEAN BURNER (bit 0)",
            "inferred_refills": self._usage.auto_bags_loaded,
            "last_inferred_refill": self._usage.last_auto_refill,
            "refill_pending": self._usage._auto_detector.pending,
            "note": "A refill is inferred, not measured. False positives are possible.",
        }

    async def async_turn_on(self, **kwargs):
        await self._usage.async_set_auto_refill(True)

    async def async_turn_off(self, **kwargs):
        await self._usage.async_set_auto_refill(False)
