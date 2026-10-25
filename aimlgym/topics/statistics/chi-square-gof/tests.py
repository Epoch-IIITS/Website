"""Tests for ST-16 Chi-Square Goodness of Fit by Hand.

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


class TestChi(unittest.TestCase):
    def test_die(self):
        r = S.chi_square_gof([5, 8, 9, 8, 10, 20], [1 / 6] * 6, critical=11.070)
        self.assertAlmostEqual(r["statistic"], 13.4, places=9)
        self.assertEqual(r["df"], 5)
        self.assertTrue(r["reject"])
        for e in r["expected"]:
            self.assertAlmostEqual(e, 10.0)

    def test_perfect_fit(self):
        r = S.chi_square_gof([50, 50], [0.5, 0.5])
        self.assertEqual(r["statistic"], 0.0)
        self.assertIsNone(r["reject"])

    def test_not_reject(self):
        r = S.chi_square_gof([18, 22, 20], [1 / 3] * 3, critical=5.991)
        self.assertAlmostEqual(r["statistic"], 0.4)
        self.assertFalse(r["reject"])

    def test_unequal_probs(self):
        r = S.chi_square_gof([30, 50, 20], [0.25, 0.5, 0.25])
        self.assertAlmostEqual(r["statistic"], (25 / 25) + 0 + (25 / 25))

    def test_bad_probs(self):
        with self.assertRaises(ValueError):
            S.chi_square_gof([1, 2], [0.5, 0.6])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.chi_square_gof([1, 2, 3], [0.5, 0.5])

    def test_zero_total(self):
        with self.assertRaises(ValueError):
            S.chi_square_gof([0, 0], [0.5, 0.5])


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy_chisquare(self):
        from scipy.stats import chisquare
        observed, probs = [18, 22, 30, 30], [0.25, 0.25, 0.25, 0.25]
        res = S.chi_square_gof(observed, probs)
        ref = chisquare(observed, f_exp=res["expected"])
        self.assertAlmostEqual(res["statistic"], float(ref.statistic), places=10)


if __name__ == "__main__":
    unittest.main()
