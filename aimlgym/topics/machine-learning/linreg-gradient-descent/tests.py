"""Tests for ML-10 Linear Regression by Gradient Descent.

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

X1 = np.array([[0.], [1.], [2.]]); Y1 = np.array([1., 3., 5.])

class TestGDReg(unittest.TestCase):
    def test_grad_values(self):
        loss, gw, gb = S.mse_grad(X1, Y1, np.zeros(1), 0.0)
        self.assertAlmostEqual(loss, 35 / 3)
        np.testing.assert_allclose(gw, [-26 / 3])
        self.assertAlmostEqual(gb, -6.0)

    def test_grad_numerical(self):
        rng = np.random.default_rng(0)
        X, y, w, b = rng.normal(size=(8, 3)), rng.normal(size=8), rng.normal(size=3), 0.3
        _, gw, gb = S.mse_grad(X, y, w, b)
        h = 1e-6
        for j in range(3):
            e = np.zeros(3); e[j] = h
            num = (S.mse_grad(X, y, w + e, b)[0] - S.mse_grad(X, y, w - e, b)[0]) / (2 * h)
            self.assertAlmostEqual(gw[j], num, places=5)
        numb = (S.mse_grad(X, y, w, b + h)[0] - S.mse_grad(X, y, w, b - h)[0]) / (2 * h)
        self.assertAlmostEqual(gb, numb, places=5)

    def test_fit_simple(self):
        w, b, _ = S.fit_gd(X1, Y1, lr=0.1, epochs=2000)
        np.testing.assert_allclose(w, [2.0], atol=1e-6)
        self.assertAlmostEqual(b, 1.0, delta=1e-6)

    def test_matches_lstsq(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(100, 3)); y = X @ np.array([1.5, -2.0, 0.5]) + 0.7 + rng.normal(0, 0.1, 100)
        w, b, _ = S.fit_gd(X, y, lr=0.1, epochs=3000)
        A = np.column_stack([np.ones(100), X])
        sol = np.linalg.lstsq(A, y, rcond=None)[0]
        np.testing.assert_allclose(np.r_[b, w], sol, atol=1e-6)

    def test_history_decreasing(self):
        _, _, h = S.fit_gd(X1, Y1, lr=0.05, epochs=50)
        self.assertEqual(len(h), 50)
        self.assertTrue(all(h[i + 1] <= h[i] for i in range(49)))

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.fit_gd(X1, Y1, lr=0)
        with self.assertRaises(ValueError):
            S.mse_grad(X1, Y1[:2], np.zeros(1), 0.0)


if __name__ == "__main__":
    unittest.main()
