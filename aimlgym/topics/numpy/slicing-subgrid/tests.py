"""Tests for NP-03 Slicing a Sub-grid.

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

A = np.arange(16).reshape(4, 4)

class TestSlicing(unittest.TestCase):
    def test_crop(self):
        np.testing.assert_array_equal(S.crop(A, 1, 1, 2, 2), [[5, 6], [9, 10]])

    def test_crop_is_copy(self):
        a = A.copy()
        c = S.crop(a, 0, 0, 2, 2)
        c[0, 0] = 99
        self.assertEqual(a[0, 0], 0)

    def test_crop_out_of_bounds(self):
        with self.assertRaises(ValueError):
            S.crop(A, 3, 3, 2, 2)
        with self.assertRaises(ValueError):
            S.crop(A, -1, 0, 1, 1)

    def test_every_other(self):
        np.testing.assert_array_equal(S.every_other(A), [[0, 2], [8, 10]])

    def test_border(self):
        self.assertEqual(S.border_sum(A), 90)

    def test_border_small(self):
        self.assertEqual(S.border_sum(np.array([[1, 2], [3, 4]])), 10)
        self.assertEqual(S.border_sum(np.array([[5]])), 5)

    def test_full_crop(self):
        np.testing.assert_array_equal(S.crop(A, 0, 0, 4, 4), A)


if __name__ == "__main__":
    unittest.main()
