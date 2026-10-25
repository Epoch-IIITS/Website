"""Tests for DL-25 1D Convolution by Hand (valid, stride).

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

X = [1, 2, 3, 4, 5]

class TestConv1d(unittest.TestCase):
    def test_valid(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 0, -1]), [-2, -2, -2])

    def test_stride(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 0, -1], stride=2), [-2, -2])

    def test_padding(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 0, -1], padding=1), [-2, -2, -2, -2, 4])

    def test_no_flip(self):
        np.testing.assert_allclose(S.conv1d(X, [1, 2]), np.correlate(X, [1, 2], mode="valid"))

    def test_bias(self):
        np.testing.assert_allclose(S.conv1d([1, 1, 1], [1, 1], bias=0.5), [2.5, 2.5])

    def test_output_length(self):
        self.assertEqual(S.conv_output_length(32, 5, 1, 2), 32)
        self.assertEqual(S.conv_output_length(7, 3, 2, 0), 3)
        for n, k, s, p in [(10, 3, 1, 0), (10, 4, 3, 1), (9, 2, 2, 2)]:
            self.assertEqual(len(S.conv1d(np.ones(n), np.ones(k), s, p)), S.conv_output_length(n, k, s, p))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.conv1d([1, 2], [1, 2, 3])
        with self.assertRaises(ValueError):
            S.conv_output_length(5, 2, 0, 0)


import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_correlate(self):
        x = np.array([1.0, 3.0, -2.0, 4.0, 0.5, 2.0])
        w = np.array([0.5, -1.0, 2.0])
        for p in (0, 1, 2):
            np.testing.assert_allclose(S.conv1d(x, w, padding=p), np.correlate(np.pad(x, p), w, mode="valid"))
        np.testing.assert_allclose(S.conv1d(x, w, stride=2), np.correlate(x, w, mode="valid")[::2])


if __name__ == "__main__":
    unittest.main()
