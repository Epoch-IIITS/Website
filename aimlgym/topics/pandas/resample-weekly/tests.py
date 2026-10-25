"""Tests for PD-13 Weekly Resampling.

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


import numpy as np
import pandas as pd

DF = pd.DataFrame({"date": ["2026-01-05", "2026-01-11", "2026-01-12", "2026-01-26"],
                   "amount": [10, 5, 7, 1]})

class TestResample(unittest.TestCase):
    def test_index(self):
        idx = S.weekly_summary(DF).index
        self.assertEqual([d.strftime("%Y-%m-%d") for d in idx],
                         ["2026-01-11", "2026-01-18", "2026-01-25", "2026-02-01"])
        self.assertEqual(idx.name, "date")

    def test_totals(self):
        self.assertEqual(S.weekly_summary(DF)["total"].tolist(), [15, 7, 0, 1])

    def test_counts(self):
        self.assertEqual(S.weekly_summary(DF)["n"].tolist(), [2, 1, 0, 1])

    def test_mean_nan_empty(self):
        m = S.weekly_summary(DF)["mean"]
        self.assertAlmostEqual(m.iloc[0], 7.5)
        self.assertTrue(np.isnan(m.iloc[2]))

    def test_unsorted_input(self):
        out = S.weekly_summary(DF.iloc[::-1].reset_index(drop=True))
        self.assertEqual(out["total"].tolist(), [15, 7, 0, 1])

    def test_sunday_belongs_to_its_week(self):
        out = S.weekly_summary(pd.DataFrame({"date": ["2026-01-11"], "amount": [3]}))
        self.assertEqual(out.index[0].strftime("%Y-%m-%d"), "2026-01-11")

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.weekly_summary(pd.DataFrame({"date": [], "amount": []}))


if __name__ == "__main__":
    unittest.main()
