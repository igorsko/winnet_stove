# SPDX-License-Identifier: GPL-3.0-only
"""Pure encoding tests; no network or hardware writes."""

import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "custom_components" / "winnet_stove" / "controls.py"
spec = importlib.util.spec_from_file_location("winnet_controls_test", SOURCE)
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)


class CapturedControlsTest(unittest.TestCase):
    def test_target_read_and_capture_values(self):
        self.assertEqual(controls.read_target({15: 156}), 21.0)
        self.assertEqual(controls.read_target({15: 158}), 21.5)
        self.assertIsNone(controls.read_target({}))
        self.assertEqual(controls.encode_target(21), 156)
        self.assertEqual(controls.encode_target(21.5), 158)

    def test_reject_inferred_or_invalid_setpoints(self):
        for value in (20, 22, 21.25, float("nan"), float("inf"), "", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    controls.encode_target(value)

    def test_levels_are_capture_limited(self):
        self.assertEqual(controls.encode_level("1"), 1)
        self.assertEqual(controls.encode_level("2"), 2)
        for value in (0, 3, 4, 5, "1.5", True, None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    controls.encode_level(value)


if __name__ == "__main__":
    unittest.main()
