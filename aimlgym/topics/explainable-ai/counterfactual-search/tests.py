"""Tests for XA-13 Minimal Counterfactual Search.

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

P = lambda X: (X[:, 0] + 2 * X[:, 1] >= 10).astype(int)

class TestCF(unittest.TestCase):
    def test_example(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 1.]))
        np.testing.assert_allclose(r["x_cf"], [4., 3.])
        self.assertEqual((r["k"], r["cost"], int(r["label"])), ((0, 1), 1, 1))

    def test_immutable(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 0.]))
        self.assertEqual(r["k"], (2, 0))

    def test_none(self):
        self.assertIsNone(S.find_counterfactual(P, np.array([0., 0.]), np.array([1., 1.]), max_steps=2))

    def test_bounds(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 1.]), upper=np.array([100., 2.]))
        self.assertEqual(r["k"], (2, 0))

    def test_minimal_cost(self):
        f = lambda X: (X[:, 0] * X[:, 1] > 6).astype(int)
        r = S.find_counterfactual(f, np.array([2., 2.]), np.array([1., 1.]))
        self.assertEqual(r["cost"], 2)
        self.assertEqual(r["k"], (0, 2))

    def test_flip_other_direction(self):
        r = S.find_counterfactual(P, np.array([10., 1.]), np.array([0.5, 0.5]))
        self.assertEqual(int(r["label"]), 0)
        self.assertEqual((r["k"], r["cost"]), ((-1, -2), 3))

    def test_label_differs(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 1.]))
        self.assertNotEqual(int(P(r["x_cf"][None])[0]), int(P(np.array([[4., 2.]]))[0]))


if __name__ == "__main__":
    unittest.main()
