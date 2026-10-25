"""Tests for RL-13 Tabular Q-Learning.

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

def corridor_step(s, a):
    s2 = min(s + 1, 3) if a == 1 else max(s - 1, 0)
    return (s2, 10.0, True) if s2 == 3 else (s2, -1.0, False)

MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
ROWS = ["S..", ".X.", "..G"]

def grid_step(s, a):
    r, c = divmod(s, 3); dr, dc = MOVES[a]; nr, nc = r + dr, c + dc
    ns = nr * 3 + nc if 0 <= nr < 3 and 0 <= nc < 3 else s
    ch = ROWS[ns // 3][ns % 3]
    return (ns, 10.0, True) if ch == "G" else (ns, -10.0, True) if ch == "X" else (ns, -1.0, False)

class TestQL(unittest.TestCase):
    def test_update(self):
        Q = np.zeros((2, 2)); Q[1] = [5.0, 2.0]
        d = S.q_update(Q, 0, 1, -1.0, 1, False, 0.5, 0.9)
        self.assertAlmostEqual(Q[0, 1], 1.75)
        self.assertAlmostEqual(d, 3.5)

    def test_update_terminal(self):
        Q = np.zeros((2, 2)); Q[1] = [100.0, 100.0]
        S.q_update(Q, 0, 0, 1.0, 1, True, 1.0, 0.9)
        self.assertEqual(Q[0, 0], 1.0)

    def test_corridor_policy(self):
        Q, _ = S.q_learning(corridor_step, 0, 4, 2, 300, 0.5, 0.9, 0.1, 0)
        np.testing.assert_array_equal(Q[:3].argmax(axis=1), [1, 1, 1])

    def test_corridor_values(self):
        Q, _ = S.q_learning(corridor_step, 0, 4, 2, 2000, 0.5, 0.9, 0.2, 1)
        np.testing.assert_allclose(Q[:3, 1], [-1 + 0.9 * (-1 + 9), -1 + 9, 10], atol=1e-3)

    def test_grid_avoids_pit(self):
        Q, rets = S.q_learning(grid_step, 0, 9, 4, 800, 0.5, 0.95, 0.1, 0)
        s, path = 0, []
        for _ in range(10):
            s, r, done = grid_step(s, int(np.argmax(Q[s]))); path.append(s)
            if done:
                break
        self.assertEqual(path[-1], 8)
        self.assertNotIn(4, path)

    def test_returns_improve(self):
        _, rets = S.q_learning(corridor_step, 0, 4, 2, 200, 0.5, 0.9, 0.1, 2)
        self.assertEqual(len(rets), 200)
        self.assertGreater(np.mean(rets[-20:]), np.mean(rets[:5]))

    def test_reproducible(self):
        a = S.q_learning(corridor_step, 0, 4, 2, 50, 0.5, 0.9, 0.3, 7)[0]
        np.testing.assert_array_equal(a, S.q_learning(corridor_step, 0, 4, 2, 50, 0.5, 0.9, 0.3, 7)[0])


if __name__ == "__main__":
    unittest.main()
