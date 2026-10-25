"""Tests for MA-15 Taylor Series for exp(x).

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


class TestTaylor(unittest.TestCase):
    def test_five_terms(self):
        self.assertAlmostEqual(S.exp_taylor(1.0, 5), 2.708333333333333, places=12)

    def test_zero_terms(self):
        self.assertEqual(S.exp_taylor(2.0, 0), 0.0)

    def test_x_zero(self):
        self.assertEqual(S.exp_taylor(0.0, 3), 1.0)

    def test_converges(self):
        for x in (-1.5, 0.3, 2.0, 5.0):
            self.assertAlmostEqual(S.exp_taylor(x, 60), math.exp(x), delta=1e-9 * max(1, math.exp(x)))

    def test_terms_needed(self):
        self.assertEqual(S.terms_needed(1.0, 1e-3), 7)

    def test_terms_needed_zero_x(self):
        self.assertEqual(S.terms_needed(0.0, 0.5), 1)

    def test_terms_needed_consistent(self):
        n = S.terms_needed(2.0, 1e-10)
        self.assertLess(abs(S.exp_taylor(2.0, n) - math.exp(2.0)), 1e-8)

    def test_bad_args(self):
        with self.assertRaises(ValueError):
            S.exp_taylor(1.0, -1)
        with self.assertRaises(ValueError):
            S.terms_needed(1.0, 0)

    def test_large_terms_no_overflow(self):
        self.assertAlmostEqual(S.exp_taylor(1.0, 500), math.e, places=12)


if __name__ == "__main__":
    unittest.main()
