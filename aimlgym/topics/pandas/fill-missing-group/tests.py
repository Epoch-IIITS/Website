"""Tests for PD-09 Fill Missing Values by Group.

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

DF = pd.DataFrame({"g": list("aabbc"), "v": [1, np.nan, 10, 20, np.nan]})

class TestImpute(unittest.TestCase):
    def test_values(self):
        out = S.impute_group_mean(DF, "g", "v")["v"].tolist()
        np.testing.assert_allclose(out, [1, 1, 10, 20, 31 / 3])

    def test_indicator(self):
        self.assertEqual(S.impute_group_mean(DF, "g", "v")["v_was_missing"].tolist(),
                         [False, True, False, False, True])

    def test_no_nan_left(self):
        self.assertFalse(S.impute_group_mean(DF, "g", "v")["v"].isna().any())

    def test_input_unchanged(self):
        d = DF.copy()
        S.impute_group_mean(d, "g", "v")
        self.assertTrue(np.isnan(d["v"].iloc[1]))

    def test_group_mean_not_global(self):
        d = pd.DataFrame({"g": ["x", "x", "y", "y"], "v": [100, np.nan, 0, np.nan]})
        self.assertEqual(S.impute_group_mean(d, "g", "v")["v"].tolist(), [100, 100, 0, 0])

    def test_all_missing(self):
        with self.assertRaises(ValueError):
            S.impute_group_mean(pd.DataFrame({"g": ["a"], "v": [np.nan]}), "g", "v")

    def test_nothing_missing(self):
        d = pd.DataFrame({"g": ["a", "b"], "v": [1.0, 2.0]})
        pd.testing.assert_series_equal(S.impute_group_mean(d, "g", "v")["v"], d["v"])


if __name__ == "__main__":
    unittest.main()
