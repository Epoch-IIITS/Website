"""Tests for XA-12 LIME-style Local Linear Explanation.

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

class TestLIME(unittest.TestCase):
    def test_linear_exact(self):
        f = lambda X: 2 * X[:, 0] - X[:, 1]
        m = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])
        r = S.lime_explain(f, np.array([3., 1.]), np.zeros(2), m)
        np.testing.assert_allclose(r["coef"], [6., -1.], atol=1e-10)
        self.assertAlmostEqual(r["intercept"], 0.0, places=10)

    def test_masks(self):
        m = S.sample_masks(50, 4, np.random.default_rng(0))
        self.assertEqual(m.shape, (50, 4))
        np.testing.assert_array_equal(m[0], 1)
        self.assertTrue(set(np.unique(m)) <= {0, 1})

    def test_masks_recipe(self):
        m = S.sample_masks(5, 3, np.random.default_rng(7))
        exp = (np.random.default_rng(7).random((4, 3)) < 0.5).astype(int)
        np.testing.assert_array_equal(m[1:], exp)

    def test_weights(self):
        m = np.array([[1, 1], [0, 0], [1, 0]])
        r = S.lime_explain(lambda X: X.sum(1), np.ones(2), np.zeros(2), m, kernel_width=1.0)
        np.testing.assert_allclose(r["weights"], [1.0, np.exp(-1.0), np.exp(-0.25)])

    def test_matches_shapley_linear_random_masks(self):
        rng = np.random.default_rng(1)
        w = np.array([1.5, -2.0, 0.5, 3.0]); x = rng.normal(size=4); base = rng.normal(size=4)
        r = S.lime_explain(lambda X: X @ w + 1, x, base, S.sample_masks(64, 4, rng))
        np.testing.assert_allclose(r["coef"], w * (x - base), atol=1e-9)

    def test_ignored_feature_zero(self):
        rng = np.random.default_rng(2)
        r = S.lime_explain(lambda X: np.exp(X[:, 0]), np.array([1., 5.]), np.zeros(2), S.sample_masks(40, 2, rng))
        self.assertAlmostEqual(r["coef"][1], 0.0, places=9)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.lime_explain(lambda X: X[:, 0], np.ones(2), np.zeros(2), np.ones((3, 2)), kernel_width=0)


if __name__ == "__main__":
    unittest.main()
