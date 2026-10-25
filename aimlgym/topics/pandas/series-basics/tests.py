"""Tests for PD-01 Series: Labelled Columns.

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


from collections import Counter

import pandas as pd


class TestSeries(unittest.TestCase):
    def setUp(self):
        self.s = S.make_series({"apple": 1.2, "pear": 0.8, "fig": 2.5})

    def test_make_series(self):
        self.assertIsInstance(self.s, pd.Series)
        self.assertEqual(self.s["pear"], 0.8)
        self.assertEqual(str(self.s.dtype), "float64")
        self.assertEqual(self.s.index.tolist(), ["apple", "pear", "fig"])

    def test_add_aligned(self):
        a = pd.Series({"y": 2.0, "x": 1.0})
        b = pd.Series({"y": 10.0, "z": 5.0})
        out = S.add_aligned(a, b)
        self.assertEqual(out.to_dict(), {"x": 1.0, "y": 12.0, "z": 5.0})
        self.assertEqual(out.index.tolist(), ["x", "y", "z"])

    def test_add_matches_dict_version(self):
        a = {"p": 1.0, "q": 4.0}
        b = {"q": 0.5, "r": -2.0}
        manual = {k: a.get(k, 0) + b.get(k, 0) for k in sorted(a.keys() | b.keys())}
        self.assertEqual(S.add_aligned(pd.Series(a), pd.Series(b)).to_dict(), manual)

    def test_above_mean(self):
        self.assertEqual(S.above_mean(self.s), ["fig"])
        self.assertEqual(S.above_mean(pd.Series({"a": 1.0, "b": 1.0})), [])

    def test_top_labels(self):
        self.assertEqual(S.top_labels(self.s, 2), ["fig", "apple"])
        self.assertEqual(S.top_labels(self.s, 1), ["fig"])

    def test_count_values(self):
        items = ["a", "b", "a", "c", "a", "b"]
        out = S.count_values(items)
        self.assertEqual(out, dict(Counter(items)))
        self.assertTrue(all(type(v) is int for v in out.values()))


if __name__ == "__main__":
    unittest.main()
