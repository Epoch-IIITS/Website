"""Tests for RL-03 The Environment Interface: reset and step.

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

RIGHT = lambda obs: 1
LEFT = lambda obs: 0


class TestLineWorld(unittest.TestCase):
    def test_reset(self):
        env = S.LineWorld(n=5, start=1)
        self.assertEqual(env.reset(), (1, {"steps": 0}))

    def test_reach_goal(self):
        env = S.LineWorld()
        env.reset()
        out = [env.step(1) for _ in range(4)]
        self.assertEqual(out[-1], (4, 1.0, True, False, {"steps": 4}))
        self.assertEqual([o[1] for o in out[:-1]], [0.0, 0.0, 0.0])

    def test_wall_and_truncation(self):
        env = S.LineWorld(max_steps=3)
        env.reset()
        results = [env.step(0) for _ in range(3)]
        self.assertEqual([r[0] for r in results], [0, 0, 0])
        self.assertEqual(results[-1][2:4], (False, True))
        with self.assertRaises(RuntimeError):
            env.step(0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            S.LineWorld(n=1)
        with self.assertRaises(ValueError):
            S.LineWorld(start=4)
        env = S.LineWorld()
        env.reset()
        with self.assertRaises(ValueError):
            env.step(2)

    def test_run_episode(self):
        self.assertEqual(S.run_episode(S.LineWorld(), RIGHT), (1.0, 4, True))
        self.assertEqual(S.run_episode(S.LineWorld(max_steps=7), LEFT), (0.0, 7, False))

    def test_slip_reproducible(self):
        env = S.LineWorld(n=6, slip=0.3, max_steps=50)
        a = [S.run_episode(env, RIGHT, seed=5) for _ in range(2)]
        self.assertEqual(a[0], a[1])
        rng = np.random.default_rng(5)
        state, steps = 0, 0
        while state != 5 and steps < 50:
            move = -1 if rng.random() < 0.3 else 1
            state = max(0, min(5, state + move))
            steps += 1
        self.assertEqual(a[0][1], steps)

    def test_reset_restarts_episode(self):
        env = S.LineWorld(max_steps=2)
        S.run_episode(env, LEFT)
        obs, info = env.reset()
        self.assertEqual((obs, info["steps"]), (0, 0))
        self.assertEqual(env.step(1)[0], 1)


if __name__ == "__main__":
    unittest.main()
