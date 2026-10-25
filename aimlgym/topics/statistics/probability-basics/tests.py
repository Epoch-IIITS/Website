"""Tests for ST-06 Probability by Counting Outcomes.

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


from fractions import Fraction


class TestProbability(unittest.TestCase):
    def setUp(self):
        self.space = S.two_dice()

    def test_space(self):
        self.assertEqual(len(self.space), 36)
        self.assertEqual(self.space[:3], [(1, 1), (1, 2), (1, 3)])
        self.assertEqual(self.space[-1], (6, 6))

    def test_probability_exact(self):
        p = S.probability(self.space, lambda o: sum(o) == 7)
        self.assertIsInstance(p, Fraction)
        self.assertEqual(p, Fraction(1, 6))
        self.assertEqual(S.probability(self.space, lambda o: sum(o) == 13), 0)

    def test_complement(self):
        self.assertEqual(S.complement(self.space, lambda o: o == (6, 6)), Fraction(35, 36))

    def test_union_overlap(self):
        p = S.union(self.space, lambda o: o[0] == 6, lambda o: o[1] == 6)
        self.assertEqual(p, Fraction(11, 36))

    def test_union_matches_direct_count(self):
        a = lambda o: sum(o) >= 10
        b = lambda o: o[0] == o[1]
        direct = S.probability(self.space, lambda o: a(o) or b(o))
        self.assertEqual(S.union(self.space, a, b), direct)

    def test_independence(self):
        even_first = lambda o: o[0] % 2 == 0
        self.assertTrue(S.independent(self.space, even_first, lambda o: sum(o) == 7))
        self.assertFalse(S.independent(self.space, even_first, lambda o: sum(o) == 12))
        coin = ["H", "T"]
        self.assertFalse(S.independent(coin, lambda o: o == "H", lambda o: o == "T"))

    def test_empty_space(self):
        with self.assertRaises(ValueError):
            S.probability([], lambda o: True)


import itertools


class TestAgainstLibrary(unittest.TestCase):
    def test_space_matches_itertools(self):
        self.assertEqual(S.two_dice(), list(itertools.product(range(1, 7), repeat=2)))


if __name__ == "__main__":
    unittest.main()
