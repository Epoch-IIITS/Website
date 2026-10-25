"""Tests for NP-14 Moving Average with cumsum.

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

class TestMovingAverage(unittest.TestCase):
    def test_example(self):
        np.testing.assert_allclose(S.moving_average([1, 2, 3, 4, 5], 2), [1.5, 2.5, 3.5, 4.5])

    def test_full_window(self):
        np.testing.assert_allclose(S.moving_average([4, 8], 2), [6.0])

    def test_w1_identity(self):
        np.testing.assert_allclose(S.moving_average([3, -1, 2], 1), [3, -1, 2])

    def test_matches_convolve(self):
        x = np.random.default_rng(0).normal(size=200)
        np.testing.assert_allclose(S.moving_average(x, 7), np.convolve(x, np.ones(7) / 7, mode="valid"),
                                   rtol=1e-10, atol=1e-12)

    def test_bad_w(self):
        with self.assertRaises(ValueError):
            S.moving_average([1, 2], 3)
        with self.assertRaises(ValueError):
            S.moving_average([1, 2], 0)

    def test_windows(self):
        np.testing.assert_array_equal(S.windows(np.arange(4), 3), [[0, 1, 2], [1, 2, 3]])

    def test_windows_mean_consistent(self):
        x = np.arange(10.0) ** 2
        np.testing.assert_allclose(S.windows(x, 4).mean(axis=1), S.moving_average(x, 4))


import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_convolve(self):
        x = np.array([3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0])
        for w in (1, 3, 8):
            np.testing.assert_allclose(S.moving_average(x, w), np.convolve(x, np.ones(w) / w, mode="valid"))


if __name__ == "__main__":
    unittest.main()
