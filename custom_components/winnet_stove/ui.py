# SPDX-License-Identifier: GPL-3.0-only
"""Install an optional side panel and a separate, editable Lovelace dashboard.

The dashboard is only populated on its first creation. Existing user-owned
dashboards and views are never overwritten or deleted.
"""

import logging
from pathlib import Path

from homeassistant.components import frontend, panel_custom
from homeassistant.components.http import StaticPathConfig
from homeassistant.components.lovelace import dashboard
from homeassistant.components.lovelace.const import LOVELACE_DATA
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.storage import Store

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PANEL_PATH = "winnet-stove"
LOVELACE_PATH = "winnet-stove-dashboard"
PANEL_JS = "/api/winnet_stove/panel.js"
STATE_KEY = "winnet_stove_ui_ownership"


def _entries(hass):
    """Only loaded WiNET Stove entries contribute UI options."""
    loaded = hass.data.get(DOMAIN, {})
    return [
        entry for entry in hass.config_entries.async_entries(DOMAIN)
        if entry.entry_id in loaded
    ]


def _entities(hass, entries):
    """Use the registry so renamed entities still work."""
    registry = er.async_get(hass)
    result = {}
    for entry in entries:
        by_suffix = {}
        prefix = entry.entry_id + "_"
        for item in registry.entities.values():
            if item.platform != DOMAIN or item.config_entry_id != entry.entry_id:
                continue
            if item.disabled or not item.unique_id.startswith(prefix):
                continue
            by_suffix[item.unique_id[len(prefix):]] = item.entity_id
        result[entry.entry_id] = by_suffix
    return result


def _panel_config(entries, entities):
    return {
        "stoves": [
            {"title": entry.title, "entities": entities[entry.entry_id]}
            for entry in entries
        ]
    }


def _lovelace_config(entries, entities):
    views = []
    for index, entry in enumerate(entries, 1):
        mapping = entities[entry.entry_id]
        cards = []
        if climate_id := mapping.get("climate"):
            cards.append({"type": "thermostat", "entity": climate_id})
        monitored = [
            mapping[key]
            for key in ("state", "power", "fan", "rssi", "alarm", "alarm_code", "crono")
            if key in mapping
        ]
        if monitored:
            cards.append({
                "type": "entities", "title": "Stove status", "entities": monitored
            })
        if switch_id := mapping.get("crono_switch"):
            cards.append({
                "type": "entities", "title": "Timer", "entities": [switch_id]
            })
        history = [mapping[key] for key in ("state", "power") if key in mapping]
        if history:
            cards.append({
                "type": "history-graph",
                "title": "Last 24 hours",
                "hours_to_show": 24,
                "entities": history,
            })
        if not cards:
            cards.append({
                "type": "markdown",
                "content": "WiNET Stove entities are not yet available. Reload the integration.",
            })
        views.append({
            "title": entry.title or f"Stove {index}",
            "path": f"stove-{index}",
            "icon": "mdi:fire",
            "cards": cards,
        })
    return {"title": "WiNET Stove", "views": views}


async def async_update_ui(hass):
    """Reconcile both UI surfaces without modifying unrelated dashboards."""
    entries = _entries(hass)
    state = hass.data.setdefault(f"{DOMAIN}_ui", {})
    show_panel = any(e.options.get("show_panel", True) for e in entries)
    show_lovelace = any(e.options.get("show_lovelace", True) for e in entries)

    if show_panel:
        if not state.get("static_ready"):
            await hass.http.async_register_static_paths([
                StaticPathConfig(
                    PANEL_JS,
                    str(Path(__file__).parent / "frontend" / "panel.js"),
                    cache_headers=False,
                )
            ])
            state["static_ready"] = True
        if state.get("panel_ready"):
            frontend.async_remove_panel(hass, PANEL_PATH)
            state["panel_ready"] = False
        if not frontend.async_panel_exists(hass, PANEL_PATH):
            await panel_custom.async_register_panel(
                hass,
                frontend_url_path=PANEL_PATH,
                webcomponent_name="winnet-stove-panel",
                module_url=PANEL_JS,
                sidebar_title="WiNET Stove",
                sidebar_icon="mdi:fire",
                config=_panel_config(entries, _entities(hass, entries)),
            )
            state["panel_ready"] = True
        else:
            _LOGGER.warning("Panel path %s already exists; not replacing it", PANEL_PATH)
    elif state.get("panel_ready"):
        frontend.async_remove_panel(hass, PANEL_PATH)
        state["panel_ready"] = False

    await _async_update_lovelace(hass, entries, show_lovelace)


async def _async_update_lovelace(hass, entries, visible):
    """Create dashboard once; visibility toggles never overwrite its cards."""
    if LOVELACE_DATA not in hass.data:
        _LOGGER.warning("Lovelace is not loaded; cannot set up WiNET dashboard")
        return

    owner_store = Store(hass, 1, STATE_KEY)
    owner = await owner_store.async_load() or {}
    collection = dashboard.DashboardsCollection(hass)
    await collection.async_load()
    existing = next(
        (item for item in collection.async_items()
         if item.get("url_path") == LOVELACE_PATH),
        None,
    )

    if existing and not owner.get("created"):
        _LOGGER.warning("Dashboard path %s is already owned by the user", LOVELACE_PATH)
        return
    if not existing and owner.get("created"):
        # A user intentionally deleted the previously managed dashboard.
        _LOGGER.info("WiNET Lovelace dashboard was removed; not recreating it")
        return
    if not existing and (not visible or not entries):
        return

    if existing is None:
        existing = await collection.async_create_item({
            "url_path": LOVELACE_PATH,
            "title": "WiNET Stove",
            "icon": "mdi:fire",
            "show_in_sidebar": True,
            "require_admin": False,
        })
        storage = dashboard.LovelaceStorage(hass, existing)
        await storage.async_save(_lovelace_config(entries, _entities(hass, entries)))
        hass.data[LOVELACE_DATA].dashboards[LOVELACE_PATH] = storage
        await owner_store.async_save({"created": True})
        frontend.async_register_built_in_panel(
            hass, "lovelace",
            frontend_url_path=LOVELACE_PATH,
            sidebar_title="WiNET Stove",
            sidebar_icon="mdi:fire",
            show_in_sidebar=True,
            require_admin=False,
            config={"mode": "storage"},
        )
    elif existing.get("show_in_sidebar", True) != visible:
        updated = await collection.async_update_item(
            existing["id"], {"show_in_sidebar": visible}
        )
        stored = hass.data[LOVELACE_DATA].dashboards.get(LOVELACE_PATH)
        if stored:
            stored.config = updated
        if frontend.async_panel_exists(hass, LOVELACE_PATH):
            frontend.async_register_built_in_panel(
                hass, "lovelace",
                frontend_url_path=LOVELACE_PATH,
                sidebar_title=updated["title"],
                sidebar_icon=updated.get("icon", "mdi:fire"),
                show_in_sidebar=visible,
                require_admin=updated.get("require_admin", False),
                config={"mode": "storage"},
                update=True,
            )
