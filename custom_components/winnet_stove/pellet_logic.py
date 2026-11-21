# SPDX-License-Identifier: GPL-3.0-only
"""Pure calculation and validation of user-managed pellet data.

No value is read from, or written to, the physical stove.
"""

from math import isfinite

DEFAULT_PELLET = {
    "initial_hours": 0.0,
    "bag_weight_kg": 15.0,
    "rate_kg_h": 0.0,  # Unknown until the user provides an average rate.
    "bags_in_stock": 0,
    "bags_loaded": 0,
}

LIMITS = {
    "initial_hours": (0.0, 10_000_000.0),
    "bag_weight_kg": (1.0, 50.0),
    "rate_kg_h": (0.0, 20.0),
    "bags_in_stock": (0, 100_000),
    "bags_loaded": (0, 100_000_000),
}


def validate_setting(name: str, raw: object) -> float | int:
    """Reject invalid values before persisting any user configuration."""
    if name not in LIMITS or isinstance(raw, bool):
        raise ValueError(f"Invalid pellet setting: {name}")
    try:
        number = float(raw)
    except (ValueError, TypeError, OverflowError) as err:
        raise ValueError(f"Invalid value for {name}") from err
    minimum, maximum = LIMITS[name]
    if not isfinite(number) or not minimum <= number <= maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    if name in ("bags_in_stock", "bags_loaded"):
        if not number.is_integer():
            raise ValueError(f"{name} must be an integer")
        return int(number)
    return number


def pellet_stats(operating_seconds: float, settings: dict) -> dict:
    """Return estimated consumption, independent of manual bag-loading events.

    Only confirmed `working` seconds since installation are used to estimate
    pellet consumption. Historical hours are used for the total-hours display
    but cannot establish historical pellet consumption.
    """
    recorded_hours = max(0.0, float(operating_seconds)) / 3600
    initial = settings["initial_hours"]
    weight = settings["bag_weight_kg"]
    rate = settings["rate_kg_h"]

    stats = {
        "total_hours": round(initial + recorded_hours, 2),
        "bags_loaded": settings["bags_loaded"],
        "bags_in_stock": settings["bags_in_stock"],
        "pellet_used": None,
        "estimated_bags": None,
        "bags_per_hour": None,
        "hours_per_bag": None,
    }
    if rate > 0:
        stats.update({
            "pellet_used": round(recorded_hours * rate, 3),
            "estimated_bags": round(recorded_hours * rate / weight, 3),
            "bags_per_hour": round(rate / weight, 4),
            "hours_per_bag": round(weight / rate, 2),
        })
    return stats
