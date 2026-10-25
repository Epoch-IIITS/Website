"""Tests for ST-03 Percentiles by Linear Interpolation.

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


class TestPercentile(unittest.TestCase):
    def test_interp(self):
        self.assertAlmostEqual(S.percentile([1, 2, 3, 4, 10], 40), 2.6)

    def test_median(self):
        self.assertAlmostEqual(S.percentile([7, 1, 3, 5], 50), 4.0)

    def test_ends(self):
        self.assertEqual(S.percentile([5, 1, 9], 0), 1)
        self.assertEqual(S.percentile([5, 1, 9], 100), 9)

    def test_single(self):
        self.assertEqual(S.percentile([3], 37), 3.0)

    def test_iqr(self):
        self.assertAlmostEqual(S.iqr([1, 2, 3, 4, 10]), 2.0)

    def test_tukey(self):
        self.assertEqual(S.tukey_outliers([1, 2, 3, 4, 10]), [10])
        self.assertEqual(S.tukey_outliers([-20, 1, 2, 3, 4]), [-20])

    def test_bad_q(self):
        with self.assertRaises(ValueError):
            S.percentile([1, 2], 101)
        with self.assertRaises(ValueError):
            S.percentile([], 50)

    def test_known_values(self):
        d = list(range(1, 11))
        self.assertAlmostEqual(S.percentile(d, 25), 3.25)
        self.assertAlmostEqual(S.percentile(d, 90), 9.1)


import statistics

import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_and_statistics(self):
        data = [7, 1, 3, 9, 4, 4, 12, 2]
        for q in (0, 10, 25, 50, 90, 100):
            self.assertAlmostEqual(S.percentile(data, q), float(np.percentile(data, q)))
        q1, q2, q3 = statistics.quantiles(data, n=4, method="inclusive")
        self.assertAlmostEqual(S.iqr(data), q3 - q1)


if __name__ == "__main__":
    unittest.main()
