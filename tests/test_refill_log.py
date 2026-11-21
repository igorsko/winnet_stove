# SPDX-License-Identifier: GPL-3.0-only
"""Pure unit tests for refill history, corrections, and persistence format."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from uuid import uuid4
import unittest

PATH = Path(__file__).resolve().parents[1] / "custom_components/winnet_stove/refill_log.py"
SPEC = spec_from_file_location("refill_log_for_tests", PATH)
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def event(kg=15, source="auto"):
    return {
        "id": str(uuid4()), "at": "2026-11-21T11:00:00+00:00",
        "kg": kg, "source": source, "bag_weight_kg": 15,
        "stock_debit": True,
    }


class RefillLogTests(unittest.TestCase):
    def test_round_trip_preserves_editable_metadata(self):
        initial = [event()]
        restored = MODULE.validate_events(initial)
        self.assertEqual(len(restored), 1)
        self.assertEqual(restored[0]["id"], initial[0]["id"])
        self.assertEqual(restored[0]["kg"], 15)
        self.assertEqual(restored[0]["source"], "auto")
        self.assertTrue(restored[0]["stock_debit"])
        self.assertFalse(restored[0]["full_hopper"])
        self.assertIsNone(restored[0]["runtime_h"])
        self.assertEqual(MODULE.ledger_stats(restored)["total_kg"], 15)
        self.assertEqual(MODULE.ledger_stats(restored)["automatic"], 1)

    def test_manual_correction_and_false_auto_positive(self):
        original = event(source="auto")
        updated = MODULE.update_event([original], original["id"], 7.5)
        self.assertEqual(updated[0]["kg"], 7.5)
        self.assertEqual(updated[0]["source"], "auto")
        self.assertEqual(MODULE.remove_event(updated, original["id"]), [])

    def test_legacy_records_are_not_invented(self):
        self.assertEqual(MODULE.validate_events(None), [])
        self.assertEqual(MODULE.ledger_stats([])["total_kg"], 0)

    def test_duplicates_and_invalid_records_ignored(self):
        initial = event()
        self.assertEqual(len(MODULE.validate_events([initial, initial, {"no": "id"}])), 1)

    def test_input_validation(self):
        for bad in (0, -1, True, "NaN", "Infinity", 501):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    MODULE.valid_kg(bad)
        self.assertEqual(MODULE.valid_kg("7.5"), 7.5)

    def test_cannot_edit_or_delete_nonexistent_event(self):
        with self.assertRaises(ValueError):
            MODULE.update_event([], str(uuid4()), 15)
        with self.assertRaises(ValueError):
            MODULE.remove_event([], str(uuid4()))


if __name__ == "__main__":
    unittest.main()
