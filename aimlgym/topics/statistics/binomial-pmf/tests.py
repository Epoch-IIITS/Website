"""Tests for ST-08 Binomial Probabilities.

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


class TestBinom(unittest.TestCase):
    def test_pmf(self):
        self.assertAlmostEqual(S.binom_pmf(2, 4, 0.5), 0.375)

    def test_at_least(self):
        self.assertAlmostEqual(S.prob_at_least(3, 4, 0.5), 0.3125)

    def test_cdf_full(self):
        self.assertEqual(S.binom_cdf(10, 10, 0.3), 1.0)

    def test_out_of_range_k(self):
        self.assertEqual(S.binom_pmf(5, 4, 0.5), 0.0)
        self.assertEqual(S.binom_pmf(-1, 4, 0.5), 0.0)

    def test_sums_to_one(self):
        self.assertAlmostEqual(sum(S.binom_pmf(k, 12, 0.37) for k in range(13)), 1.0, places=12)

    def test_mean(self):
        n, p = 9, 0.2
        self.assertAlmostEqual(sum(k * S.binom_pmf(k, n, p) for k in range(n + 1)), n * p, places=12)

    def test_edge_p(self):
        self.assertEqual(S.binom_pmf(0, 5, 0.0), 1.0)
        self.assertEqual(S.binom_pmf(5, 5, 1.0), 1.0)

    def test_at_least_zero(self):
        self.assertAlmostEqual(S.prob_at_least(0, 7, 0.4), 1.0)

    def test_bad_p(self):
        with self.assertRaises(ValueError):
            S.binom_pmf(1, 3, 1.5)


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy_binom(self):
        from scipy.stats import binom
        for k in (0, 3, 7, 12):
            self.assertAlmostEqual(S.binom_pmf(k, 12, 0.35), float(binom.pmf(k, 12, 0.35)), places=12)
            self.assertAlmostEqual(S.binom_cdf(k, 12, 0.35), float(binom.cdf(k, 12, 0.35)), places=12)
            self.assertAlmostEqual(S.prob_at_least(k, 12, 0.35), float(binom.sf(k - 1, 12, 0.35)), places=12)


if __name__ == "__main__":
    unittest.main()
