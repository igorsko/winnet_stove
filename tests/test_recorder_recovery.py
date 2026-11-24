# SPDX-License-Identifier: GPL-3.0-only
"""Test conservative recovery without importing Home Assistant."""
import importlib.util
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "recorder_recovery", Path(__file__).resolve().parents[1]
    / "custom_components/winnet_stove/recorder_recovery.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.at = datetime(2026, 11, 24, tzinfo=timezone.utc)
        self.event = {"at": self.at.isoformat(), "runtime_h": 10,
                      "power_seconds": None}
        self.values = {"1": 4, "2": 6}

    def test_valid_snapshot(self):
        result = module.recover_snapshot(
            self.event, [(self.at - timedelta(seconds=10), self.values)], 70)
        self.assertEqual(result["1"], 14400)
        self.assertEqual(result["2"], 21600)
        self.assertEqual(result["5"], 0)

    def test_reject_stale_future_missing_and_incomplete(self):
        for samples in ([], [(self.at - timedelta(seconds=71), self.values)],
                        [(self.at + timedelta(seconds=1), self.values)],
                        [(self.at, {"1": 4})],
                        [(self.at, {"1": 4, "9": 6})]):
            with self.subTest(samples=samples):
                self.assertIsNone(module.recover_snapshot(self.event, samples, 70))

    def test_preserve_native_snapshot(self):
        self.event["power_seconds"] = {"1": 36000}
        self.assertIsNone(module.recover_snapshot(
            self.event, [(self.at, self.values)], 70))

    def test_rounding(self):
        result = module.recover_snapshot(
            self.event, [(self.at, {"1": 4.01, "2": 6})], 70)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
