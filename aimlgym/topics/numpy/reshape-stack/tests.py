"""Tests for NP-08 Reshape and Stack.

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

class TestReshape(unittest.TestCase):
    def test_batches(self):
        np.testing.assert_array_equal(S.to_batches(np.arange(10), 4), [[0, 1, 2, 3], [4, 5, 6, 7]])

    def test_batches_exact(self):
        self.assertEqual(S.to_batches(np.arange(12), 3).shape, (4, 3))

    def test_batches_bad(self):
        with self.assertRaises(ValueError):
            S.to_batches(np.arange(3), 5)
        with self.assertRaises(ValueError):
            S.to_batches(np.arange(3), 0)

    def test_bias(self):
        np.testing.assert_allclose(S.add_bias_column(np.array([[3, 4], [5, 6]])), [[1, 3, 4], [1, 5, 6]])

    def test_bias_shape(self):
        self.assertEqual(S.add_bias_column(np.zeros((7, 3))).shape, (7, 4))

    def test_flatten(self):
        np.testing.assert_array_equal(S.flatten_images(np.arange(8).reshape(2, 2, 2)),
                                      [[0, 1, 2, 3], [4, 5, 6, 7]])

    def test_flatten_bad(self):
        with self.assertRaises(ValueError):
            S.flatten_images(np.zeros((4, 4)))


if __name__ == "__main__":
    unittest.main()
