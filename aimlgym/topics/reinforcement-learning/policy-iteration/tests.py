"""Tests for RL-10 Policy Iteration.

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

def value_iteration(P, gamma):
    V = np.zeros(len(P))
    for _ in range(10000):
        Q = np.array([[sum(p * (r + gamma * (0 if d else V[s2])) for p, s2, r, d in P[s][a]) for a in range(len(P[0]))] for s in range(len(P))])
        new = Q.max(1)
        if np.max(np.abs(new - V)) < 1e-12:
            return new
        V = new
    return V

class TestPI(unittest.TestCase):
    def test_grid(self):
        V, pi, k = S.policy_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
        np.testing.assert_array_equal(pi[:3], [1, 1, 1])
        self.assertGreaterEqual(k, 2)

    def test_matches_value_iteration(self):
        P = grid_P(["S...", ".#X.", "...G"])
        V, _, _ = S.policy_iteration(P, gamma=0.95)
        np.testing.assert_allclose(V, value_iteration(P, 0.95), atol=1e-7)

    def test_stochastic(self):
        P = {0: {0: [(1.0, 0, 0.0, True)], 1: [(0.8, 1, 0.0, False), (0.2, 0, -1.0, False)]},
             1: {0: [(1.0, 1, 5.0, True)], 1: [(1.0, 1, 1.0, True)]}}
        V, pi, _ = S.policy_iteration(P, gamma=0.9)
        self.assertEqual(pi.tolist(), [1, 0])
        self.assertAlmostEqual(V[0], (0.8 * 0.9 * 5 - 0.2) / (1 - 0.2 * 0.9), places=8)

    def test_already_optimal_one_cycle(self):
        P = {0: {0: [(1.0, 0, 1.0, True)], 1: [(1.0, 0, 0.0, True)]}}
        _, pi, k = S.policy_iteration(P)
        self.assertEqual((pi.tolist(), k), ([0], 1))

    def test_avoid_pit(self):
        _, pi, _ = S.policy_iteration(grid_P(["S.X", "...", "..G"]), gamma=0.9)
        self.assertEqual(pi[1], 2)

    def test_bad_gamma(self):
        with self.assertRaises(ValueError):
            S.policy_iteration(grid_P(["SG"]), gamma=1.0)


if __name__ == "__main__":
    unittest.main()
