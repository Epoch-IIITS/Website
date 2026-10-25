"""Tests for ST-09 The Normal Distribution.

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


class TestNormal(unittest.TestCase):
    def test_pdf(self):
        self.assertAlmostEqual(S.normal_pdf(0), 1 / math.sqrt(2 * math.pi))
        self.assertAlmostEqual(S.normal_pdf(172, 170, 2), math.exp(-0.5) / (2 * math.sqrt(2 * math.pi)))
        self.assertGreater(S.normal_pdf(0, 0, 0.1), 1)

    def test_cdf(self):
        self.assertAlmostEqual(S.normal_cdf(0), 0.5)
        self.assertAlmostEqual(S.normal_cdf(180, 170, 10), 0.8413447460685429, places=12)
        self.assertAlmostEqual(S.normal_cdf(-1.5) + S.normal_cdf(1.5), 1.0)

    def test_between(self):
        self.assertAlmostEqual(S.prob_between(160, 180, 170, 10), 0.6826894921370859, places=12)
        with self.assertRaises(ValueError):
            S.prob_between(2, 1)

    def test_empirical_rule(self):
        r = S.empirical_rule()
        self.assertEqual(sorted(r), [1, 2, 3])
        self.assertAlmostEqual(r[1], 0.6827, places=4)
        self.assertAlmostEqual(r[2], 0.9545, places=4)
        self.assertAlmostEqual(r[3], 0.9973, places=4)

    def test_invalid_sigma(self):
        for f in (S.normal_pdf, S.normal_cdf):
            with self.assertRaises(ValueError):
                f(0, 0, 0)

    def test_binomial_approx_close_to_exact(self):
        exact = sum(math.comb(100, i) for i in range(56)) / 2 ** 100
        approx = S.binomial_cdf_approx(55, 100, 0.5)
        self.assertAlmostEqual(approx, S.normal_cdf(55.5, 50, 5))
        self.assertLess(abs(approx - exact), 0.002)


from statistics import NormalDist

try:
    import scipy.stats as _stats
except ImportError:
    _stats = None


class TestAgainstLibrary(unittest.TestCase):
    def test_matches_normaldist(self):
        d = NormalDist(3, 2)
        for x in (-4.0, 0.0, 3.0, 5.5):
            self.assertAlmostEqual(S.normal_pdf(x, 3, 2), d.pdf(x), places=12)
            self.assertAlmostEqual(S.normal_cdf(x, 3, 2), d.cdf(x), places=12)

    @unittest.skipIf(_stats is None, "SciPy not installed")
    def test_matches_scipy(self):
        self.assertAlmostEqual(S.normal_cdf(1.2, 0.5, 0.8), float(_stats.norm.cdf(1.2, 0.5, 0.8)), places=12)


if __name__ == "__main__":
    unittest.main()
