"""Tests for PD-12 Working with Dates.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


import pandas as pd


def trips():
    return pd.DataFrame({"start": ["2026-02-26", "2024-02-28", "2026-03-09"],
                         "end": ["2026-03-02", "2024-03-01", "2026-03-09"]})


class TestDates(unittest.TestCase):
    def test_manual(self):
        self.assertEqual(S.days_between_manual("2026-02-26", "2026-03-02"), 4)
        self.assertEqual(S.days_between_manual("2024-02-28", "2024-03-01"), 2)

    def test_parse(self):
        df = trips()
        out = S.parse_dates(df, "start")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(out["start"]))
        self.assertTrue(pd.api.types.is_string_dtype(df["start"]))

    def test_parse_rejects_bad_format(self):
        with self.assertRaises((ValueError, TypeError)):
            S.parse_dates(pd.DataFrame({"d": ["03/04/2026"]}), "d")

    def test_parts(self):
        out = S.add_date_parts(S.parse_dates(trips(), "end"), "end")
        self.assertEqual(out["year"].tolist(), [2026, 2024, 2026])
        self.assertEqual(out["month"].tolist(), [3, 3, 3])
        self.assertEqual(out["weekday"].tolist(), ["Monday", "Friday", "Monday"])

    def test_duration_matches_manual(self):
        df = trips()
        out = S.add_duration(df, "start", "end")
        manual = [S.days_between_manual(s, e) for s, e in zip(df["start"], df["end"])]
        self.assertEqual(out["days"].tolist(), manual)
        self.assertEqual(manual, [4, 2, 0])

    def test_in_month(self):
        df = S.parse_dates(trips(), "start")
        out = S.in_month(df, "start", 2026, 3)
        self.assertEqual(len(out), 1)
        self.assertEqual(out.index.tolist(), [0])
        self.assertEqual(len(S.in_month(df, "start", 2026, 2)), 1)


if __name__ == "__main__":
    unittest.main()
