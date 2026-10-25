"""Tests for XA-10 Global Surrogate and Fidelity.

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

X = np.random.default_rng(0).normal(size=(100, 2))

class TestSurrogate(unittest.TestCase):
    def test_linear_recovered(self):
        f = lambda X: 2 * X[:, 0] - X[:, 1] + 3
        b, w = S.fit_linear_surrogate(f, X)
        self.assertAlmostEqual(b, 3.0)
        np.testing.assert_allclose(w, [2, -1], atol=1e-10)
        self.assertAlmostEqual(S.fidelity_r2(f, lambda X: b + X @ w, X), 1.0)

    def test_nonlinear_low_fidelity(self):
        f = lambda X: X[:, 0] ** 2
        Xs = np.column_stack([np.linspace(-2, 2, 101), np.zeros(101)])
        b, w = S.fit_linear_surrogate(f, Xs)
        self.assertLess(S.fidelity_r2(f, lambda Z: b + Z @ w, Xs), 0.05)

    def test_fits_predictions_not_labels(self):
        f = lambda X: 5 * X[:, 1]
        _, w = S.fit_linear_surrogate(f, X)
        np.testing.assert_allclose(w, [0, 5], atol=1e-10)

    def test_partial_fidelity(self):
        f = lambda X: X[:, 0] + np.sin(3 * X[:, 1])
        b, w = S.fit_linear_surrogate(f, X)
        r = S.fidelity_r2(f, lambda Z: b + Z @ w, X)
        self.assertTrue(0.3 < r < 0.95)

    def test_constant_blackbox(self):
        f = lambda X: np.full(len(X), 4.0)
        self.assertEqual(S.fidelity_r2(f, lambda Z: np.full(len(Z), 4.0), X), 1.0)
        self.assertEqual(S.fidelity_r2(f, lambda Z: np.zeros(len(Z)), X), 0.0)

    def test_bad_surrogate_negative(self):
        f = lambda X: X[:, 0]
        self.assertLess(S.fidelity_r2(f, lambda Z: -Z[:, 0], X), 0)


if __name__ == "__main__":
    unittest.main()
