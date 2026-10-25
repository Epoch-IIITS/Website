"""Tests for ST-19 Permutation Test with SciPy.

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


import itertools


def brute_force_p(x, y):
    """Exact two-sided p-value: the share of all splits with |difference| at least the observed."""
    values, k = list(x) + list(y), len(x)
    observed = abs(sum(x) / len(x) - sum(y) / len(y))
    hits = total = 0
    for chosen in itertools.combinations(range(len(values)), k):
        a = [values[i] for i in chosen]
        b = [values[i] for i in range(len(values)) if i not in chosen]
        total += 1
        hits += abs(sum(a) / len(a) - sum(b) / len(b)) >= observed - 1e-12
    return hits / total


class TestPermutationSciPy(unittest.TestCase):
    def test_exact_small_sample(self):
        r = S.permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5])
        self.assertAlmostEqual(r["statistic"], -2.1)
        self.assertAlmostEqual(r["p_value"], brute_force_p([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5]), places=9)

    def test_identical_groups(self):
        r = S.permutation_mean_diff([1, 2, 3], [1, 2, 3])
        self.assertEqual(r["statistic"], 0.0)
        self.assertAlmostEqual(r["p_value"], 1.0)

    def test_one_sided(self):
        less = S.permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5], alternative="less")
        greater = S.permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5], alternative="greater")
        self.assertLess(less["p_value"], greater["p_value"])
        self.assertAlmostEqual(less["p_value"], 16 / 252, places=9)

    def test_reproducible_with_seed(self):
        x = [0.1 * i for i in range(20)]
        y = [0.1 * i + 0.4 for i in range(20)]
        a = S.permutation_mean_diff(x, y, n_resamples=500, seed=3)
        b = S.permutation_mean_diff(x, y, n_resamples=500, seed=3)
        self.assertEqual(a, b)

    def test_large_shift_is_significant(self):
        x = [10 + 0.01 * i for i in range(12)]
        y = [0.01 * i for i in range(12)]
        r = S.permutation_mean_diff(x, y, n_resamples=999, seed=0)
        self.assertLess(r["p_value"], 0.01)
        self.assertAlmostEqual(r["statistic"], 10.0)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            S.permutation_mean_diff([], [1, 2])
        with self.assertRaises(ValueError):
            S.permutation_mean_diff([1, 2], [3, 4], alternative="sideways")


if __name__ == "__main__":
    unittest.main()
