# ============================================================================
# FILE: custom_components/winet_stufa/sensor.py
# VERSIONE CORRETTA - Sensori che leggono dagli attributi del climate
# ============================================================================

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import SIGNAL_STRENGTH_DECIBELS_MILLIWATT
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
    """Setup sensor entities."""
    # Prende il coordinator salvato in climate.py
    coordinator = hass.data[DOMAIN][entry.entry_id].get("coordinator")
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    
    if not coordinator:
        _LOGGER.error("Coordinator non trovato per i sensori!")
        return
    
    _LOGGER.info("Creazione sensori WiNET Stufa")
    
    sensors = [
        WinetStufaStateSensor(coordinator, api, entry),
        WinetStufaPowerSensor(coordinator, api, entry),
        WinetStufaFanSensor(coordinator, api, entry),
        WinetStufaRSSISensor(coordinator, api, entry),
        WinetStufaAlarmSensor(coordinator, api, entry),
        WinetStufaAlarmCodeSensor(coordinator, api, entry),  # Nuovo: codice allarme numerico
        WinetStufaCronoSensor(coordinator, api, entry),  # Nuovo: stato crono
    ]
    
    async_add_entities(sensors)
    _LOGGER.info(f"Creati {len(sensors)} sensori")

class WinetStufaBaseSensor(CoordinatorEntity, SensorEntity):
    """Sensore base."""
    
    def __init__(self, coordinator, api, entry, sensor_type):
        """Inizializza."""
        super().__init__(coordinator)
        self._api = api
        self._sensor_type = sensor_type
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }
        self._attr_has_entity_name = True

class WinetStufaStateSensor(WinetStufaBaseSensor):
    """Sensore stato stufa."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "state")
        self._attr_name = "Stato"
        self._attr_unique_id = f"{entry.entry_id}_state"
        self._attr_icon = "mdi:fire"
    
    @property
    def native_value(self):
        """Valore del sensore."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            state = self._api.get_state(self.coordinator.data["registers"])
            state_name = STOVE_STATES.get(state, "unknown")
            
            # Traduzione in italiano
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
            
            _LOGGER.debug(f"Sensor state: code={state}, name={state_name}")
            return state_names_it.get(state_name, state_name)
        return "Non Disponibile"
    
    @property
    def available(self):
        """Sensore sempre disponibile se c'è connessione."""
        return self.coordinator.last_update_success
    
    @property
    def extra_state_attributes(self):
        """Attributi extra."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            state = self._api.get_state(self.coordinator.data["registers"])
            return {
                "state_code": state,
                "state_english": STOVE_STATES.get(state, "unknown")
            }
        return {}

class WinetStufaPowerSensor(WinetStufaBaseSensor):
    """Sensore potenza."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "power")
        self._attr_name = "Potenza"
        self._attr_unique_id = f"{entry.entry_id}_power"
        self._attr_icon = "mdi:fire-circle"
        self._attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self):
        """Valore del sensore."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            power = self._api.get_power(self.coordinator.data["registers"])
            _LOGGER.debug(f"Sensor power: {power}")
            return power
        return None
    
    @property
    def available(self):
        """Sensore sempre disponibile se c'è connessione."""
        return self.coordinator.last_update_success

class WinetStufaFanSensor(WinetStufaBaseSensor):
    """Sensore ventilazione."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "fan")
        self._attr_name = "Ventilazione"
        self._attr_unique_id = f"{entry.entry_id}_fan"
        self._attr_icon = "mdi:fan"
        self._attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self):
        """Valore del sensore."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            fan = self._api.get_fan_speed(self.coordinator.data["registers"])
            _LOGGER.debug(f"Sensor fan: {fan}")
            return fan
        return None
    
    @property
    def available(self):
        """Sensore sempre disponibile se c'è connessione."""
        return self.coordinator.last_update_success

class WinetStufaRSSISensor(WinetStufaBaseSensor):
    """Sensore segnale WiFi."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "rssi")
        self._attr_name = "Segnale WiFi"
        self._attr_unique_id = f"{entry.entry_id}_rssi"
        self._attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
        self._attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT
        self._attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self):
        """Valore del sensore."""
        if self.coordinator.data:
            rssi = self.coordinator.data.get("rssi")
            _LOGGER.debug(f"Sensor RSSI: {rssi}")
            return rssi
        return None
    
    @property
    def available(self):
        """Sensore sempre disponibile se c'è connessione."""
        return self.coordinator.last_update_success

