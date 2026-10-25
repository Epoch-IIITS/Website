"""Tests for PD-15 Binning with pd.cut.

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

class TestBinning(unittest.TestCase):
    def test_groups(self):
        out = S.age_groups([5, 13, 19, 20, 70, -1]).tolist()
        self.assertEqual(out[:5], ["child", "teen", "teen", "adult", "senior"])
        self.assertTrue(pd.isna(out[5]))

    def test_edges_left_closed(self):
        self.assertEqual(S.age_groups([0, 13, 20, 65]).tolist(), ["child", "teen", "adult", "senior"])

    def test_counts(self):
        self.assertEqual(S.group_counts([5, 13, 19, 20, 70, -1]),
                         {"child": 1, "teen": 2, "adult": 1, "senior": 1})

    def test_counts_zeros_and_order(self):
        c = S.group_counts([30])
        self.assertEqual(list(c), ["child", "teen", "adult", "senior"])
        self.assertEqual(c, {"child": 0, "teen": 0, "adult": 1, "senior": 0})

    def test_ordered_categorical(self):
        s = S.age_groups([1, 90])
        self.assertTrue(isinstance(s.dtype, pd.CategoricalDtype) and s.cat.ordered)

    def test_large(self):
        self.assertEqual(S.age_groups([1000]).tolist(), ["senior"])


if __name__ == "__main__":
    unittest.main()
