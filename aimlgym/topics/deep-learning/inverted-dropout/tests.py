"""Tests for DL-21 Inverted Dropout.

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

class TestDropout(unittest.TestCase):
    def test_values(self):
        y, m = S.dropout_forward(np.ones(8), 0.5, np.random.default_rng(0))
        self.assertTrue(set(np.unique(y)).issubset({0.0, 2.0}))
        np.testing.assert_allclose(y, m * 2.0)

    def test_recipe(self):
        rng_a, rng_b = np.random.default_rng(7), np.random.default_rng(7)
        x = np.arange(10.0)
        y, m = S.dropout_forward(x, 0.3, rng_a)
        exp_mask = rng_b.random(x.shape) >= 0.3
        np.testing.assert_array_equal(m, exp_mask)
        np.testing.assert_allclose(y, x * exp_mask / 0.7)

    def test_eval_identity(self):
        y, m = S.dropout_forward(np.array([1., 2., 3.]), 0.5, None, training=False)
        np.testing.assert_array_equal(y, [1, 2, 3])
        self.assertIsNone(m)

    def test_expectation(self):
        y, _ = S.dropout_forward(np.full(200000, 3.0), 0.4, np.random.default_rng(1))
        self.assertAlmostEqual(y.mean(), 3.0, delta=0.02)

    def test_p0_identity(self):
        y, _ = S.dropout_forward(np.array([5., -1.]), 0.0, np.random.default_rng(2))
        np.testing.assert_array_equal(y, [5., -1.])

    def test_backward(self):
        x = np.array([1., 2., 3., 4.])
        y, m = S.dropout_forward(x, 0.5, np.random.default_rng(3))
        g = S.dropout_backward(np.ones(4), m, 0.5)
        np.testing.assert_allclose(g, m * 2.0)

    def test_bad_p(self):
        with self.assertRaises(ValueError):
            S.dropout_forward(np.ones(2), 1.0, np.random.default_rng(0))


if __name__ == "__main__":
    unittest.main()
