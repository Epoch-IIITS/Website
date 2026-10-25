"""Tests for RL-15 SARSA.

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

# Cliff walking (Sutton & Barto Example 6.6, scaled down): 3 x 6 grid, start bottom-left,
# goal bottom-right, the bottom cells between them are a cliff (-100, back to start).
R, C = 3, 6
START, GOAL = (R - 1) * C, R * C - 1
CLIFF = set(range(START + 1, GOAL))
MOVES = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
def cliff_step(s, a):
    r, c = divmod(s, C); dr, dc = MOVES[a]; nr, nc = r + dr, c + dc
    if not (0 <= nr < R and 0 <= nc < C):
        nr, nc = r, c
    ns = nr * C + nc
    if ns in CLIFF:
        return START, -100.0, False
    if ns == GOAL:
        return GOAL, 0.0, True
    return ns, -1.0, False

def q_learning_ref(env_step, start, nS, nA, episodes, alpha, gamma, eps, seed, max_steps):
    rng = np.random.default_rng(seed); Q = np.zeros((nS, nA))
    for _ in range(episodes):
        s = start
        for _ in range(max_steps):
            a = int(rng.integers(nA)) if rng.random() < eps else int(np.argmax(Q[s]))
            s2, r, d = env_step(s, a)
            Q[s, a] += alpha * (r + (0 if d else gamma * Q[s2].max()) - Q[s, a]); s = s2
            if d:
                break
    return Q

def greedy_rows(Q):
    s, rows = START, []
    for _ in range(40):
        s, _, d = cliff_step(s, int(np.argmax(Q[s]))); rows.append(s // C)
        if d:
            return rows, True
    return rows, False

class TestSARSA(unittest.TestCase):
    def test_update(self):
        Q = np.zeros((2, 2)); Q[1] = [5., 2.]
        d = S.sarsa_update(Q, 0, 1, -1.0, 1, 1, False, 0.5, 0.9)
        self.assertAlmostEqual(Q[0, 1], 0.4)
        self.assertAlmostEqual(d, 0.8)

    def test_update_terminal(self):
        Q = np.ones((2, 2)) * 50
        S.sarsa_update(Q, 0, 0, 2.0, 1, 0, True, 0.5, 0.9)
        self.assertAlmostEqual(Q[0, 0], 26.0)

    def test_corridor(self):
        Q, _ = S.sarsa(corridor_step, 0, 4, 2, 400, 0.5, 0.9, 0.1, 0)
        np.testing.assert_array_equal(Q[:3].argmax(axis=1), [1, 1, 1])

    def test_cliff_safe_path_vs_qlearning(self):
        Qs, _ = S.sarsa(cliff_step, START, R * C, 4, 3000, 0.1, 1.0, 0.1, 0, max_steps=500)
        Qq = q_learning_ref(cliff_step, START, R * C, 4, 3000, 0.1, 1.0, 0.1, 0, 500)
        rs, ok_s = greedy_rows(Qs)
        rq, ok_q = greedy_rows(Qq)
        self.assertTrue(ok_s and ok_q)
        self.assertEqual(min(rs), 0)   # SARSA detours through the far (safe) row
        self.assertEqual(min(rq), 1)   # Q-learning walks along the cliff edge

    def test_returns_len(self):
        _, rets = S.sarsa(corridor_step, 0, 4, 2, 37, 0.5, 0.9, 0.1, 1)
        self.assertEqual(len(rets), 37)

    def test_reproducible(self):
        a = S.sarsa(corridor_step, 0, 4, 2, 30, 0.5, 0.9, 0.3, 5)[0]
        np.testing.assert_array_equal(a, S.sarsa(corridor_step, 0, 4, 2, 30, 0.5, 0.9, 0.3, 5)[0])


if __name__ == "__main__":
    unittest.main()
