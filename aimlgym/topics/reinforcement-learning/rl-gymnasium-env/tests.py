"""Tests for RL-04 Gymnasium Environments.

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
from gymnasium.utils.env_checker import check_env
from gymnasium.wrappers import TimeLimit


def run(env, actions, seed=None):
    obs, _ = env.reset(seed=seed)
    states = [obs]
    for a in actions:
        obs, r, terminated, truncated, _ = env.step(a)
        states.append(obs)
        if terminated or truncated:
            return states, r, terminated, truncated
    return states, r, terminated, truncated


class TestGymnasiumEnv(unittest.TestCase):
    def test_check_env(self):
        check_env(S.LineWorldEnv(), skip_render_check=True)

    def test_spaces(self):
        env = S.LineWorldEnv(7)
        self.assertEqual((env.observation_space.n, env.action_space.n), (7, 2))

    def test_reach_goal(self):
        states, r, terminated, truncated = run(S.make_lineworld(5), [1, 1, 1, 1], seed=0)
        self.assertEqual((states, r, terminated, truncated), ([0, 1, 2, 3, 4], 1.0, True, False))

    def test_time_limit_truncates(self):
        env = S.make_lineworld(5, max_steps=6)
        self.assertIsInstance(env, TimeLimit)
        states, r, terminated, truncated = run(env, [0] * 10, seed=0)
        self.assertEqual((len(states) - 1, terminated, truncated), (6, False, True))

    def test_seeded_slip_reproducible(self):
        actions = [1] * 15
        a = run(S.make_lineworld(6, slip=0.5, max_steps=15), actions, seed=3)[0]
        b = run(S.make_lineworld(6, slip=0.5, max_steps=15), actions, seed=3)[0]
        self.assertEqual(a, b)
        self.assertTrue(all(type(s) is int for s in a))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.LineWorldEnv(1)
        env = S.LineWorldEnv()
        env.reset(seed=0)
        with self.assertRaises(ValueError):
            env.step(2)


if __name__ == "__main__":
    unittest.main()
