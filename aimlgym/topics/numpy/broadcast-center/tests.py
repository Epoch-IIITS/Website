"""Tests for NP-07 Centering Columns with Broadcasting.

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

X = np.array([[1., 2.], [3., 6.]])

class TestBroadcast(unittest.TestCase):
    def test_center(self):
        np.testing.assert_allclose(S.center_columns(X), [[-1, -2], [1, 2]])

    def test_center_means_zero(self):
        Y = S.center_columns(np.array([[1., 9, 4], [2, 7, 1], [6, 2, 0], [3, 3, 3]]))
        np.testing.assert_allclose(Y.mean(axis=0), 0, atol=1e-12)

    def test_scale_rows(self):
        np.testing.assert_allclose(S.scale_rows(X, [10, 0.5]), [[10, 20], [1.5, 3]])

    def test_scale_rows_bad(self):
        with self.assertRaises(ValueError):
            S.scale_rows(X, [1, 2, 3])

    def test_standardize_constant(self):
        np.testing.assert_allclose(S.standardize(np.array([[1., 5.], [3., 5.]])), [[-1, 0], [1, 0]])

    def test_standardize_props(self):
        Z = S.standardize(np.array([[1., 10], [2, 30], [4, 20], [9, 0]]))
        np.testing.assert_allclose(Z.mean(axis=0), 0, atol=1e-12)
        np.testing.assert_allclose(Z.std(axis=0), 1, atol=1e-12)

    def test_no_nan(self):
        self.assertFalse(np.isnan(S.standardize(np.ones((3, 2)))).any())

    def test_shape_preserved(self):
        self.assertEqual(S.scale_rows(np.ones((5, 3)), np.arange(5)).shape, (5, 3))


if __name__ == "__main__":
    unittest.main()
