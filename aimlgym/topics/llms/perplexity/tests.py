"""Tests for LM-05 Perplexity.

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


class TestPPL(unittest.TestCase):
    def test_example(self):
        self.assertAlmostEqual(S.perplexity([0.5, 0.25, 0.125]), 4.0)

    def test_uniform(self):
        self.assertAlmostEqual(S.perplexity([0.1] * 7), 10.0)

    def test_zero(self):
        self.assertEqual(S.perplexity([0.9, 0.0]), math.inf)
        self.assertEqual(S.avg_nll([0.0]), math.inf)

    def test_perfect(self):
        self.assertEqual(S.perplexity([1.0, 1.0]), 1.0)

    def test_nll_value(self):
        self.assertAlmostEqual(S.avg_nll([0.5, 0.25, 0.125]), 2 * math.log(2))

    def test_not_mean_of_probs(self):
        self.assertNotAlmostEqual(S.perplexity([0.9, 0.1]), 1 / 0.5)
        self.assertAlmostEqual(S.perplexity([0.9, 0.1]), 1 / math.sqrt(0.09))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.perplexity([])
        with self.assertRaises(ValueError):
            S.perplexity([1.2])


if __name__ == "__main__":
    unittest.main()
