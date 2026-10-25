"""Tests for RL-07 UCB1 Bandit.

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

class TestUCB(unittest.TestCase):
    def test_select(self):
        self.assertEqual(S.ucb_select(np.array([0.5, 0.4]), np.array([10, 2]), 13), 1)

    def test_untried_first(self):
        self.assertEqual(S.ucb_select(np.array([9., 0., 0.]), np.array([5, 3, 0]), 9), 2)
        self.assertEqual(S.ucb_select(np.zeros(3), np.zeros(3, int), 1), 0)

    def test_exploit_when_confident(self):
        self.assertEqual(S.ucb_select(np.array([0.9, 0.1]), np.array([1000, 1000]), 2001), 0)

    def test_learns_best(self):
        r = S.run_bandit([0.2, 0.8], 1000, seed=0)
        self.assertGreater(r["actions"].count(1), 900)

    def test_regret_definition(self):
        r = S.run_bandit([0.1, 0.5, 0.3], 200, seed=4)
        means = np.array([0.1, 0.5, 0.3])
        self.assertAlmostEqual(r["regret"], 200 * 0.5 - means[r["actions"]].sum())

    def test_ucb_beats_egreedy(self):
        means = [0.2, 0.8]
        ucb = np.mean([S.run_bandit(means, 3000, s)["regret"] for s in range(5)])
        eg = np.mean([S.run_bandit(means, 3000, s, policy="egreedy", epsilon=0.3)["regret"] for s in range(5)])
        self.assertLess(ucb, eg)

    def test_reproducible(self):
        a = S.run_bandit([0.3, 0.6], 100, 9)
        self.assertEqual(a, S.run_bandit([0.3, 0.6], 100, 9))


if __name__ == "__main__":
    unittest.main()
