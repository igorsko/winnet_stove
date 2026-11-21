# SPDX-License-Identifier: GPL-3.0-only
"""Unit tests for calibration, costs, accounting, and maintenance."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from uuid import uuid4
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location(
    "insights_logic_for_tests",
    ROOT / "custom_components/winnet_stove/insights_logic.py",
)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def refill(kg, runtime_h, full=False):
    return {
        "id": str(uuid4()),
        "kg": kg,
        "runtime_h": runtime_h,
        "full_hopper": full,
        "source": "manual",
    }


class InsightsTests(unittest.TestCase):
    def test_no_calibration_without_two_full_hoppers(self):
        self.assertIsNone(MODULE.calibrated_rate([]))
        self.assertIsNone(MODULE.calibrated_rate([refill(15, 10, True)]))
        rate, source = MODULE.effective_rate(1.2, [])
        self.assertEqual((rate, source), (1.2, "user_average"))

    def test_two_full_hoppers_and_partial_topups(self):
        entries = [
            refill(15, 10, True),
            refill(5, 15, False),
            refill(10, 20, True),
        ]
        # In 10 confirmed hours, 5 + 10 kg entered since previous full.
        self.assertEqual(MODULE.calibrated_rate(entries), 1.5)
        self.assertEqual(MODULE.effective_rate(2, entries),
                         (1.5, "full_hopper_calibration"))

    def test_ignores_invalid_run_intervals(self):
        entries = [refill(15, 10, True), refill(15, 10, True)]
        self.assertIsNone(MODULE.calibrated_rate(entries))
        entries[1]["runtime_h"] = 9
        self.assertIsNone(MODULE.calibrated_rate(entries))

    def test_maintenance_hours(self):
        self.assertEqual(MODULE.maintenance_remaining(30, 20, 12), 2)
        self.assertEqual(MODULE.maintenance_remaining(35, 20, 12), -3)

    def test_daily_costs_require_known_price_and_rate(self):
        days = {"2026-11-21": 7200.0}
        rows = MODULE.daily_estimates(days, 1.5, 15, 7.5)
        self.assertEqual(rows[0]["estimated_kg"], 3)
        self.assertEqual(rows[0]["estimated_cost"], 1.5)
        self.assertIsNone(MODULE.daily_estimates(days, None, 15, 7.5)[0]["estimated_kg"])
        self.assertIsNone(MODULE.daily_estimates(days, 1.5, 15, 0)[0]["estimated_cost"])

    def test_power_profile_does_not_invent_unconfigured_rates(self):
        self.assertEqual(
            MODULE.profile_consumption({"1": 3600, "2": 7200}, {"1": 1.0, "2": 1.5}),
            4,
        )
        self.assertIsNone(
            MODULE.profile_consumption({"1": 3600, "9": 7200}, {"1": 1.0})
        )

    def test_invalid_threshold(self):
        for bad in (-1, 0, "NaN", True):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                MODULE.valid_positive(bad)


if __name__ == "__main__":
    unittest.main()
