# SPDX-License-Identifier: GPL-3.0-only
"""Unit tests of the independent accounting logic."""

from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sys
import unittest

PATH = Path(__file__).resolve().parents[1] / "custom_components/winnet_stove/usage_logic.py"
spec = importlib.util.spec_from_file_location("usage_logic_for_tests", PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
Tracker = module.UsageTracker
NOW = datetime(2026, 11, 21, tzinfo=timezone.utc)


class UsageTests(unittest.TestCase):
    def test_working_time_requires_consecutive_samples(self):
        t = Tracker()
        t.observe(1, 0, NOW, 70)
        t.observe(2, 30, NOW, 70)
        t.observe(3, 60, NOW, 70)
        t.observe(3, 90, NOW, 70)
        self.assertEqual(t.operating_seconds, 30)
        self.assertEqual(t.session_seconds, 60)
        self.assertEqual(t.last_ignition, NOW)

    def test_unknown_state_does_not_count_time(self):
        t = Tracker()
        t.observe(3, 0, NOW, 70)
        t.interrupt()
        t.observe(3, 900, NOW, 70)
        self.assertEqual(t.operating_seconds, 0)

    def test_no_unobserved_ignition_timestamp(self):
        t = Tracker()
        t.observe(3, 100, NOW, 70)
        self.assertIsNone(t.last_ignition)
        self.assertEqual(t.session_seconds, 0)

    def test_long_gap_ignored(self):
        t = Tracker()
        t.observe(3, 0, NOW, 70)
        t.observe(3, 150, NOW, 70)
        self.assertEqual(t.operating_seconds, 0)

    def test_session_resets_after_off(self):
        t = Tracker()
        t.observe(2, 0, NOW, 70)
        t.observe(3, 30, NOW, 70)
        t.observe(1, 60, NOW, 70)
        self.assertEqual(t.session_seconds, 0)

    def test_waiting_program_is_not_active(self):
        t = Tracker()
        t.observe(7, 0, NOW, 70)
        t.observe(3, 30, NOW, 70)
        self.assertEqual(t.last_ignition, NOW)


if __name__ == "__main__":
    unittest.main()
