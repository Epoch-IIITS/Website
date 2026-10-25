"""Tests for XA-14 Integrated Gradients.

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

F = lambda P: P[:, 0] ** 2 * P[:, 1]
G = lambda P: np.column_stack([2 * P[:, 0] * P[:, 1], P[:, 0] ** 2])

class TestIG(unittest.TestCase):
    def test_example(self):
        ig, _ = S.integrated_gradients(G, np.array([1., 2.]), np.zeros(2), steps=1000)
        np.testing.assert_allclose(ig, [4 / 3, 2 / 3], atol=1e-5)

    def test_completeness(self):
        x, b = np.array([1.5, -0.5]), np.array([0.2, 0.3])
        ig, _ = S.integrated_gradients(G, x, b, steps=2000)
        self.assertAlmostEqual(ig.sum(), F(x[None])[0] - F(b[None])[0], places=5)

    def test_linear_exact(self):
        w = np.array([2., -3., 0.5])
        ig, _ = S.integrated_gradients(lambda P: np.tile(w, (len(P), 1)), np.array([1., 2., 3.]), np.zeros(3), steps=1)
        np.testing.assert_allclose(ig, w * np.array([1., 2., 3.]))

    def test_alphas_midpoint(self):
        _, a = S.integrated_gradients(G, np.ones(2), np.zeros(2), steps=4)
        np.testing.assert_allclose(a, [0.125, 0.375, 0.625, 0.875])

    def test_single_call(self):
        calls = []
        def g(P):
            calls.append(P.shape); return G(P)
        S.integrated_gradients(g, np.ones(2), np.zeros(2), steps=7)
        self.assertEqual(calls, [(7, 2)])

    def test_saturation_vs_gradient(self):
        sig = lambda z: 1 / (1 + np.exp(-z))
        g = lambda P: (sig(10 * P) * (1 - sig(10 * P))) * 10
        x = np.array([5.0])
        ig, _ = S.integrated_gradients(g, x, np.zeros(1), steps=4000)
        self.assertLess(float(g(x[None])[0, 0]), 1e-15)
        self.assertAlmostEqual(ig[0], sig(50) - 0.5, places=4)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.integrated_gradients(G, np.ones(2), np.zeros(3))


if __name__ == "__main__":
    unittest.main()
