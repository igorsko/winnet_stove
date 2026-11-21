# SPDX-License-Identifier: GPL-3.0-only
"""Pure statistics for calibrated pellet consumption and maintenance.

All results are estimates. Full-to-full calibration requires user confirmation
that the hopper was returned to the same full level on both occasions.
"""

from datetime import datetime
from math import isfinite

MAINTENANCE_DEFAULTS = {
    "burner": 12.0,
    "deep_clean": 100.0,
    "annual_service": 1000.0,
}
MAX_DAILY_HISTORY = 400


def valid_positive(value, maximum=100_000.0):
    if isinstance(value, bool):
        raise ValueError("Invalid number")
    try:
        value = float(value)
    except (ValueError, TypeError, OverflowError) as err:
        raise ValueError("Invalid number") from err
    if not isfinite(value) or not 0 < value <= maximum:
        raise ValueError("Value must be positive, finite and within range")
    return value


def calibrated_rate(refills):
    """Infer average kg/h from the two latest full-hopper confirmations.

    Include all top-ups after the first full event, including the pellet needed
    to return the tank to full at the second. Do not guess missing observations.
    """
    full = [(i, e) for i, e in enumerate(refills)
            if e.get("full_hopper") is True
            and isinstance(e.get("runtime_h"), (int, float))
            and isfinite(e["runtime_h"])]
    if len(full) < 2:
        return None
    (left_i, left), (right_i, right) = full[-2:]
    hours = right["runtime_h"] - left["runtime_h"]
    if hours <= 0:
        return None
    mass = sum(e["kg"] for e in refills[left_i + 1:right_i + 1])
    if mass <= 0 or not isfinite(mass):
        return None
    rate = mass / hours
    # Rates outside plausible bounds likely imply bad refill or uptime data.
    if not 0.05 <= rate <= 10:
        return None
    return round(rate, 4)


def effective_rate(manual_rate, refills):
    """Prefer a learned rate, otherwise use a user-configured rate."""
    learned = calibrated_rate(refills)
    if learned is not None:
        return learned, "full_hopper_calibration"
    if manual_rate > 0:
        return manual_rate, "user_average"
    return None, "unconfigured"


def maintenance_remaining(total_hours, last_reset_hours, threshold_hours):
    """Hours until the next due service; negative means overdue."""
    return round(threshold_hours - max(0.0, total_hours - last_reset_hours), 2)


def daily_estimates(daily_working_seconds, rate, bag_weight_kg, price_per_bag):
    """Compute estimates per UTC/HA-local date from observed working time."""
    output = []
    for day, seconds in sorted(daily_working_seconds.items())[-MAX_DAILY_HISTORY:]:
        if not isinstance(day, str) or not isinstance(seconds, (int, float)):
            continue
        try:
            datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            continue
        if not isfinite(seconds) or seconds < 0:
            continue
        kg = round(seconds / 3600 * rate, 3) if rate is not None else None
        cost = round(kg / bag_weight_kg * price_per_bag, 2) if kg is not None and price_per_bag > 0 else None
        output.append({"date": day, "working_h": round(seconds / 3600, 3),
                       "estimated_kg": kg, "estimated_cost": cost})
    return output

def profile_consumption(power_seconds: dict, rate_by_power: dict):
    """Estimate total pellet only when each observed power has a valid rate.

    Raw controller power levels are treated as opaque labels. Unconfigured
    or unknown levels make the result unavailable instead of extrapolated.
    """
    if not power_seconds:
        return None
    total = 0.0
    for level, seconds in power_seconds.items():
        if seconds <= 0:
            continue
        rate = rate_by_power.get(str(level))
        if not isinstance(rate, (int, float)) or not isfinite(rate) or rate <= 0:
            return None
        total += seconds / 3600 * rate
    return round(total, 3)
