"""Tests for PD-06 Finding and Handling Missing Values.

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


def frame():
    return pd.DataFrame({"age": [20, None, 31, np.nan], "city": ["A", "B", None, "D"],
                         "score": [1.0, 2.0, 3.0, 4.0]})


class TestMissing(unittest.TestCase):
    def test_report(self):
        self.assertEqual(S.missing_report(frame()), {"age": 2, "city": 1, "score": 0})

    def test_drop_subset(self):
        out = S.drop_incomplete(frame(), ["age"])
        self.assertEqual(out["age"].tolist(), [20.0, 31.0])
        self.assertEqual(out.index.tolist(), [0, 1])

    def test_drop_two_columns(self):
        out = S.drop_incomplete(frame(), ["age", "city"])
        self.assertEqual(out["age"].tolist(), [20.0])

    def test_fill_defaults(self):
        df = frame()
        out = S.fill_defaults(df, {"age": 0, "city": "unknown"})
        self.assertEqual(out["age"].tolist(), [20.0, 0.0, 31.0, 0.0])
        self.assertEqual(out["city"].tolist(), ["A", "B", "unknown", "D"])
        self.assertEqual(int(df["age"].isna().sum()), 2)

    def test_manual_mean(self):
        self.assertEqual(S.mean_skipping_missing([20, None, 31, float("nan")]), 25.5)
        self.assertIsNone(S.mean_skipping_missing([None, float("nan")]))

    def test_manual_matches_pandas(self):
        values = [3.5, None, -1.0, float("nan"), 10.0]
        self.assertAlmostEqual(S.mean_skipping_missing(values), pd.Series(values, dtype=float).mean())


if __name__ == "__main__":
    unittest.main()
