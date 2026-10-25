"""Tests for XA-02 Ranking Attributions.

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

N = ["age", "income", "debt"]

class TestTopAttr(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.top_attributions(N, np.array([0.5, -2.0, 1.5]), k=2),
                         [("income", -2.0, "-", 0.5), ("debt", 1.5, "+", 0.375)])

    def test_shares_sum(self):
        r = S.top_attributions(N, np.array([0.5, -2.0, 1.5]), k=3)
        self.assertAlmostEqual(sum(t[3] for t in r), 1.0)

    def test_ties_alphabetical(self):
        r = S.top_attributions(["b", "a", "c"], np.array([1.0, -1.0, 0.5]))
        self.assertEqual([t[0] for t in r], ["a", "b", "c"])

    def test_zero(self):
        r = S.top_attributions(["x", "y"], np.array([0.0, 0.0]))
        self.assertEqual(r, [("x", 0.0, "0", 0.0), ("y", 0.0, "0", 0.0)])

    def test_k_larger(self):
        self.assertEqual(len(S.top_attributions(N, np.array([1., 2., 3.]), k=10)), 3)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.top_attributions(N, np.array([1.0]))
        with self.assertRaises(ValueError):
            S.top_attributions(N, np.ones(3), k=0)


if __name__ == "__main__":
    unittest.main()
