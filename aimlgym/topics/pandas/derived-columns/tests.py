"""Tests for PD-05 Derived Columns.

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

DF = pd.DataFrame({"a": [30, 10, 0], "b": [20, 0, 0]})

class TestFeatures(unittest.TestCase):
    def test_total(self):
        self.assertEqual(S.add_features(DF)["total"].tolist(), [50, 10, 0])

    def test_ratio_nan(self):
        r = S.add_features(DF)["ratio"]
        self.assertAlmostEqual(r.iloc[0], 1.5)
        self.assertTrue(np.isnan(r.iloc[1]) and np.isnan(r.iloc[2]))

    def test_no_inf(self):
        self.assertFalse(np.isinf(S.add_features(DF)["ratio"].to_numpy(dtype=float)).any())

    def test_passed(self):
        self.assertEqual(S.add_features(DF)["passed"].tolist(), [True, False, False])

    def test_columns(self):
        self.assertEqual(list(S.add_features(DF).columns), ["a", "b", "total", "ratio", "passed"])

    def test_not_mutated(self):
        d = DF.copy()
        S.add_features(d)
        self.assertEqual(list(d.columns), ["a", "b"])

    def test_negative_b(self):
        out = S.add_features(pd.DataFrame({"a": [6], "b": [-3]}))
        self.assertAlmostEqual(out["ratio"].iloc[0], -2.0)


if __name__ == "__main__":
    unittest.main()
