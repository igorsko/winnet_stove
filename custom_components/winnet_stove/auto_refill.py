# SPDX-License-Identifier: GPL-3.0-only
"""Conservative, persistent detection of pellet-refill evidence.

WiNET alarm bit 0 means "NO PELLET / CLEAN BURNER", so a refill inferred
from this bit is not confirmed. The feature must be explicitly opted into.
"""

from dataclasses import dataclass

# WiNET state 1 = off, 2 = starting, 7 = waiting, 8 = stopping.
RESTART_STATES = frozenset((1, 2, 7, 8))
WORKING_STATE = 3
NO_PELLET_OR_CLEAN_BURNER_BIT = 1 << 0


@dataclass
class AutoRefillDetector:
    """One refill per observed alarm episode after a confirmed restart."""

    pending: bool = False
    restart_seen: bool = False
    alarm_cleared: bool = False
    working_samples: int = 0
    last_alarm: bool | None = None

    def reset(self) -> None:
        """Discard an old candidate when the setting is toggled."""
        self.pending = False
        self.restart_seen = False
        self.alarm_cleared = False
        self.working_samples = 0
        self.last_alarm = None

    def observe(self, state: int | None, alarm_code: int | None) -> tuple[bool, bool]:
        """Return (persist_state, inferred_refill).

        Missing/offline data must never complete a refill. After an alarm,
        require an observed off/starting phase and then two separate polls
        in the working state with the alarm cleared.
        """
        if state is None or alarm_code is None:
            self.working_samples = 0
            return False, False

        alarm = bool(alarm_code & NO_PELLET_OR_CLEAN_BURNER_BIT)
        changed = False

        if alarm and self.last_alarm is not True and not self.pending:
            self.pending = True
            self.restart_seen = False
            self.alarm_cleared = False
            self.working_samples = 0
            changed = True

        if self.last_alarm is not alarm:
            self.last_alarm = alarm
            changed = True

        if not self.pending:
            return changed, False

        if state in RESTART_STATES and not self.restart_seen:
            self.restart_seen = True
            changed = True

        if not alarm and not self.alarm_cleared:
            self.alarm_cleared = True
            changed = True

        if self.restart_seen and self.alarm_cleared and not alarm and state == WORKING_STATE:
            self.working_samples += 1
            if self.working_samples >= 2:
                self.pending = False
                self.restart_seen = False
                self.alarm_cleared = False
                self.working_samples = 0
                return True, True
        elif self.working_samples:
            self.working_samples = 0
            changed = True

        return changed, False

    def snapshot(self) -> dict:
        """Persist meaningful progress across reloads."""
        return {
            "pending": self.pending,
            "restart_seen": self.restart_seen,
            "alarm_cleared": self.alarm_cleared,
            "last_alarm": self.last_alarm,
            # Never trust a half-confirmed running streak after a restart.
        }

    @classmethod
    def restore(cls, value: object) -> "AutoRefillDetector":
        if not isinstance(value, dict):
            return cls()
        fields = ("pending", "restart_seen", "alarm_cleared")
        if any(type(value.get(name)) is not bool for name in fields):
            return cls()
        last_alarm = value.get("last_alarm")
        if last_alarm is not None and type(last_alarm) is not bool:
            return cls()
        return cls(
            pending=value["pending"],
            restart_seen=value["restart_seen"],
            alarm_cleared=value["alarm_cleared"],
            last_alarm=last_alarm,
        )
