"""Tests for PD-04 Select and Filter Rows.

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

DF = pd.DataFrame({"name": ["ann", "bob", "cy", "dee"], "city": ["Pune", "Delhi", "Pune", "Chennai"],
                   "score": [72, 90, 55, 61]})

class TestFilter(unittest.TestCase):
    def test_example(self):
        out = S.filter_students(DF, 60, ["Pune", "Chennai"], ["name", "score"])
        pd.testing.assert_frame_equal(out, pd.DataFrame({"name": ["ann", "dee"], "score": [72, 61]}),
                                      check_dtype=False)

    def test_inclusive(self):
        self.assertEqual(S.filter_students(DF, 61, ["Chennai"], ["name"])["name"].tolist(), ["dee"])

    def test_none(self):
        out = S.filter_students(DF, 100, ["Pune"], ["name"])
        self.assertEqual(len(out), 0)
        self.assertEqual(list(out.columns), ["name"])

    def test_index_reset(self):
        out = S.filter_students(DF, 0, ["Pune"], ["name"])
        self.assertEqual(list(out.index), [0, 1])

    def test_column_order(self):
        out = S.filter_students(DF, 0, ["Delhi"], ["score", "name"])
        self.assertEqual(list(out.columns), ["score", "name"])

    def test_input_unchanged(self):
        before = DF.copy()
        S.filter_students(DF, 60, ["Pune"], ["name"])
        pd.testing.assert_frame_equal(DF, before)

    def test_missing_col(self):
        with self.assertRaises(KeyError):
            S.filter_students(DF, 0, ["Pune"], ["age"])


if __name__ == "__main__":
    unittest.main()
