"""Tests for ST-01 Mean and Variance (Population vs Sample).

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

DATA = [2, 4, 4, 4, 5, 5, 7, 9]

class TestMeanVar(unittest.TestCase):
    def test_population(self):
        self.assertEqual(S.mean_variance(DATA), (5.0, 4.0))

    def test_sample(self):
        m, v = S.mean_variance(DATA, sample=True)
        self.assertAlmostEqual(v, 32 / 7, places=12)

    def test_single(self):
        self.assertEqual(S.mean_variance([3]), (3.0, 0.0))

    def test_single_sample_error(self):
        with self.assertRaises(ValueError):
            S.mean_variance([3], sample=True)

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.mean_variance([])

    def test_matches_statistics_module(self):
        d = [0.5, 1.75, -2.0, 3.25, 10.0]
        self.assertAlmostEqual(S.mean_variance(d)[1], statistics.pvariance(d), places=12)
        self.assertAlmostEqual(S.mean_variance(d, sample=True)[1], statistics.variance(d), places=12)

    def test_large_offset_stable(self):
        d = [1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]
        self.assertAlmostEqual(S.mean_variance(d)[1], 22.5, places=6)


import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_statistics(self):
        data = [2.5, 3.0, 7.25, -1.0, 4.0]
        m, pv = S.mean_variance(data)
        _, sv = S.mean_variance(data, sample=True)
        self.assertAlmostEqual(m, statistics.fmean(data), places=12)
        self.assertAlmostEqual(pv, statistics.pvariance(data), places=12)
        self.assertAlmostEqual(sv, statistics.variance(data), places=12)


if __name__ == "__main__":
    unittest.main()
