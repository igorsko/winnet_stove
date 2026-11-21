# SPDX-License-Identifier: GPL-3.0-only
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST

from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .api import WinetStufaAPI

class WinetStufaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow per WiNET Stufa."""
    
    VERSION = 1
    
    async def async_step_user(self, user_input=None):
        """Gestisce il flow iniziato dall'utente."""
        errors = {}
        
        if user_input is not None:
            host = user_input[CONF_HOST]
            
            # Testa la connessione
            api = WinetStufaAPI(host)
            try:
                connected = await api.async_test_connection()
            finally:
                await api.async_close()
            if connected:
                # Connessione riuscita
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=f"Stufa WiNET ({host})",
                    data={CONF_HOST: host}
                )
            else:
                errors["base"] = "cannot_connect"
        
        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default="192.168.1.100"): str,
        })
        
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "example": "Es: 192.168.1.100"
            }
        )
    
    @staticmethod
    def async_get_options_flow(config_entry):
        """Opzioni flow."""
        return WinetStufaOptionsFlow(config_entry)

class WinetStufaOptionsFlow(config_entries.OptionsFlow):
    """Options flow per WiNET Stufa."""
    
    def __init__(self, config_entry):
        """Inizializza."""
        self._legacy_entry = config_entry
    
    async def async_step_init(self, user_input=None):
        """Gestisce le opzioni."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self._legacy_entry.options.get(
                        CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                    )
                ): vol.All(vol.Coerce(int), vol.Range(min=10, max=300))
            })
        )
