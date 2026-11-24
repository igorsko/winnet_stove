# SPDX-License-Identifier: GPL-3.0-only
"""Conservative recovery of historical cumulative power counters."""

from datetime import datetime, timedelta
from math import isfinite


def recover_snapshot(event, samples, max_age):
    """Find a real, nearby cumulative reading consistent with refill runtime.

    Recorded power_hours are rounded to 0.01 h. Never interpolate, extrapolate
    or replace native snapshots. Unknown power and incomplete totals are rejected.
    """
    if event.get("power_seconds") is not None:
        return None
    runtime = event.get("runtime_h")
    if not isinstance(runtime, (int, float)) or not isfinite(runtime) or runtime <= 0:
        return None
    try:
        at = datetime.fromisoformat(event["at"].replace("Z", "+00:00"))
        if at.tzinfo is None:
            return None
    except (KeyError, TypeError, ValueError):
        return None
    for stamp, values in sorted(samples, key=lambda item: item[0], reverse=True):
        age = (at - stamp).total_seconds()
        if not 0 <= age <= max_age or not isinstance(values, dict) or not values:
            continue
        if any(key not in ("1", "2", "3", "4", "5") or
               isinstance(value, bool) or not isinstance(value, (int, float)) or
               not isfinite(value) or value < 0 for key, value in values.items()):
            continue
        seconds = {str(i): round(values.get(str(i), 0) * 3600, 3)
                   for i in range(1, 6)}
        # Five independently rounded counters can differ by up to 90 seconds.
        # Also require the total to be within 2% of recorded combustion time.
        if abs(sum(seconds.values()) - runtime * 3600) <= min(91, runtime * 72):
            return seconds
    return None


def recover_runtime(event, samples, max_age, current_hours):
    """Return a recorded cumulative combustion reading near the refill."""
    if event.get("runtime_h") is not None:
        return None
    try:
        at = datetime.fromisoformat(event["at"].replace("Z", "+00:00"))
        if at.tzinfo is None:
            return None
    except (KeyError, TypeError, ValueError):
        return None
    for stamp, value in sorted(samples, key=lambda item: item[0], reverse=True):
        if not 0 <= (at - stamp).total_seconds() <= max_age:
            continue
        try:
            hours = float(value)
        except (TypeError, ValueError):
            continue
        if isfinite(hours) and 0 <= hours <= current_hours:
            return hours
    return None


async def async_recover_refills(hass, entry_id, events, max_age, current_hours):
    """Read per-device Recorder history, retaining independently valid fields."""
    if "recorder" not in hass.config.components:
        return {}
    from homeassistant.helpers import entity_registry as er
    from homeassistant.components.recorder import get_instance, history

    registry = er.async_get(hass)
    runtime_id = registry.async_get_entity_id(
        "sensor", "winnet_stove", f"{entry_id}_usage_total"
    )
    power_id = registry.async_get_entity_id(
        "sensor", "winnet_stove", f"{entry_id}_insights_power_profile"
    )
    entity_ids = [entity for entity in (runtime_id, power_id) if entity]
    if not entity_ids:
        return {}
    candidates = [event for event in events if event.get("full_hopper") is True
                  and (event.get("runtime_h") is None or
                       event.get("power_seconds") is None)][-31:]
    recovered = {}
    for event in candidates:
        try:
            at = datetime.fromisoformat(event["at"].replace("Z", "+00:00"))
            if at.tzinfo is None:
                continue
        except (KeyError, TypeError, ValueError):
            continue

        def read_history():
            return history.get_significant_states(
                hass, at - timedelta(seconds=max_age), at + timedelta(microseconds=1),
                entity_ids=entity_ids, include_start_time_state=False,
                significant_changes_only=False, minimal_response=False,
                no_attributes=False,
            )

        result = await get_instance(hass).async_add_executor_job(read_history)
        changes = {}
        runtime = recover_runtime(
            event, [(state.last_updated, state.state)
                    for state in result.get(runtime_id, [])], max_age, current_hours
        )
        if runtime is not None:
            changes.update(runtime_h=runtime, runtime_source="recorder")
        snapshot = recover_snapshot(
            {**event, **changes},
            [(state.last_updated, state.attributes.get("power_hours"))
             for state in result.get(power_id, [])
             if state.state not in ("unknown", "unavailable")], max_age
        )
        if snapshot is not None:
            changes.update(power_seconds=snapshot, power_snapshot_source="recorder")
        if changes:
            recovered[event["id"]] = changes
    return recovered
