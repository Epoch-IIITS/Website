"""Tests for RL-05 Epsilon-Greedy Action Selection.

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

class TestEpsGreedy(unittest.TestCase):
    def test_probs(self):
        np.testing.assert_allclose(S.epsilon_greedy_probs([1, 5, 2], 0.3), [0.1, 0.8, 0.1])

    def test_greedy(self):
        self.assertEqual(S.epsilon_greedy([1, 5, 2], 0.0, np.random.default_rng(0)), 1)

    def test_ties_lowest(self):
        self.assertEqual(S.epsilon_greedy([3, 3, 1], 0.0, np.random.default_rng(0)), 0)

    def test_recipe(self):
        rng_a, rng_b = np.random.default_rng(5), np.random.default_rng(5)
        for _ in range(50):
            got = S.epsilon_greedy([0., 1., 0.5, 0.2], 0.4, rng_a)
            exp = int(rng_b.integers(4)) if rng_b.random() < 0.4 else 1
            self.assertEqual(got, exp)

    def test_frequencies(self):
        rng = np.random.default_rng(1)
        counts = np.bincount([S.epsilon_greedy([1, 5, 2], 0.3, rng) for _ in range(30000)], minlength=3) / 30000
        np.testing.assert_allclose(counts, [0.1, 0.8, 0.1], atol=0.01)

    def test_full_exploration(self):
        np.testing.assert_allclose(S.epsilon_greedy_probs([9, 0, 0, 0], 1.0), 0.25)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.epsilon_greedy_probs([], 0.1)
        with self.assertRaises(ValueError):
            S.epsilon_greedy([1], 1.5, np.random.default_rng(0))


if __name__ == "__main__":
    unittest.main()
