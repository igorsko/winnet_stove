# ============================================================================
# FILE: custom_components/winet_stufa/climate.py
# VERSIONE CORRETTA - Usa coordinator creato in __init__.py
# ============================================================================

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
)
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from .const import DOMAIN, STOVE_STATES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup climate entity."""
    data = hass.data[DOMAIN][entry.entry_id]
    api = data["api"]
    coordinator = data["coordinator"]  # Usa quello creato in __init__.py
    
    _LOGGER.info("Setup Climate - Coordinator disponibile")
    
    async_add_entities([WinetStufaClimate(coordinator, api, entry)])

class WinetStufaClimate(CoordinatorEntity, ClimateEntity):
    """Climate entity per la stufa."""
    
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_supported_features = (
        ClimateEntityFeature.TURN_ON |
        ClimateEntityFeature.TURN_OFF
    )
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_min_temp = 5
    _attr_max_temp = 40
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator)
        self._api = api
        self._attr_name = "Stufa WiNET"
        self._attr_unique_id = f"{entry.entry_id}_climate"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Stufa WiNET",
            "manufacturer": "Micronova/Thermorossi",
            "model": "WiNET",
        }
    
    @property
    def current_temperature(self):
        """Temperatura corrente."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            temp = self._api.get_temperature(self.coordinator.data["registers"])
            _LOGGER.debug(f"Current temperature: {temp}°C")
            return temp
        return None
    
    @property
    def hvac_mode(self):
        """Modalità HVAC corrente."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            state = self._api.get_state(self.coordinator.data["registers"])
            _LOGGER.debug(f"Stove state: {state} -> {STOVE_STATES.get(state)}")
            if state in [0, 1, 8]:  # Off, off, stop
                return HVACMode.OFF
            return HVACMode.HEAT
        return HVACMode.OFF
    
    @property
    def hvac_action(self):
        """Azione HVAC corrente."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            state = self._api.get_state(self.coordinator.data["registers"])
            if state == 3:  # Working
                return HVACAction.HEATING
            elif state in [2, 4, 5, 6, 7, 9]:  # Starting, waiting, etc
                return HVACAction.IDLE
        return HVACAction.OFF
    
    @property
    def extra_state_attributes(self):
        """Attributi extra con TUTTI i dati."""
        if not self.coordinator.data or "registers" not in self.coordinator.data:
            return {}
        
        registers = self.coordinator.data["registers"]
        state_code = self._api.get_state(registers)
        state_name = STOVE_STATES.get(state_code, "unknown")
        
        # Mappa stati in italiano
        state_names_it = {
            "unknown": "Sconosciuto",
            "off": "Spento",
            "starting": "Avvio",
            "working": "In Funzione",
            "wait_on": "Attesa Accensione",
            "temp_ok": "Temperatura OK",
            "no_program": "Nessun Programma",
            "wait_time": "Attesa Orario",
            "stop": "Arresto",
            "sunout": "Spento"
        }
        
        power = self._api.get_power(registers)
        fan = self._api.get_fan_speed(registers)
        rssi = self.coordinator.data.get("rssi")
        alarm_code = self._api.get_alarm_code(registers)
        
        _LOGGER.debug(f"Extra attributes - State: {state_name}, Power: {power}, Fan: {fan}, RSSI: {rssi}, Alarm: {alarm_code}")
        
        attributes = {
            "state_code": state_code,
            "state": state_name,
            "state_italian": state_names_it.get(state_name, state_name),
            "power_level": power,
            "fan_speed": fan,
            "rssi": rssi,
            "is_on": state_code not in [0, 1, 8],
            "alarm_code": alarm_code,
            "has_alarm": alarm_code != 0,
        }
        
        # Aggiungi descrizione allarme se presente
        if alarm_code != 0:
            alarms = self._api.decode_alarm(alarm_code)
            if alarms:
                attributes["alarm_description"] = alarms[0]["description"]
                attributes["alarm_count"] = len(alarms)
        
        # DEBUG: Aggiungi TUTTI i registri grezzi come attributi
        # TODO: Rimuovere dopo aver identificato il registro crono
        for reg_num, reg_value in registers.items():
            attributes[f"register_{reg_num}"] = reg_value
        
        return attributes
    
    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Imposta la modalità HVAC."""
        _LOGGER.info(f"Setting HVAC mode to: {hvac_mode}")
        
        if hvac_mode == HVACMode.HEAT:
            success = await self._api.async_turn_on()
            _LOGGER.info(f"Turn ON result: {success}")
        elif hvac_mode == HVACMode.OFF:
            success = await self._api.async_turn_off()
            _LOGGER.info(f"Turn OFF result: {success}")
        
        # Forza aggiornamento immediato
        await self.coordinator.async_request_refresh()