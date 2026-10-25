"""Tests for PD-02 Build and Describe a DataFrame.

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

D = {"name": ["ann", "bob"], "score": [91.5, 78.0], "year": [1, 2]}

class TestBasics(unittest.TestCase):
    def test_make(self):
        df = S.make_df(D)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df["score"].tolist(), [91.5, 78.0])

    def test_describe(self):
        self.assertEqual(S.describe_df(S.make_df(D)),
                         {"n_rows": 2, "n_cols": 3, "columns": ["name", "score", "year"],
                          "numeric": ["score", "year"]})

    def test_unequal(self):
        with self.assertRaises(ValueError):
            S.make_df({"a": [1, 2], "b": [1]})

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.make_df({})

    def test_no_numeric(self):
        self.assertEqual(S.describe_df(S.make_df({"x": ["a", "b"]}))["numeric"], [])

    def test_bool_not_numeric(self):
        d = S.describe_df(S.make_df({"flag": [True, False], "v": [1, 2]}))
        self.assertEqual(d["numeric"], ["v"])


if __name__ == "__main__":
    unittest.main()
