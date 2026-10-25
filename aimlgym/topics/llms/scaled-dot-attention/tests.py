"""Tests for LM-07 Scaled Dot-Product Attention.

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

class TestAttention(unittest.TestCase):
    def test_example(self):
        out, w = S.attention(np.array([[1., 0.]]), np.array([[1., 0.], [0., 1.]]), np.array([[1., 2.], [3., 4.]]))
        a = np.exp(1 / np.sqrt(2)); e = np.array([a, 1.0]) / (a + 1)
        np.testing.assert_allclose(w, [e])
        np.testing.assert_allclose(out, [e @ np.array([[1., 2.], [3., 4.]])])

    def test_rows_sum_one(self):
        rng = np.random.default_rng(0)
        _, w = S.attention(rng.normal(size=(4, 8)), rng.normal(size=(6, 8)), rng.normal(size=(6, 3)))
        np.testing.assert_allclose(w.sum(axis=1), 1.0)
        self.assertEqual(w.shape, (4, 6))

    def test_identical_keys_average(self):
        out, _ = S.attention(np.ones((1, 2)), np.ones((3, 2)), np.array([[0.], [3.], [6.]]))
        np.testing.assert_allclose(out, [[3.0]])

    def test_mask(self):
        out, w = S.attention(np.ones((1, 2)), np.ones((2, 2)), np.array([[1.], [5.]]),
                             mask=np.array([[True, False]]))
        np.testing.assert_allclose(w, [[1.0, 0.0]])
        np.testing.assert_allclose(out, [[1.0]])

    def test_scaling(self):
        q = np.array([[2., 2., 2., 2.]]); k = np.array([[1., 1., 1., 1.], [0., 0., 0., 0.]])
        _, w = S.attention(q, k, np.eye(2))
        self.assertAlmostEqual(w[0, 0], 1 / (1 + np.exp(-4.0)))

    def test_all_masked_row(self):
        with self.assertRaises(ValueError):
            S.attention(np.ones((1, 2)), np.ones((2, 2)), np.ones((2, 1)), mask=np.array([[False, False]]))

    def test_shape_error(self):
        with self.assertRaises(ValueError):
            S.attention(np.ones((1, 3)), np.ones((2, 2)), np.ones((2, 1)))


if __name__ == "__main__":
    unittest.main()
