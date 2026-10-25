"""Tests for PD-14 Pivot Tables.

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

DF = pd.DataFrame({"region": ["N", "N", "S", "N"], "quarter": ["Q1", "Q2", "Q1", "Q1"],
                   "sales": [5, 3, 7, 2]})

class TestPivot(unittest.TestCase):
    def test_values(self):
        w = S.sales_pivot(DF)
        self.assertEqual(w.loc["N", "Q1"], 7)
        self.assertEqual(w.loc["S", "Q2"], 0)

    def test_axes(self):
        w = S.sales_pivot(DF)
        self.assertEqual(list(w.index), ["N", "S"])
        self.assertEqual(list(w.columns), ["Q1", "Q2"])
        self.assertIsNone(w.columns.name)

    def test_int_dtype(self):
        self.assertTrue(pd.api.types.is_integer_dtype(S.sales_pivot(DF)["Q2"]))

    def test_sorted_columns(self):
        d = pd.DataFrame({"region": ["A", "A"], "quarter": ["Q4", "Q1"], "sales": [1, 2]})
        self.assertEqual(list(S.sales_pivot(d).columns), ["Q1", "Q4"])

    def test_long(self):
        long = S.to_long(S.sales_pivot(DF))
        self.assertEqual(list(long.columns), ["region", "quarter", "sales"])
        self.assertEqual(long.values.tolist(), [["N", "Q1", 7], ["N", "Q2", 3], ["S", "Q1", 7], ["S", "Q2", 0]])

    def test_total_preserved(self):
        self.assertEqual(int(S.to_long(S.sales_pivot(DF))["sales"].sum()), int(DF["sales"].sum()))


if __name__ == "__main__":
    unittest.main()
