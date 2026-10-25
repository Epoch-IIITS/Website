"""Tests for RL-14 Q-Learning on FrozenLake.

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


import gymnasium as gym
import numpy as np


class TestFrozenLake(unittest.TestCase):
    def test_deterministic_lake_solved(self):
        env = gym.make("FrozenLake-v1", is_slippery=False)
        Q = S.q_learning(env, 300)
        self.assertEqual(S.success_rate(env, Q, episodes=20), 1.0)

    def test_slippery_lake(self):
        env = gym.make("FrozenLake-v1", is_slippery=True)
        Q = S.q_learning(env, 2000)
        self.assertGreater(S.success_rate(env, Q), 0.6)

    def test_shape_and_terminal_rows(self):
        env = gym.make("FrozenLake-v1", is_slippery=False)
        Q = S.q_learning(env, 50)
        self.assertEqual(Q.shape, (16, 4))
        for hole_or_goal in (5, 7, 11, 12, 15):
            self.assertTrue(np.all(Q[hole_or_goal] == 0))

    def test_reproducible(self):
        env = gym.make("FrozenLake-v1", is_slippery=True)
        self.assertTrue(np.array_equal(S.q_learning(env, 100, seed=3), S.q_learning(env, 100, seed=3)))

    def test_untrained_policy_fails(self):
        env = gym.make("FrozenLake-v1", is_slippery=False)
        self.assertEqual(S.success_rate(env, np.zeros((16, 4)), episodes=10), 0.0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.q_learning(gym.make("FrozenLake-v1"), 0)


if __name__ == "__main__":
    unittest.main()
