# SPDX-License-Identifier: GPL-3.0-only
"""Pure refill ledger operations, independent of Home Assistant."""

from datetime import datetime
from math import isfinite
from uuid import UUID

MAX_ENTRIES = 5000
MAX_KG = 500.0


def valid_kg(value: object) -> float:
    """Require a finite, positive quantity measured in kilograms."""
    if isinstance(value, bool):
        raise ValueError("Quantity must be a number")
    try:
        kg = float(value)
    except (ValueError, TypeError, OverflowError) as err:
        raise ValueError("Quantity must be a number") from err
    if not isfinite(kg) or not 0.001 <= kg <= MAX_KG:
        raise ValueError("Quantity must be between 0.001 and 500 kg")
    return round(kg, 3)


def validate_events(value: object) -> list[dict]:
    """Restore only well-formed persisted entries; ignore invalid records."""
    if not isinstance(value, list):
        return []
    validated = []
    seen = set()
    for event in value[-MAX_ENTRIES:]:
        if not isinstance(event, dict):
            continue
        try:
            event_id = str(UUID(str(event["id"])))
            kg = valid_kg(event["kg"])
            stamp = str(event["at"])
            datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            source = event["source"]
            if source not in ("manual", "auto") or event_id in seen:
                continue
            bag_weight = valid_kg(event.get("bag_weight_kg", 15.0))
        except (KeyError, ValueError, TypeError):
            continue
        debit = event.get("stock_debit", False) is True
        validated.append({
            "id": event_id, "at": stamp, "kg": kg,
            "bag_weight_kg": bag_weight, "stock_debit": debit, "source": source,
            "full_hopper": event.get("full_hopper") is True,
            "runtime_h": event.get("runtime_h") if isinstance(event.get("runtime_h"), (int, float)) and 0 <= event.get("runtime_h") <= 1e8 else None,
        })
        seen.add(event_id)
    return validated


def update_event(events: list[dict], event_id: str, kg: object) -> list[dict]:
    """Replace quantity for one existing event without changing its identity."""
    updated = []
    found = False
    for event in events:
        if event["id"] == event_id:
            updated.append({**event, "kg": valid_kg(kg)})
            found = True
        else:
            updated.append(event)
    if not found:
        raise ValueError("Refill event not found")
    return updated


def remove_event(events: list[dict], event_id: str) -> list[dict]:
    """Delete a mistaken record; never modify unrelated entries."""
    filtered = [event for event in events if event["id"] != event_id]
    if len(filtered) == len(events):
        raise ValueError("Refill event not found")
    return filtered


def ledger_stats(events: list[dict]) -> dict:
    """Only the new ledger is in kg; old bag counts have unknown weights."""
    return {
        "count": len(events),
        "total_kg": round(sum(e["kg"] for e in events), 3),
        "automatic": sum(e["source"] == "auto" for e in events),
        "manual": sum(e["source"] == "manual" for e in events),
    }
