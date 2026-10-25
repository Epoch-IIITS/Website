"""Tests for PY-11 Sum and Mean of a List.

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


class TestSumAndMean(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(S.sum_and_mean([2, 4, 9]), (15, 5.0))

    def test_empty(self):
        self.assertEqual(S.sum_and_mean([]), (0, None))

    def test_single(self):
        self.assertEqual(S.sum_and_mean([7]), (7, 7.0))

    def test_floats_tolerance(self):
        t, m = S.sum_and_mean([0.1, 0.2, 0.3])
        self.assertAlmostEqual(t, 0.6, places=9)
        self.assertAlmostEqual(m, 0.2, places=9)

    def test_negative_cancel(self):
        t, m = S.sum_and_mean([-1.5, 1.5])
        self.assertAlmostEqual(t, 0.0)
        self.assertAlmostEqual(m, 0.0)

    def test_mean_is_true_division(self):
        self.assertEqual(S.sum_and_mean([1, 2])[1], 1.5)

    def test_input_not_modified(self):
        data = [3, 1, 2]
        S.sum_and_mean(data)
        self.assertEqual(data, [3, 1, 2])


import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_builtins(self):
        data = [3, -1.5, 8, 0.25, 4]
        total, mean = S.sum_and_mean(data)
        self.assertAlmostEqual(total, sum(data))
        self.assertAlmostEqual(mean, statistics.fmean(data))


if __name__ == "__main__":
    unittest.main()
