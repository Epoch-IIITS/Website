"""Tests for ST-07 Conditional Probability and Bayes' Rule.

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

DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]


class TestBayes(unittest.TestCase):
    def test_conditional_dice(self):
        self.assertEqual(S.conditional(DICE, lambda o: sum(o) == 8, lambda o: o[0] == 6), Fraction(1, 6))
        self.assertEqual(S.conditional(DICE, lambda o: o[0] == 6, lambda o: sum(o) == 12), 1)

    def test_conditional_matches_definition(self):
        a = lambda o: o[0] > o[1]
        b = lambda o: sum(o) >= 9
        both = Fraction(sum(1 for o in DICE if a(o) and b(o)), 36)
        pb = Fraction(sum(1 for o in DICE if b(o)), 36)
        self.assertEqual(S.conditional(DICE, a, b), both / pb)

    def test_conditional_zero(self):
        with self.assertRaises(ValueError):
            S.conditional(DICE, lambda o: True, lambda o: sum(o) > 12)

    def test_posterior_base_rate(self):
        self.assertAlmostEqual(S.posterior(0.01, 0.9, 0.05), 0.009 / 0.0585, places=12)

    def test_posterior_edge(self):
        self.assertAlmostEqual(S.posterior(0.5, 0.8, 0.8), 0.5)
        self.assertAlmostEqual(S.posterior(0.2, 1.0, 0.0), 1.0)

    def test_update_two_positives(self):
        p1 = S.posterior(0.01, 0.9, 0.05)
        self.assertAlmostEqual(S.update(0.01, 0.9, 0.05, [True, True]), S.posterior(p1, 0.9, 0.05))
        self.assertAlmostEqual(S.update(0.01, 0.9, 0.05, [True, True]), 0.7659574468, places=8)

    def test_update_negative_and_empty(self):
        self.assertEqual(S.update(0.3, 0.9, 0.05, []), 0.3)
        neg = S.update(0.3, 0.9, 0.05, [False])
        self.assertAlmostEqual(neg, 0.1 * 0.3 / (0.1 * 0.3 + 0.95 * 0.7))
        self.assertLess(neg, 0.3)


if __name__ == "__main__":
    unittest.main()
