"""Tests for AG-11 BFS Planner.

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


G = {"hall": [("go kitchen", "kitchen"), ("go study", "study")], "kitchen": [("go garden", "garden")],
     "study": [("go garden", "garden")], "garden": []}

def grid_succ(walls, n):
    def succ(s):
        r, c = s; out = []
        for name, (dr, dc) in [("up", (-1, 0)), ("right", (0, 1)), ("down", (1, 0)), ("left", (0, -1))]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in walls:
                out.append((name, (nr, nc)))
        return out
    return succ

class TestBFS(unittest.TestCase):
    def test_rooms(self):
        r = S.bfs_plan("hall", lambda s: s == "garden", lambda s: G[s])
        self.assertEqual(r["actions"], ["go kitchen", "go garden"])
        self.assertEqual(r["states"], ["hall", "kitchen", "garden"])

    def test_start_is_goal(self):
        r = S.bfs_plan("hall", lambda s: s == "hall", lambda s: G[s])
        self.assertEqual((r["actions"], r["states"], r["expanded"]), ([], ["hall"], 1))

    def test_unreachable(self):
        self.assertIsNone(S.bfs_plan("garden", lambda s: s == "hall", lambda s: G[s]))

    def test_shortest_on_grid(self):
        walls = {(1, 1), (1, 2), (1, 3)}
        r = S.bfs_plan((0, 0), lambda s: s == (2, 2), grid_succ(walls, 4))
        self.assertEqual(len(r["actions"]), 4)

    def test_cycles(self):
        cyc = {0: [("a", 1)], 1: [("b", 0), ("c", 2)], 2: [("d", 0)]}
        r = S.bfs_plan(0, lambda s: s == 2, lambda s: cyc[s])
        self.assertEqual(r["actions"], ["a", "c"])

    def test_expanded_count(self):
        line = {i: [("n", i + 1)] for i in range(5)}; line[5] = []
        self.assertEqual(S.bfs_plan(0, lambda s: s == 5, lambda s: line[s])["expanded"], 6)


if __name__ == "__main__":
    unittest.main()
