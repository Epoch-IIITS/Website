"""Tests for RL-01 Discounted Return.

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


class TestReturns(unittest.TestCase):
    def test_example(self):
        self.assertAlmostEqual(S.discounted_return([1, 0, 2], 0.5), 1.5)
        self.assertEqual([round(g, 10) for g in S.returns_to_go([1, 0, 2], 0.5)], [1.5, 1.0, 2.0])

    def test_gamma_zero(self):
        self.assertEqual(S.returns_to_go([3, 4, 5], 0.0), [3, 4, 5])

    def test_gamma_one(self):
        self.assertEqual(S.returns_to_go([1, 2, 3], 1.0), [6, 5, 3])

    def test_empty(self):
        self.assertEqual(S.discounted_return([], 0.9), 0.0)
        self.assertEqual(S.returns_to_go([], 0.9), [])

    def test_formula(self):
        r = [0.5, -1.0, 2.0, 0.0, 3.0]
        g = 0.9
        self.assertAlmostEqual(S.discounted_return(r, g), sum(g ** k * x for k, x in enumerate(r)))

    def test_long(self):
        self.assertAlmostEqual(S.discounted_return([1.0] * 2000, 0.99), (1 - 0.99 ** 2000) / 0.01, places=6)

    def test_bad_gamma(self):
        with self.assertRaises(ValueError):
            S.discounted_return([1], 1.5)


if __name__ == "__main__":
    unittest.main()
