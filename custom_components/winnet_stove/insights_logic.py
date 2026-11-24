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


def _solve_system(matrix, values):
    """Small pivoted Gaussian elimination; reject rank-deficient calibrations."""
    n = len(values)
    a = [list(row) + [values[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-7:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        for index in range(col, n + 1):
            a[col][index] /= divisor
        for row in range(n):
            if row == col:
                continue
            coefficient = a[row][col]
            for index in range(col, n + 1):
                a[row][index] -= coefficient * a[col][index]
    return [a[i][-1] for i in range(n)]


def learned_power_profile(refills):
    """Infer independent kg/h power rates from full-to-full cycles.

    Do not invent per-level rates when snapshots are missing, power coverage
    is incomplete, or the observed cycles cannot identify the separate levels.
    All historical power snapshots are cumulative working seconds.
    """
    full = [
        (i, event) for i, event in enumerate(refills)
        if event.get("full_hopper") is True
    ]
    rows = []
    for (left_i, left), (right_i, right) in zip(full, full[1:]):
        start, end = left.get("power_seconds"), right.get("power_seconds")
        h1, h2 = left.get("runtime_h"), right.get("runtime_h")
        if not isinstance(start, dict) or not isinstance(end, dict):
            continue
        if not isinstance(h1, (int, float)) or not isinstance(h2, (int, float)):
            continue
        if not all(isfinite(v) for v in (h1, h2)) or h2 <= h1:
            continue
        hours = (h2 - h1)
        if hours < 0.5:
            continue
        levels = {}
        valid = True
        for level in ("1", "2", "3", "4", "5"):
            before, after = start.get(level, 0), end.get(level, 0)
            if not (isinstance(before, (int, float))
                    and isinstance(after, (int, float))
                    and all(isfinite(v) for v in (before, after))
                    and after >= before >= 0):
                valid = False
                break
            levels[level] = (after - before) / 3600
        observed = sum(levels.values())
        if not valid or not 0.98 * hours <= observed <= 1.02 * hours:
            continue
        mass = sum(entry["kg"] for entry in refills[left_i + 1:right_i + 1])
        if not isfinite(mass) or not 0.05 <= mass / hours <= 5:
            continue
        rows.append((levels, mass))
    rows = rows[-30:]
    active = [level for level in ("1", "2", "3", "4", "5")
              if any(row[0][level] > 0 for row in rows)]
    result = {"rates": {}, "cycles": len(rows), "levels": active,
              "status": "collecting", "relative_error": None}
    # At least two cycles, and at least one independent equation per unknown.
    if len(rows) < max(2, len(active)) or not active:
        return result
    matrix = [[sum(r[0][a] * r[0][b] for r in rows)
               for b in active] for a in active]
    values = [sum(r[0][a] * r[1] for r in rows) for a in active]
    rates = _solve_system(matrix, values)
    if rates is None or not all(isfinite(rate) and 0.05 <= rate <= 5
                                  for rate in rates):
        result["status"] = "insufficient_variation"
        return result
    max_error = max(abs(sum(hrs[level] * rate
                            for level, rate in zip(active, rates)) - kg)
                    / kg for hrs, kg in rows)
    if max_error > 0.25:
        result["status"] = "inconsistent_refills"
        result["relative_error"] = round(max_error, 3)
        return result
    result.update({"rates": dict(zip(active, [round(x, 4) for x in rates])),
                   "status": "learned",
                   "relative_error": round(max_error, 3)})
    return result

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
