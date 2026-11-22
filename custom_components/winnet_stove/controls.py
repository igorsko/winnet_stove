# SPDX-License-Identifier: GPL-3.0-only
"""Consumer-facing WiNET controls with conservative firmware pilot limits.

Observed on one Thermorossi Slimquadro 9 Evo on 2026-11-22.
Register mapping and first two levels verified in capture and a local test.
Remaining levels and temperatures are inferred; verify on the physical stove.
"""

import math

TARGET_REGISTER = 15
POWER_REGISTER = 12
FAN_REGISTER = 13

# Initial pilot range: narrower than third-party WiNET documentation (5–40 °C).
# Encoding matches captured 21.0 -> 156 and 21.5 -> 158.
MIN_TARGET = 15.0
MAX_TARGET = 30.0
TARGET_STEP = 0.5
LEVEL_VALUES = tuple(range(1, 6))


def read_target(registers):
    """Decode the same register 15 used by the cloud (category 1)."""
    raw = registers.get(TARGET_REGISTER)
    return None if raw is None else (int(raw) / 4.0) - 18.0


def encode_target(value):
    """Return only a captured raw setpoint, never an inferred write."""
    try:
        numeric = float(value)
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid target temperature") from err
    if (not math.isfinite(numeric) or numeric < MIN_TARGET or numeric > MAX_TARGET
            or not (numeric * 2).is_integer()):
        raise ValueError("Target must be 15–30 °C in 0.5 °C steps")
    return int(round((numeric + 18.0) * 4))


def encode_level(value):
    """Levels 1–5 are documented user-facing settings; first two tested locally."""
    if isinstance(value, bool):
        raise ValueError("A level must be an integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid control level") from err
    if str(value) not in ("1", "2", "3", "4", "5") and value not in LEVEL_VALUES:
        raise ValueError("Levels must be 1–5")
    if number not in LEVEL_VALUES:
        raise ValueError("Only captured levels 1 and 2 are enabled")
    return number
