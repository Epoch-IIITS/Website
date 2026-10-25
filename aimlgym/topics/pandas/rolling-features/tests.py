"""Tests for PD-16 Rolling-Window Features.

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

DF = pd.DataFrame({"store": ["A", "B", "A", "A", "B", "A"],
                   "date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03", "2026-01-02", "2026-01-04"],
                   "sales": [10, 5, 20, 30, 7, 40]})

def nan_list(s):
    return [None if pd.isna(v) else float(v) for v in s]

class TestRolling(unittest.TestCase):
    def test_order(self):
        out = S.add_history_features(DF, 2)
        self.assertEqual(out["store"].tolist(), ["A"] * 4 + ["B"] * 2)
        self.assertEqual(out["sales"].tolist(), [10, 20, 30, 40, 5, 7])

    def test_lag(self):
        self.assertEqual(nan_list(S.add_history_features(DF, 2)["lag1"]), [None, 10, 20, 30, None, 5])

    def test_past_mean(self):
        self.assertEqual(nan_list(S.add_history_features(DF, 2)["past_mean"]), [None, 10, 15, 25, None, 5])

    def test_window3(self):
        self.assertAlmostEqual(S.add_history_features(DF, 3)["past_mean"].iloc[3], 20.0)

    def test_no_leakage(self):
        out = S.add_history_features(DF, 1)
        self.assertTrue((out["past_mean"].dropna() != out["sales"][out["past_mean"].notna()]).all())

    def test_datetime(self):
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(S.add_history_features(DF)["date"]))

    def test_bad_window(self):
        with self.assertRaises(ValueError):
            S.add_history_features(DF, 0)


if __name__ == "__main__":
    unittest.main()
