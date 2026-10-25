"""Tests for FL-08 Seeded Client Sampling.

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


import numpy as np

class TestSampling(unittest.TestCase):
    def test_count_distinct(self):
        s = S.sample_clients(10, 0.3, 0, 0)
        self.assertEqual(len(s), 3)
        self.assertEqual(len(set(s.tolist())), 3)

    def test_full(self):
        np.testing.assert_array_equal(S.sample_clients(10, 1.0, 0, 5), np.arange(10))

    def test_min_one(self):
        self.assertEqual(len(S.sample_clients(100, 0.001, 1, 0)), 1)

    def test_recipe_and_round_independence(self):
        exp = np.sort(np.random.default_rng([3, 7]).choice(20, 5, replace=False))
        np.testing.assert_array_equal(S.sample_clients(20, 0.25, 3, 7), exp)

    def test_sorted_range(self):
        s = S.sample_clients(50, 0.2, 2, 4)
        self.assertTrue((np.diff(s) > 0).all() and s.min() >= 0 and s.max() < 50)

    def test_participation_rate(self):
        counts = np.zeros(10)
        for r in range(3000):
            counts[S.sample_clients(10, 0.3, 0, r)] += 1
        np.testing.assert_allclose(counts / 3000, 0.3, atol=0.03)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.sample_clients(10, 0.0, 0, 0)


if __name__ == "__main__":
    unittest.main()
