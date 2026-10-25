"""Tests for XA-11 Exact Shapley Values.

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

class TestShapley(unittest.TestCase):
    def test_interaction_split(self):
        np.testing.assert_allclose(S.shapley_values(lambda X: X[:, 0] * X[:, 1], np.array([1., 1.]), np.zeros(2)), [0.5, 0.5])

    def test_linear_matches_xa01(self):
        w = np.array([2., -1., 0.5]); x = np.array([3., 4., -2.]); base = np.array([1., 1., 1.])
        np.testing.assert_allclose(S.shapley_values(lambda X: X @ w + 7, x, base), w * (x - base))

    def test_efficiency(self):
        f = lambda X: np.tanh(X[:, 0] * X[:, 1]) + X[:, 2] ** 2 - X[:, 0] * X[:, 3]
        rng = np.random.default_rng(0)
        x, base = rng.normal(size=4), rng.normal(size=4)
        phi = S.shapley_values(f, x, base)
        self.assertAlmostEqual(phi.sum(), f(x[None])[0] - f(base[None])[0])

    def test_dummy(self):
        phi = S.shapley_values(lambda X: X[:, 0] ** 3, np.array([2., 5., 7.]), np.zeros(3))
        np.testing.assert_allclose(phi[1:], 0.0)

    def test_symmetry(self):
        phi = S.shapley_values(lambda X: X[:, 0] + X[:, 1] + X[:, 0] * X[:, 1], np.array([2., 2.]), np.zeros(2))
        self.assertAlmostEqual(phi[0], phi[1])

    def test_coalition_value(self):
        f = lambda X: X[:, 0] * 10 + X[:, 1]
        self.assertEqual(S.coalition_value(f, np.array([1., 2.]), np.array([0., 0.]), (1,)), 2.0)

    def test_max_d(self):
        with self.assertRaises(ValueError):
            S.shapley_values(lambda X: X.sum(1), np.ones(13), np.zeros(13))


if __name__ == "__main__":
    unittest.main()
