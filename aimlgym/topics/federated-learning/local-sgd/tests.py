"""Tests for FL-06 Local SGD on a Client.

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

class TestLocalSGD(unittest.TestCase):
    def test_full_batch_one_step(self):
        X = np.array([[1., 0.], [0., 1.]]); y = np.array([1., 2.])
        np.testing.assert_allclose(S.local_sgd(np.zeros(2), X, y, 0.5, 1, 2, 0), [0.5, 1.0])

    def test_grad(self):
        X = np.array([[1., 2.], [3., 4.]]); y = np.array([1., 0.]); w = np.array([0.5, -0.5])
        np.testing.assert_allclose(S.mse_grad(w, X, y), 2 / 2 * X.T @ (X @ w - y))

    def test_recipe(self):
        rng0 = np.random.default_rng(1)
        X, y = rng0.normal(size=(7, 3)), rng0.normal(size=7)
        w = np.zeros(3); rng = np.random.default_rng(11)
        for _ in range(2):
            o = rng.permutation(7)
            for s in range(0, 7, 3):
                b = o[s:s + 3]; w = w - 0.05 * 2 / len(b) * X[b].T @ (X[b] @ w - y[b])
        np.testing.assert_allclose(S.local_sgd(np.zeros(3), X, y, 0.05, 2, 3, 11), w)

    def test_converges(self):
        rng = np.random.default_rng(2)
        X = rng.normal(size=(100, 2)); y = X @ np.array([2., -1.])
        np.testing.assert_allclose(S.local_sgd(np.zeros(2), X, y, 0.05, 50, 10, 0), [2., -1.], atol=1e-6)

    def test_no_mutation(self):
        w = np.zeros(2)
        S.local_sgd(w, np.eye(2), np.ones(2), 0.1, 1, 1, 0)
        np.testing.assert_array_equal(w, [0, 0])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.local_sgd(np.zeros(2), np.eye(2), np.ones(2), 0.1, 0, 1, 0)


if __name__ == "__main__":
    unittest.main()
