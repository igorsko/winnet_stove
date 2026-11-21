# SPDX-License-Identifier: GPL-3.0-only
"""Pure, testable WiNET stove runtime accounting."""

from dataclasses import dataclass
from datetime import datetime

ACTIVE_STATES = frozenset((2, 3, 4, 5, 8, 9))
OFF_STATES = frozenset((1, 6, 7))


@dataclass
class UsageTracker:
    """Accumulate only intervals supported by consecutive valid observations."""

    operating_seconds: float = 0.0
    session_seconds: float = 0.0
    last_ignition: datetime | None = None
    _previous_state: int | None = None
    _previous_sample: float | None = None

    def observe(
        self, state: int | None, elapsed: float, wall_time: datetime, max_gap: float
    ) -> bool:
        """Update totals; unknown/offline readings interrupt observation."""
        if state not in ACTIVE_STATES | OFF_STATES:
            self._previous_state = None
            self._previous_sample = None
            return False

        changed = False
        was_active = self._previous_state in ACTIVE_STATES
        is_active = state in ACTIVE_STATES

        if self._previous_state in OFF_STATES and is_active:
            self.session_seconds = 0.0
            self.last_ignition = wall_time
            changed = True
        elif self._previous_state is None and is_active:
            # Start measuring from first observed active sample, not an invented
            # ignition time. Previous session information is not reused.
            self.session_seconds = 0.0
            changed = True

        if was_active and is_active and self._previous_sample is not None:
            delta = elapsed - self._previous_sample
            if 0 <= delta <= max_gap:
                self.session_seconds += delta
                if self._previous_state == 3 and state == 3:
                    self.operating_seconds += delta
                changed = changed or delta > 0

        if not is_active and was_active:
            self.session_seconds = 0.0
            changed = True

        self._previous_state = state
        self._previous_sample = elapsed
        return changed

    def interrupt(self) -> None:
        """Do not bridge periods of unknown connectivity."""
        self._previous_state = None
        self._previous_sample = None
