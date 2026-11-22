# SPDX-License-Identifier: GPL-3.0-only
"""Conservative, capture-verified experimental WiNET control encoding.

Observed on one Thermorossi Slimquadro 9 Evo on 2026-11-22.
Only register values 156/158 and levels 1/2 have been verified.
Do not broaden without additional capture evidence and hardware testing.
"""

import math

TARGET_REGISTER = 15
POWER_REGISTER = 12
FAN_REGISTER = 13

# These two settings and levels were actually observed in the supplied PCAP.
TARGET_VALUES = {21.0: 156, 21.5: 158}
LEVEL_VALUES = (1, 2)


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
    if not math.isfinite(numeric) or numeric not in TARGET_VALUES:
        raise ValueError("Only captured target temperatures 21.0 and 21.5 °C are enabled")
    return TARGET_VALUES[numeric]


def encode_level(value):
    """Only levels 1 and 2 were captured for both fan and power."""
    if isinstance(value, bool):
        raise ValueError("A level must be an integer")
    try:
        number = int(value)
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid control level") from err
    if str(value) not in ("1", "2") and value not in LEVEL_VALUES:
        raise ValueError("Only captured levels 1 and 2 are enabled")
    if number not in LEVEL_VALUES:
        raise ValueError("Only captured levels 1 and 2 are enabled")
    return number
