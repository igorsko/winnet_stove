# SPDX-License-Identifier: GPL-3.0-only
"""Tests for the pellet maths without requiring a Home Assistant installation."""

from importlib.util import module_from_spec, spec_from_file_location
from math import nan, inf
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location(
    "pellet_logic_for_tests",
    ROOT / "custom_components/winnet_stove/pellet_logic.py",
)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate = MODULE.validate_setting
calculate = MODULE.pellet_stats
DEFAULTS = MODULE.DEFAULT_PELLET


class PelletLogicTest(unittest.TestCase):
    def test_not_configured_means_unknown_consumption(self):
        stats = calculate(7200, dict(DEFAULTS))
        self.assertEqual(stats["total_hours"], 2)
        self.assertIsNone(stats["pellet_used"])
        self.assertIsNone(stats["hours_per_bag"])

    def test_consumption_and_hours_per_bag(self):
        settings = dict(DEFAULTS, initial_hours=2350, rate_kg_h=1.5)
        stats = calculate(4 * 3600, settings)
        self.assertEqual(stats["total_hours"], 2354)
        self.assertEqual(stats["pellet_used"], 6)
        self.assertEqual(stats["estimated_bags"], 0.4)
        self.assertEqual(stats["bags_per_hour"], 0.1)
        self.assertEqual(stats["hours_per_bag"], 10)

    def test_loaded_bags_are_not_assumed_consumed(self):
        settings = dict(DEFAULTS, bags_loaded=10, bags_in_stock=5, rate_kg_h=1)
        stats = calculate(3600, settings)
        self.assertEqual(stats["bags_loaded"], 10)
        self.assertEqual(stats["bags_in_stock"], 5)
        self.assertEqual(stats["pellet_used"], 1)

    def test_no_historical_consumption_inferred(self):
        settings = dict(DEFAULTS, initial_hours=4000, rate_kg_h=2)
        stats = calculate(0, settings)
        self.assertEqual(stats["pellet_used"], 0)
        self.assertEqual(stats["total_hours"], 4000)

    def test_finite_validated_input(self):
        for bad in (nan, inf, -1, True, "not-a-number"):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    validate("initial_hours", bad)

    def test_bags_must_be_nonnegative_whole_numbers(self):
        self.assertEqual(validate("bags_in_stock", 5), 5)
        with self.assertRaises(ValueError):
            validate("bags_in_stock", 2.5)


if __name__ == "__main__":
    unittest.main()
