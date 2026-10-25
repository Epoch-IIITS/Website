"""Tests for ST-14 Introducing scipy.stats.

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


class TestDistributionFacts(unittest.TestCase):
    def test_normal_matches_formulas(self):
        r = S.distribution_facts("norm", (170, 10), 180, 0.975)
        self.assertAlmostEqual(r["cdf"], 0.5 * (1 + math.erf(1 / math.sqrt(2))), places=10)
        self.assertAlmostEqual(r["density"], math.exp(-0.5) / (10 * math.sqrt(2 * math.pi)), places=12)
        self.assertAlmostEqual(r["quantile"], 170 + 10 * 1.959963984540054, places=6)

    def test_binomial_matches_formulas(self):
        r = S.distribution_facts("binom", (10, 0.5), 5, 0.5)
        self.assertAlmostEqual(r["density"], math.comb(10, 5) / 2 ** 10, places=12)
        self.assertAlmostEqual(r["cdf"], sum(math.comb(10, k) for k in range(6)) / 2 ** 10, places=12)
        self.assertEqual(r["quantile"], 5.0)

    def test_mean_and_std(self):
        r = S.distribution_facts("binom", (20, 0.3), 6, 0.5)
        self.assertAlmostEqual(r["mean"], 6.0)
        self.assertAlmostEqual(r["std"], math.sqrt(20 * 0.3 * 0.7))

    def test_plain_floats(self):
        r = S.distribution_facts("norm", (0, 1), 0, 0.5)
        self.assertEqual(set(r), {"density", "cdf", "quantile", "mean", "std"})
        self.assertTrue(all(type(v) is float for v in r.values()))
        self.assertAlmostEqual(r["quantile"], 0.0)

    def test_standard_normal_symmetry(self):
        low = S.distribution_facts("norm", (0, 1), -1.5, 0.1)
        high = S.distribution_facts("norm", (0, 1), 1.5, 0.9)
        self.assertAlmostEqual(low["cdf"] + high["cdf"], 1.0, places=12)
        self.assertAlmostEqual(low["quantile"], -high["quantile"], places=9)

    def test_invalid_parameters(self):
        for args in [("norm", (0, 0), 0, 0.5), ("binom", (10, 1.5), 1, 0.5), ("binom", (-1, 0.5), 0, 0.5),
                     ("norm", (0, 1), 0, 1.0), ("poisson", (3,), 1, 0.5)]:
            with self.assertRaises(ValueError):
                S.distribution_facts(*args)


if __name__ == "__main__":
    unittest.main()
