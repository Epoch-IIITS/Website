"""Tests for ST-20 Permutation Test for a Mean Difference by Hand.

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

class TestPermutation(unittest.TestCase):
    def test_fy_recipe(self):
        rng = random.Random(0)
        a = [0, 1, 2, 3, 4]
        for i in range(4, 0, -1):
            j = int(rng.random() * (i + 1)); a[i], a[j] = a[j], a[i]
        self.assertEqual(S.fisher_yates([0, 1, 2, 3, 4], random.Random(0)), a)

    def test_fy_is_permutation_and_copy(self):
        items = list(range(20))
        out = S.fisher_yates(items, random.Random(5))
        self.assertEqual(sorted(out), items)
        self.assertEqual(items, list(range(20)))

    def test_fy_uniform_first_position(self):
        rng = random.Random(1)
        counts = [0, 0, 0]
        for _ in range(30000):
            counts[S.fisher_yates([0, 1, 2], rng)[0]] += 1
        for c in counts:
            self.assertAlmostEqual(c / 30000, 1 / 3, delta=0.015)

    def test_exact_p_approx(self):
        r = S.permutation_test([5, 6, 7], [1, 2, 3], n_perm=4000, seed=0)
        self.assertAlmostEqual(r["observed"], 4.0)
        self.assertAlmostEqual(r["p_value"], 0.1, delta=0.02)

    def test_identical_groups(self):
        self.assertEqual(S.permutation_test([1, 2, 3], [1, 2, 3], n_perm=100)["p_value"], 1.0)

    def test_p_never_zero(self):
        r = S.permutation_test([100, 101, 102, 103], [0, 1, 2, 3], n_perm=10, seed=3)
        self.assertGreater(r["p_value"], 0)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.permutation_test([], [1])


if __name__ == "__main__":
    unittest.main()
