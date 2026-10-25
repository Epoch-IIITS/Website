"""Tests for NP-04 Boolean Masks.

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

A = np.array([4, -1, 9, 3, 12])

class TestMasks(unittest.TestCase):
    def test_in_range(self):
        np.testing.assert_array_equal(S.in_range(A, 0, 9), [4, 9, 3])

    def test_in_range_2d(self):
        np.testing.assert_array_equal(S.in_range(np.array([[1, 5], [7, 2]]), 2, 6), [5, 2])

    def test_in_range_empty(self):
        self.assertEqual(S.in_range(A, 100, 200).size, 0)

    def test_count(self):
        self.assertEqual(S.count_above(A, 5), 2)
        self.assertIsInstance(S.count_above(A, 5), int)

    def test_count_strict(self):
        self.assertEqual(S.count_above(np.array([5, 5, 6]), 5), 1)

    def test_cap(self):
        np.testing.assert_array_equal(S.cap(A, 5), [4, -1, 5, 3, 5])

    def test_cap_no_mutation(self):
        a = A.copy()
        S.cap(a, 0)
        np.testing.assert_array_equal(a, A)

    def test_float(self):
        np.testing.assert_allclose(S.cap(np.array([0.5, 2.5]), 1.0), [0.5, 1.0])


if __name__ == "__main__":
    unittest.main()
