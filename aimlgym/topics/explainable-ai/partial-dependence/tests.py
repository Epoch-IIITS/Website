"""Tests for XA-06 Partial Dependence by Hand.

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

F = lambda X: X[:, 0] * X[:, 1]

class TestPDP(unittest.TestCase):
    def test_interaction_flat(self):
        X = np.array([[0., -1.], [0., 1.]])
        np.testing.assert_allclose(S.partial_dependence(F, X, 0, [0, 1, 2]), 0)

    def test_spread(self):
        X = np.array([[0., -1.], [0., 1.]])
        self.assertAlmostEqual(S.ice_spread(F, X, 0, [0, 1, 2]), 1.0)

    def test_additive_no_spread(self):
        g = lambda X: 3 * X[:, 0] + X[:, 1] ** 2
        X = np.random.default_rng(0).normal(size=(20, 2))
        self.assertAlmostEqual(S.ice_spread(g, X, 0, np.linspace(-1, 1, 5)), 0.0)

    def test_linear_pd(self):
        g = lambda X: 2 * X[:, 0] + X[:, 1]
        X = np.array([[5., 1.], [6., 3.]])
        np.testing.assert_allclose(S.partial_dependence(g, X, 0, [0, 1]), [2, 4])

    def test_matches_ice_average(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(7, 3)); grid = [-1, 0, 2]
        h = lambda X: np.tanh(X[:, 0] * X[:, 2]) + X[:, 1]
        exp = []
        for gv in grid:
            Xg = X.copy(); Xg[:, 2] = gv; exp.append(h(Xg).mean())
        np.testing.assert_allclose(S.partial_dependence(h, X, 2, grid), exp)

    def test_no_mutation(self):
        X = np.array([[1., 2.]])
        S.partial_dependence(F, X, 1, [7, 8])
        np.testing.assert_array_equal(X, [[1., 2.]])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.partial_dependence(F, np.zeros((0, 2)), 0, [1])


if __name__ == "__main__":
    unittest.main()