class WinetStufaAlarmSensor(WinetStufaBaseSensor):
    """Sensore allarmi stufa - Mostra descrizione allarme."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "alarm")
        self._attr_name = "Allarme"
        self._attr_unique_id = f"{entry.entry_id}_alarm"
    
    @property
    def native_value(self):
        """Valore del sensore - sempre disponibile."""
        if not self.coordinator.data or "registers" not in self.coordinator.data:
            return "Connessione persa"
        
        alarm_code = self._api.get_alarm_code(self.coordinator.data["registers"])
        
        if alarm_code == 0:
            return "Nessun Allarme"
        
        # Decodifica gli allarmi
        alarms = self._api.decode_alarm(alarm_code)
        
        if alarms:
            # Mostra il primo allarme come stato
            return alarms[0]["description"]
        
        return f"Allarme Sconosciuto (code: {alarm_code})"
    
    @property
    def available(self):
        """Sensore sempre disponibile - mostra anche errori di connessione."""
        return True  # Sempre disponibile, mostra "Connessione persa" se offline
    
    @property
    def icon(self):
        """Icona dinamica basata sullo stato."""
        if not self.coordinator.data or "registers" not in self.coordinator.data:
            return "mdi:lan-disconnect"
        
        alarm_code = self._api.get_alarm_code(self.coordinator.data["registers"])
        if alarm_code == 0:
            return "mdi:check-circle"
        return "mdi:alert-circle"
    
    @property
    def extra_state_attributes(self):
        """Attributi extra con tutti gli allarmi."""
        if not self.coordinator.data or "registers" not in self.coordinator.data:
            return {
                "alarm_code": None,
                "alarm_count": 0,
                "has_alarm": False,
            }
        
        alarm_code = self._api.get_alarm_code(self.coordinator.data["registers"])
        alarms = self._api.decode_alarm(alarm_code)
        
        attributes = {
            "alarm_code": alarm_code,
            "alarm_count": len(alarms),
            "has_alarm": alarm_code != 0,
        }
        
        # Aggiungi tutti gli allarmi come attributi
        if alarms:
            attributes["alarms"] = [alarm["description"] for alarm in alarms]
            for i, alarm in enumerate(alarms, 1):
                attributes[f"alarm_{i}"] = alarm["description"]
                attributes[f"alarm_{i}_bit"] = alarm["bit"]
        
        return attributes

class WinetStufaAlarmCodeSensor(WinetStufaBaseSensor):
    """Sensore codice allarme numerico - utile per automazioni."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "alarm_code")
        self._attr_name = "Codice Allarme"
        self._attr_unique_id = f"{entry.entry_id}_alarm_code"
        self._attr_icon = "mdi:numeric"
        self._attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self):
        """Valore del sensore."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            alarm_code = self._api.get_alarm_code(self.coordinator.data["registers"])
            return alarm_code
        return None
    
    @property
    def available(self):
        """Sensore sempre disponibile se c'è connessione."""
        return self.coordinator.last_update_success
    
    @property
    def extra_state_attributes(self):
        """Attributi extra."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            alarm_code = self._api.get_alarm_code(self.coordinator.data["registers"])
            return {
                "has_alarm": alarm_code != 0,
                "hex": f"0x{alarm_code:08X}",
                "binary": f"{alarm_code:032b}"
            }
        return {}

class WinetStufaCronoSensor(WinetStufaBaseSensor):
    """Sensore stato crono/programmazione."""
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "crono")
        self._attr_name = "Crono"
        self._attr_unique_id = f"{entry.entry_id}_crono"
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["Attivo", "Disattivo"]
    
    @property
    def native_value(self):
        """Valore del sensore."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            registers = self.coordinator.data["registers"]
            
            # Registro 7 controlla il crono
            # Valore 3 (0b00000011) = Crono attivo
            # Valore 128 (0b10000000) = Crono disattivo
            reg7_value = registers.get(7, 0)
            
            # Controlla i bit bassi (0-2) per il crono
            # Se uno dei primi 3 bit è attivo, il crono è ON
            if reg7_value & 0b00000111:  # Maschera bit 0, 1, 2
                return "Attivo"
            else:
                return "Disattivo"
        
        return "Disattivo"
    
    @property
    def icon(self):
        """Icona dinamica."""
        if self.native_value == "Attivo":
            return "mdi:clock-check"
        else:
            return "mdi:clock-outline"
    
    @property
    def available(self):
        """Sensore sempre disponibile se c'è connessione."""
        return self.coordinator.last_update_success
    
    @property
    def extra_state_attributes(self):
        """Attributi extra."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            registers = self.coordinator.data["registers"]
            reg7_value = registers.get(7, 0)
            
            return {
                "register_value": reg7_value,
                "register_number": 7,
                "register_binary": f"{reg7_value:08b}",
                "register_hex": f"0x{reg7_value:02X}",
                "is_active": bool(reg7_value & 0b00000111)
            }
        return {}

class WinetStufaDebugSensor(WinetStufaBaseSensor):
    """Sensore DEBUG - Mostra tutti i registri grezzi.
    ATTENZIONE: Rimuovere dopo aver identificato il registro crono!
    """
    
    def __init__(self, coordinator, api, entry):
        """Inizializza."""
        super().__init__(coordinator, api, entry, "debug_registers")
        self._attr_name = "DEBUG Registri"
        self._attr_unique_id = f"{entry.entry_id}_debug_registers"
        self._attr_icon = "mdi:bug"
        self._attr_entity_category = "diagnostic"
    
    @property
    def native_value(self):
        """Valore del sensore - mostra quanti registri ci sono."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            registers = self.coordinator.data["registers"]
            return f"{len(registers)} registri"
        return "N/D"
    
    @property
    def available(self):
        """Sensore sempre disponibile se c'è connessione."""
        return self.coordinator.last_update_success
    
    @property
    def extra_state_attributes(self):
        """Attributi extra - TUTTI i registri grezzi."""
        if self.coordinator.data and "registers" in self.coordinator.data:
            registers = self.coordinator.data["registers"]
            
            # Crea un dizionario con TUTTI i registri
            attrs = {}
            
            for reg_num in sorted(registers.keys()):
                value = registers[reg_num]
                attrs[f"reg_{reg_num}"] = value
                attrs[f"reg_{reg_num}_hex"] = f"0x{value:04X}"
                attrs[f"reg_{reg_num}_bin"] = f"{value:016b}"
            
            # Aggiungi anche statistiche
            attrs["total_registers"] = len(registers)
            attrs["min_register"] = min(registers.keys()) if registers else 0
            attrs["max_register"] = max(registers.keys()) if registers else 0
            
            return attrs
        
        return {"error": "No data available"}