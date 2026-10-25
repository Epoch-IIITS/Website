"""Tests for FL-14 FedProx Local Objective.

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

X1, Y1 = np.array([[1.]]), np.array([4.])

class TestFedProx(unittest.TestCase):
    def test_closed_form(self):
        for mu, exp in [(0.0, 4.0), (2.0, 2.0), (6.0, 1.0)]:
            np.testing.assert_allclose(S.local_prox_gd(np.zeros(1), X1, Y1, mu, 0.1, 2000), [exp], atol=1e-6)

    def test_grad_formula(self):
        g = S.prox_grad(np.array([1.0]), np.array([3.0]), X1, Y1, 0.5)
        np.testing.assert_allclose(g, [2 * (1 - 4) + 0.5 * (1 - 3)])

    def test_mu0_plain(self):
        rng = np.random.default_rng(0)
        X, y = rng.normal(size=(10, 2)), rng.normal(size=10)
        w = np.zeros(2)
        for _ in range(5):
            w = w - 0.05 * 2 / 10 * X.T @ (X @ w - y)
        np.testing.assert_allclose(S.local_prox_gd(np.zeros(2), X, y, 0.0, 0.05, 5), w)

    def test_drift_decreases_with_mu(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(30, 2)); y = X @ np.array([5., 5.])
        g = np.zeros(2)
        drifts = [np.linalg.norm(S.local_prox_gd(g, X, y, mu, 0.02, 300) - g) for mu in (0.0, 1.0, 10.0)]
        self.assertTrue(drifts[0] > drifts[1] > drifts[2])

    def test_anchor_fixed(self):
        g = np.array([1.0])
        S.local_prox_gd(g, X1, Y1, 1.0, 0.1, 10)
        np.testing.assert_array_equal(g, [1.0])

    def test_large_mu_stays(self):
        w = S.local_prox_gd(np.array([0.5]), X1, Y1, 1000.0, 0.001, 2000)
        self.assertAlmostEqual(w[0], (8 + 1000 * 0.5) / 1002, places=4)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.local_prox_gd(np.zeros(1), X1, Y1, -1.0, 0.1, 5)


if __name__ == "__main__":
    unittest.main()
