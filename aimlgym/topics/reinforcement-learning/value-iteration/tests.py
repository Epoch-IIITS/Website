"""Tests for RL-09 Value Iteration.

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

MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

def grid_P(rows):
    R, C = len(rows), len(rows[0]); P = {}
    for s in range(R * C):
        r, c = divmod(s, C); ch = rows[r][c]; P[s] = {}
        for a, (dr, dc) in MOVES.items():
            if ch in "#GX":
                P[s][a] = [(1.0, s, 0.0, True)]; continue
            nr, nc = r + dr, c + dc
            ns = nr * C + nc if 0 <= nr < R and 0 <= nc < C and rows[nr][nc] != "#" else s
            t = rows[ns // C][ns % C]
            P[s][a] = [(1.0, ns, 10.0, True)] if t == "G" else [(1.0, ns, -10.0, True)] if t == "X" else [(1.0, ns, -1.0, False)]
    return P

class TestVI(unittest.TestCase):
    def test_grid_policy(self):
        V, pi = S.value_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
        self.assertEqual((pi[0], pi[1], pi[2]), (1, 1, 1))
        self.assertEqual(pi[6], 0)

    def test_grid_values(self):
        V, _ = S.value_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
        self.assertAlmostEqual(V[2], 10.0)
        self.assertAlmostEqual(V[1], -1 + 0.9 * 10)
        self.assertAlmostEqual(V[0], -1 + 0.9 * (-1 + 9))

    def test_q_from_v(self):
        P = {0: {0: [(1.0, 1, 2.0, False)], 1: [(0.5, 1, 0.0, False), (0.5, 0, 4.0, True)]}, 1: {0: [(1.0, 1, 0.0, True)], 1: [(1.0, 1, 0.0, True)]}}
        Q = S.q_from_v(P, np.array([0.0, 10.0]), 0.5)
        np.testing.assert_allclose(Q, [[7.0, 4.5], [0.0, 0.0]])

    def test_bellman_optimality(self):
        P = grid_P(["S..", ".X.", "..G"])
        V, _ = S.value_iteration(P, gamma=0.95)
        np.testing.assert_allclose(V, S.q_from_v(P, V, 0.95).max(axis=1), atol=1e-8)

    def test_avoids_pit(self):
        _, pi = S.value_iteration(grid_P(["S.X", "...", "..G"]), gamma=0.9)
        self.assertEqual(pi[1], 2)

    def test_ties_lowest(self):
        P = {0: {0: [(1.0, 0, 1.0, True)], 1: [(1.0, 0, 1.0, True)]}}
        self.assertEqual(S.value_iteration(P)[1][0], 0)


if __name__ == "__main__":
    unittest.main()
