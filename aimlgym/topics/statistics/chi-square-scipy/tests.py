"""Tests for ST-15 Chi-Square Test with SciPy.

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


class TestChiSquareSciPy(unittest.TestCase):
    def test_die(self):
        r = S.chi_square_test([5, 8, 9, 8, 10, 20], [1 / 6] * 6)
        self.assertAlmostEqual(r["statistic"], 13.4, places=9)
        self.assertEqual(r["df"], 5)
        self.assertAlmostEqual(r["p_value"], 0.019905220334774, places=9)
        self.assertTrue(r["reject"])

    def test_stricter_alpha(self):
        self.assertFalse(S.chi_square_test([5, 8, 9, 8, 10, 20], [1 / 6] * 6, alpha=0.01)["reject"])

    def test_perfect_fit(self):
        r = S.chi_square_test([50, 50], [0.5, 0.5])
        self.assertEqual(r["statistic"], 0.0)
        self.assertAlmostEqual(r["p_value"], 1.0)
        self.assertFalse(r["reject"])

    def test_p_value_is_upper_tail(self):
        from scipy import stats
        r = S.chi_square_test([30, 50, 20], [0.25, 0.5, 0.25])
        self.assertAlmostEqual(r["statistic"], 2.0)
        self.assertAlmostEqual(r["p_value"], stats.chi2(2).sf(2.0), places=12)

    def test_plain_types(self):
        r = S.chi_square_test([18, 22, 20], [1 / 3] * 3)
        self.assertIs(type(r["statistic"]), float)
        self.assertIs(type(r["p_value"]), float)
        self.assertIs(type(r["reject"]), bool)

    def test_invalid_inputs(self):
        for args in [([1, 2], [0.5, 0.6]), ([1, 2, 3], [0.5, 0.5]), ([0, 0], [0.5, 0.5]),
                     ([3, -1], [0.5, 0.5]), ([5], [1.0])]:
            with self.assertRaises(ValueError):
                S.chi_square_test(*args)
        with self.assertRaises(ValueError):
            S.chi_square_test([5, 5], [0.5, 0.5], alpha=1.5)


if __name__ == "__main__":
    unittest.main()
