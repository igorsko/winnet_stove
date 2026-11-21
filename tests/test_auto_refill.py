# SPDX-License-Identifier: GPL-3.0-only
"""Alarm-to-refill recognition tests; no Home Assistant dependency."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = spec_from_file_location(
    "auto_refill_for_tests",
    ROOT / "custom_components/winnet_stove/auto_refill.py",
)
module = module_from_spec(spec)
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)
Detector = module.AutoRefillDetector


class AutoRefillTest(unittest.TestCase):
    def test_alarm_clear_then_successful_restart_counts_once(self):
        d = Detector()
        self.assertFalse(d.observe(1, 1)[1])  # Alarm raised.
        self.assertFalse(d.observe(2, 1)[1])  # Ignition with latched alarm.
        self.assertFalse(d.observe(3, 0)[1])  # First valid working sample.
        self.assertTrue(d.observe(3, 0)[1])   # Confirmation.
        for _ in range(10):
            self.assertFalse(d.observe(3, 0)[1])
        self.assertFalse(d.pending)

    def test_alarm_clear_alone_is_not_enough(self):
        d = Detector()
        d.observe(3, 1)
        self.assertFalse(d.observe(3, 0)[1])
        self.assertFalse(d.observe(3, 0)[1])

    def test_offline_interrupts_consecutive_working(self):
        d = Detector()
        d.observe(1, 1)
        d.observe(2, 0)
        d.observe(3, 0)
        d.observe(None, None)
        self.assertFalse(d.observe(3, 0)[1])
        self.assertTrue(d.observe(3, 0)[1])

    def test_next_distinct_alarm_can_count_again(self):
        d = Detector()
        for state, code in ((1, 1), (2, 0), (3, 0), (3, 0)):
            first = d.observe(state, code)[1]
        self.assertTrue(first)
        for state, code in ((1, 1), (2, 0), (3, 0), (3, 0)):
            second = d.observe(state, code)[1]
        self.assertTrue(second)

    def test_other_alarm_bits_do_not_trigger(self):
        d = Detector()
        for state, code in ((1, 2), (2, 0), (3, 0), (3, 0)):
            self.assertFalse(d.observe(state, code)[1])

    def test_persistence_keeps_pending_event_and_no_double_count(self):
        d = Detector()
        d.observe(1, 1)
        d.observe(2, 0)
        restored = Detector.restore(d.snapshot())
        self.assertTrue(restored.pending)
        self.assertFalse(restored.observe(3, 0)[1])
        self.assertTrue(restored.observe(3, 0)[1])
        self.assertFalse(Detector.restore(restored.snapshot()).observe(3, 0)[1])

    def test_missing_data_does_not_clear_alarm(self):
        d = Detector()
        d.observe(1, 1)
        d.observe(None, None)
        self.assertFalse(d.observe(3, 1)[1])
        self.assertFalse(d.observe(3, 1)[1])

    def test_toggle_reset_ignores_previous_alarm(self):
        d = Detector()
        d.observe(1, 1)
        d.reset()
        self.assertFalse(d.pending)
        self.assertFalse(d.observe(3, 0)[1])


if __name__ == "__main__":
    unittest.main()
