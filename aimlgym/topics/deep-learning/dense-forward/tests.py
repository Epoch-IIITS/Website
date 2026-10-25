"""Tests for DL-04 Dense Layer Forward Pass.

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

class TestDense(unittest.TestCase):
    def test_forward(self):
        Y = S.dense(np.array([[1., 2.]]), np.array([[1., 0., -1.], [2., 1., 0.]]), np.array([0.5, 0., 0.]))
        np.testing.assert_allclose(Y, [[5.5, 2., -1.]])

    def test_batch_shape(self):
        self.assertEqual(S.dense(np.ones((7, 4)), np.ones((4, 3)), np.zeros(3)).shape, (7, 3))

    def test_shape_errors(self):
        with self.assertRaises(ValueError):
            S.dense(np.ones((2, 3)), np.ones((4, 2)), np.zeros(2))
        with self.assertRaises(ValueError):
            S.dense(np.ones((2, 3)), np.ones((3, 2)), np.zeros(3))

    def test_n_params(self):
        self.assertEqual(S.n_params([784, 128, 10]), 101770)
        self.assertEqual(S.n_params([2, 1]), 3)

    def test_n_params_bad(self):
        with self.assertRaises(ValueError):
            S.n_params([5])

    def test_he_stats(self):
        W, b = S.he_init(500, 400, np.random.default_rng(0))
        self.assertEqual(W.shape, (500, 400))
        np.testing.assert_array_equal(b, np.zeros(400))
        self.assertAlmostEqual(W.std(), np.sqrt(2 / 500), delta=0.002)
        self.assertAlmostEqual(W.mean(), 0.0, delta=0.002)

    def test_he_reproducible(self):
        a, _ = S.he_init(3, 2, np.random.default_rng(5))
        b, _ = S.he_init(3, 2, np.random.default_rng(5))
        np.testing.assert_array_equal(a, b)


if __name__ == "__main__":
    unittest.main()
