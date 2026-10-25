"""Tests for ST-12 Sampling Distributions and Standard Error.

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


import random
import statistics


def reference_means(population, n, reps, seed):
    rng = random.Random(seed)
    out = []
    for _ in range(reps):
        out.append(sum(population[int(rng.random() * len(population))] for _ in range(n)) / n)
    return out


class TestSamplingDistribution(unittest.TestCase):
    def test_recipe_matches(self):
        pop = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual(S.sample_means(pop, 5, 50, seed=11), reference_means(pop, 5, 50, 11))

    def test_reproducible(self):
        a = S.sample_means([1, 2, 3], 4, 10, seed=3)
        self.assertEqual(a, S.sample_means([1, 2, 3], 4, 10, seed=3))
        self.assertNotEqual(a, S.sample_means([1, 2, 3], 4, 10, seed=4))

    def test_spread_shrinks_like_sqrt_n(self):
        die = [1, 2, 3, 4, 5, 6]
        sigma = statistics.pstdev(die)
        for n in (4, 25):
            sd = statistics.pstdev(S.sample_means(die, n, 3000, seed=1))
            self.assertAlmostEqual(sd / (sigma / math.sqrt(n)), 1.0, delta=0.06)

    def test_centre(self):
        means = S.sample_means([1, 2, 3, 4, 5, 6], 10, 3000, seed=2)
        self.assertAlmostEqual(statistics.fmean(means), 3.5, delta=0.05)

    def test_standard_error(self):
        self.assertAlmostEqual(S.standard_error([2, 4, 4, 4, 5, 5, 7, 9]), statistics.stdev([2, 4, 4, 4, 5, 5, 7, 9]) / math.sqrt(8))
        with self.assertRaises(ValueError):
            S.standard_error([1])

    def test_ci95(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        low, high = S.mean_ci95(data)
        se = S.standard_error(data)
        self.assertAlmostEqual((low + high) / 2, 5.0)
        self.assertAlmostEqual(high - low, 2 * 1.959963984540054 * se, places=9)


try:
    import scipy.stats as _stats
except ImportError:
    _stats = None


class TestAgainstLibrary(unittest.TestCase):
    def test_matches_statistics_stdev(self):
        data = [1.2, 3.4, 2.2, 5.0, 4.1]
        self.assertAlmostEqual(S.standard_error(data), statistics.stdev(data) / math.sqrt(5), places=12)

    @unittest.skipIf(_stats is None, "SciPy not installed")
    def test_matches_scipy_sem(self):
        data = [1.2, 3.4, 2.2, 5.0, 4.1]
        self.assertAlmostEqual(S.standard_error(data), float(_stats.sem(data)), places=12)


if __name__ == "__main__":
    unittest.main()
