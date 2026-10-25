"""Tests for NP-13 One-Hot Encoding.

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

class TestOneHot(unittest.TestCase):
    def test_basic(self):
        np.testing.assert_array_equal(S.one_hot([2, 0, 1]), [[0, 0, 1], [1, 0, 0], [0, 1, 0]])

    def test_num_classes(self):
        np.testing.assert_array_equal(S.one_hot([1], num_classes=4), [[0, 1, 0, 0]])

    def test_roundtrip(self):
        np.testing.assert_array_equal(S.from_one_hot(S.one_hot([3, 1, 3])), [3, 1, 3])

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            S.one_hot([0, 3], num_classes=3)

    def test_negative(self):
        with self.assertRaises(ValueError):
            S.one_hot([-1, 0])

    def test_float_labels(self):
        with self.assertRaises(ValueError):
            S.one_hot([0.0, 1.0])

    def test_bad_decode(self):
        with self.assertRaises(ValueError):
            S.from_one_hot(np.array([[1, 1, 0]]))
        with self.assertRaises(ValueError):
            S.from_one_hot(np.array([[0.5, 0.5]]))

    def test_dtype_and_sum(self):
        Y = S.one_hot([0, 1, 1, 0])
        self.assertEqual(Y.dtype, np.float64)
        np.testing.assert_array_equal(Y.sum(axis=1), 1)


import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_eye_idiom(self):
        labels = np.array([2, 0, 1, 2, 3])
        np.testing.assert_array_equal(S.one_hot(labels, 5), np.eye(5)[labels])


if __name__ == "__main__":
    unittest.main()
