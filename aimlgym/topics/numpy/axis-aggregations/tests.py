"""Tests for NP-05 Aggregations Along Axes.

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

X = np.array([[1, 5, 2], [7, 0, 3]])

class TestAxis(unittest.TestCase):
    def test_col_means(self):
        np.testing.assert_allclose(S.summarize(X)["col_means"], [4.0, 2.5, 2.5])

    def test_row_sums(self):
        np.testing.assert_array_equal(S.summarize(X)["row_sums"], [8, 10])

    def test_row_argmax(self):
        np.testing.assert_array_equal(S.summarize(X)["row_argmax"], [1, 0])

    def test_max_pos(self):
        self.assertEqual(S.summarize(X)["max_pos"], (1, 0))

    def test_keepdims(self):
        k = S.summarize(X)["row_means_keep"]
        self.assertEqual(k.shape, (2, 1))
        np.testing.assert_allclose(k[:, 0], [8 / 3, 10 / 3])

    def test_tie_first(self):
        self.assertEqual(S.summarize(np.array([[2, 9], [9, 1]]))["max_pos"], (0, 1))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            S.summarize(np.array([1, 2, 3]))


if __name__ == "__main__":
    unittest.main()
