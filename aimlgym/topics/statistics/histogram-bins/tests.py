"""Tests for ST-04 Histogram with Equal-Width Bins.

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


class TestHistogram(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(S.histogram([1, 2, 2, 3, 4, 5], 2), ([1.0, 3.0, 5.0], [3, 3]))

    def test_explicit_range_outside(self):
        self.assertEqual(S.histogram([0, 10, 11], 2, lo=0, hi=10), ([0.0, 5.0, 10.0], [1, 1]))

    def test_max_in_last_bin(self):
        _, c = S.histogram([0, 1, 2, 3, 4], 4)
        self.assertEqual(c, [1, 1, 1, 2])

    def test_constant_data(self):
        e, c = S.histogram([7, 7, 7], 1)
        self.assertEqual(e, [6.5, 7.5])
        self.assertEqual(c, [3])

    def test_counts_sum(self):
        d = [0.1 * i for i in range(101)]
        _, c = S.histogram(d, 7)
        self.assertEqual(sum(c), 101)

    def test_bad_bins(self):
        with self.assertRaises(ValueError):
            S.histogram([1, 2], 0)

    def test_empty_needs_range(self):
        with self.assertRaises(ValueError):
            S.histogram([], 3)
        self.assertEqual(S.histogram([], 2, lo=0, hi=1), ([0.0, 0.5, 1.0], [0, 0]))

    def test_matches_numpy_convention(self):
        e, c = S.histogram([0.0, 0.25, 0.5, 0.75, 1.0], 2)
        self.assertEqual(c, [2, 3])


import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_histogram(self):
        data = [0.0, 0.5, 1.0, 2.5, 3.0, 3.0, 4.9, 5.0]
        edges, counts = S.histogram(data, 5)
        np_counts, np_edges = np.histogram(data, bins=5)
        self.assertEqual(counts, np_counts.tolist())
        np.testing.assert_allclose(edges, np_edges)
        edges, counts = S.histogram([2.0, 2.0], 2)
        np_counts, np_edges = np.histogram([2.0, 2.0], bins=2)
        self.assertEqual(counts, np_counts.tolist())
        np.testing.assert_allclose(edges, np_edges)


if __name__ == "__main__":
    unittest.main()
