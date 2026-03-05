# ============================================================================
# FILE: custom_components/winet_stufa/api.py
# VERSIONE con controllo crono
# ============================================================================

import aiohttp
import asyncio
import logging

_LOGGER = logging.getLogger(__name__)

class WinetStufaAPI:
    """API per comunicare con la stufa WiNET."""
    
    def __init__(self, host: str):
        """Inizializza l'API."""
        self.host = host
        self.base_url = f"http://{host}/ajax"
        self._session = None
    
    async def async_get_session(self):
        """Ottiene o crea una sessione aiohttp."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def async_close(self):
        """Chiude la sessione."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def async_test_connection(self) -> bool:
        """Testa la connessione alla stufa."""
        try:
            data = await self.async_get_data()
            return data is not None
        except Exception:
            return False
    
    async def async_get_data(self) -> dict:
        """Legge tutti i dati dalla stufa."""
        url = f"{self.base_url}/get-registers"
        data = "key=020&category=1"
        
        try:
            session = await self.async_get_session()
            async with session.post(url, data=data, timeout=10) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    
                    if "registers" in result:
                        # Converti in dizionario
                        registers = {num: val for num, val in result["registers"]}
                        
                        return {
                            "name": result.get("name", "Stufa"),
                            "rssi": result.get("rssi"),
                            "registers": registers
                        }
            return None
        except Exception as e:
            _LOGGER.error("Errore lettura dati: %s", e)
            return None
    
    def get_temperature(self, registers: dict) -> float:
        """Calcola la temperatura dal registro 16.
        Formula: (registro ÷ 4) - 18
        """
        if 16 in registers:
            return (registers[16] * 0.25) - 18.0
        return None
    
    def get_target_temperature(self, registers: dict) -> float:
        """Ottiene la temperatura target (registro 4 su cat 2)."""
        # TODO: implementare lettura categoria 2
        return None
    
    def get_state(self, registers: dict) -> int:
        """Ottiene lo stato della stufa (registro 6)."""
        if 6 in registers:
            return registers[6] & 0xFF
        return 0
    
    def get_power(self, registers: dict) -> int:
        """Ottiene la potenza (registro 12)."""
        return registers.get(12, 0)
    
    def get_fan_speed(self, registers: dict) -> int:
        """Ottiene la velocità ventilazione (registro 13)."""
        return registers.get(13, 0)
    
    def get_crono_state(self, registers: dict) -> bool:
        """Verifica se il crono è attivo (registro 7).
        Registro 7 bit 0-2: se attivi = crono ON
        """
        if 7 in registers:
            reg7_value = registers[7]
            # Controlla i bit bassi (0, 1, 2)
            return bool(reg7_value & 0b00000111)
        return False
    
    def get_alarm_code(self, registers: dict) -> int:
        """Ottiene il codice allarme combinando registri 8 e 9."""
        alarm_lsb = registers.get(8, 0)
        alarm_msb = registers.get(9, 0)
        # Combina i due byte in un word (32 bit)
        return (alarm_msb << 16) | alarm_lsb
    
    def decode_alarm(self, alarm_code: int) -> list:
        """Decodifica il codice allarme in lista di allarmi attivi."""
        if alarm_code == 0:
            return []
        
        alarm_descriptions = {
            0: "NO PELLET / CLEAN BURNER",
            1: "FAILED START / CLEAN BURNER",
            2: "SMOKE NO-OUT / CHECK OUTLET",
            3: "ALARM T MAX / CHECK WATER CIRCUIT/PUMP",
            4: "AL SMOKE TEMP SENSOR",
            5: "AL SMOKE R.P.M. SENSOR",
            6: "AL SMOKE FAN",
            7: "ALARM EARTHQUAKE",
            8: "S1 DISCONNECTED",
            9: "S2 DISCONNECTED",
            10: "S. ACS DISCONNECTED",
            11: "S.T.A. DISCONNECTED",
            12: "CLEANING MOTOR",
            13: "TROLLEY FULL",
            14: "TROLLEY OUTSIDE",
            15: "LCD TIMEOUT",
            16: "S.t.g. DISCONNECTED",
        }
        
        alarms = []
        for bit in range(32):
            if alarm_code & (1 << bit):
                alarms.append({
                    "bit": bit,
                    "description": alarm_descriptions.get(bit, f"Unknown alarm (bit {bit})")
                })
        
        return alarms
    
    async def async_turn_on(self) -> bool:
        """Accende la stufa."""
        return await self.async_set_register(1, 23040)
    
    async def async_turn_off(self) -> bool:
        """Spegne la stufa."""
        return await self.async_set_register(1, 42240)
    
    async def async_set_crono_on(self) -> bool:
        """Attiva il crono (programmazione oraria).
        Scrive valore 3 nel registro 7.
        """
        _LOGGER.info("Attivazione crono...")
        result = await self.async_set_register(7, 3)
        if result:
            _LOGGER.info("Crono attivato con successo")
        else:
            _LOGGER.error("Errore attivazione crono")
        return result
    
    async def async_set_crono_off(self) -> bool:
        """Disattiva il crono (programmazione oraria).
        Scrive valore 128 nel registro 7.
        """
        _LOGGER.info("Disattivazione crono...")
        result = await self.async_set_register(7, 128)
        if result:
            _LOGGER.info("Crono disattivato con successo")
        else:
            _LOGGER.error("Errore disattivazione crono")
        return result
    
    async def async_toggle_crono(self, current_state: bool) -> bool:
        """Toggle crono: attiva se spento, spegne se attivo."""
        if current_state:
            return await self.async_set_crono_off()
        else:
            return await self.async_set_crono_on()
    
    async def async_set_register(self, reg_id: int, value: int) -> bool:
        """Scrive un registro."""
        url = f"{self.base_url}/set-register"
        data = f"key=002&regId={reg_id}&value={value}"
        
        try:
            session = await self.async_get_session()
            async with session.post(url, data=data, timeout=10) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    success = result.get("result", False)
                    _LOGGER.debug(f"Set register {reg_id}={value}: {success}")
                    return success
            return False
        except Exception as e:
            _LOGGER.error("Errore scrittura registro %d: %s", reg_id, e)
            return False