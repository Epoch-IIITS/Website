"""Tests for MA-01 Summation and Product Notation.

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


class TestSummation(unittest.TestCase):
    def test_sum_odd_numbers(self):
        self.assertEqual(S.summation(lambda i: 2 * i + 1, 1, 4), 24)

    def test_empty_ranges(self):
        self.assertEqual(S.summation(lambda i: i, 5, 4), 0)
        self.assertEqual(S.product(lambda i: i, 5, 4), 1)

    def test_product_factorial(self):
        self.assertEqual(S.product(lambda i: i, 1, 5), 120)
        self.assertAlmostEqual(S.product(lambda i: 0.5, 1, 3), 0.125)

    def test_mean(self):
        self.assertEqual(S.mean([2, 4, 9]), 5.0)
        with self.assertRaises(ValueError):
            S.mean([])

    def test_closed_form_matches_loop(self):
        for n in range(0, 60):
            self.assertEqual(S.sum_of_squares(n), S.summation(lambda i: i * i, 1, n))
        self.assertIsInstance(S.sum_of_squares(10), int)

    def test_accurate_sum(self):
        self.assertEqual(S.accurate_sum([0.1] * 10), 1.0)
        self.assertNotEqual(S.summation(lambda i: 0.1, 1, 10), 1.0)

    def test_matches_builtins(self):
        f = lambda i: i ** 3 - 2 * i
        self.assertEqual(S.summation(f, -3, 7), sum(f(i) for i in range(-3, 8)))
        self.assertEqual(S.product(lambda i: i, 1, 10), math.prod(range(1, 11)))


import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_mean_matches_statistics(self):
        data = [1.5, 2.25, -4.0, 10.125, 3.0]
        self.assertAlmostEqual(S.mean(data), statistics.fmean(data), places=12)


if __name__ == "__main__":
    unittest.main()
