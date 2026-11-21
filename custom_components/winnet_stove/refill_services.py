# SPDX-License-Identifier: GPL-3.0-only
"""Home Assistant service endpoints for the refill editor."""

from uuid import UUID

import voluptuous as vol
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .refill_log import MAX_KG


def _entry_usage(hass, entry_id):
    info = hass.data.get(DOMAIN, {}).get(entry_id)
    if info is None or "usage" not in info:
        raise HomeAssistantError("WiNET Stove device not found")
    return info["usage"]


def register_refill_services(hass):
    """Register once, including for multiple stoves. Never write to hardware."""
    if hass.services.has_service(DOMAIN, "record_refill"):
        return

    async def record(call):
        try:
            await _entry_usage(hass, call.data["entry_id"]).async_record_refill(
                call.data["quantity_kg"]
            )
        except ValueError as err:
            raise HomeAssistantError(str(err)) from err

    async def edit(call):
        try:
            await _entry_usage(hass, call.data["entry_id"]).async_edit_refill(
                str(UUID(call.data["refill_id"])), call.data["quantity_kg"]
            )
        except ValueError as err:
            raise HomeAssistantError(str(err)) from err

    async def remove(call):
        try:
            await _entry_usage(hass, call.data["entry_id"]).async_remove_refill(
                str(UUID(call.data["refill_id"]))
            )
        except ValueError as err:
            raise HomeAssistantError(str(err)) from err

    common = {vol.Required("entry_id"): str}
    quantity = {**common, vol.Required("quantity_kg"): vol.All(
        vol.Coerce(float), vol.Range(min=0.001, max=MAX_KG)
    )}
    item = {vol.Required("refill_id"): str}

    hass.services.async_register(
        DOMAIN, "record_refill", record, schema=vol.Schema(quantity)
    )
    hass.services.async_register(
        DOMAIN, "edit_refill", edit, schema=vol.Schema({**quantity, **item})
    )
    hass.services.async_register(
        DOMAIN, "remove_refill", remove, schema=vol.Schema({**common, **item})
    )
