"""Tests for ST-11 Covariance and Pearson Correlation.

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


import statistics

class TestCovCorr(unittest.TestCase):
    def test_cov(self):
        self.assertAlmostEqual(S.covariance([1, 2, 3, 4], [2, 4, 5, 8]), 9.5 / 3, places=12)

    def test_cov_population(self):
        self.assertAlmostEqual(S.covariance([1, 2, 3, 4], [2, 4, 5, 8], sample=False), 9.5 / 4)

    def test_r(self):
        self.assertAlmostEqual(S.pearson([1, 2, 3, 4], [2, 4, 5, 8]), 9.5 / math.sqrt(93.75), places=12)

    def test_perfect_negative(self):
        self.assertAlmostEqual(S.pearson([1, 2, 3], [3, 2, 1]), -1.0)

    def test_nonlinear_zero(self):
        self.assertAlmostEqual(S.pearson([-2, -1, 0, 1, 2], [4, 1, 0, 1, 4]), 0.0)

    def test_constant_raises(self):
        with self.assertRaises(ValueError):
            S.pearson([1, 2, 3], [5, 5, 5])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.covariance([1, 2], [1, 2, 3])

    def test_matches_statistics(self):
        x, y = [0.5, 2.0, 3.5, -1.0, 4.0], [1.0, 1.5, 4.0, -2.0, 3.0]
        self.assertAlmostEqual(S.covariance(x, y), statistics.covariance(x, y), places=12)
        self.assertAlmostEqual(S.pearson(x, y), statistics.correlation(x, y), places=12)

    def test_scale_invariance(self):
        x, y = [1, 3, 2, 5], [2, 1, 4, 3]
        self.assertAlmostEqual(S.pearson(x, y), S.pearson([10 * v + 7 for v in x], y), places=12)


import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_statistics_module(self):
        x = [1.0, 2.0, 4.0, 7.0, 11.0]
        y = [2.1, 3.9, 8.2, 13.8, 22.5]
        self.assertAlmostEqual(S.covariance(x, y), statistics.covariance(x, y), places=10)
        self.assertAlmostEqual(S.pearson(x, y), statistics.correlation(x, y), places=10)


if __name__ == "__main__":
    unittest.main()
