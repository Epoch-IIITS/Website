"""Tests for MA-07 Binomial Coefficient.

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


class TestComb(unittest.TestCase):
    def test_small(self):
        self.assertEqual(S.comb(5, 2), 10)

    def test_edges(self):
        self.assertEqual(S.comb(5, 0), 1)
        self.assertEqual(S.comb(5, 5), 1)
        self.assertEqual(S.comb(0, 0), 1)

    def test_k_greater(self):
        self.assertEqual(S.comb(3, 5), 0)

    def test_negative(self):
        with self.assertRaises(ValueError):
            S.comb(-1, 0)

    def test_large_exact(self):
        self.assertEqual(S.comb(60, 30), 118264581564861424)
        self.assertIsInstance(S.comb(60, 30), int)

    def test_symmetry(self):
        for n in range(15):
            for k in range(n + 1):
                self.assertEqual(S.comb(n, k), S.comb(n, n - k))

    def test_pascal_rule(self):
        for n in range(1, 20):
            for k in range(1, n):
                self.assertEqual(S.comb(n, k), S.comb(n - 1, k - 1) + S.comb(n - 1, k))

    def test_row_sum(self):
        self.assertEqual(sum(S.comb(10, k) for k in range(11)), 2 ** 10)


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_math_comb(self):
        for n in range(0, 30, 3):
            for k in range(0, n + 3):
                self.assertEqual(S.comb(n, k), math.comb(n, k))


if __name__ == "__main__":
    unittest.main()
