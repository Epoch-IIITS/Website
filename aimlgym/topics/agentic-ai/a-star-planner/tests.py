"""Tests for AG-12 A* Planner.

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


def grid(n, walls=frozenset(), costs=None):
    def nb(s):
        r, c = s
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            q = (r + dr, c + dc)
            if 0 <= q[0] < n and 0 <= q[1] < n and q not in walls:
                yield q, (costs.get(q, 1.0) if costs else 1.0)
    return nb

man = lambda g: (lambda s: abs(s[0] - g[0]) + abs(s[1] - g[1]))

class TestAStar(unittest.TestCase):
    def test_open_grid(self):
        r = S.astar((0, 0), (4, 4), grid(5), man((4, 4)))
        self.assertEqual((r["cost"], len(r["path"]), r["path"][0], r["path"][-1]), (8.0, 9, (0, 0), (4, 4)))

    def test_fewer_expansions_than_ucs(self):
        a = S.astar((0, 0), (9, 9), grid(10), man((9, 9)))
        u = S.astar((0, 0), (9, 9), grid(10), lambda s: 0.0)
        self.assertEqual(a["cost"], u["cost"])
        self.assertLess(a["expanded"], u["expanded"])

    def test_walls(self):
        walls = frozenset({(1, 0), (1, 1), (1, 2), (1, 3)})
        r = S.astar((0, 0), (2, 0), grid(5, walls), man((2, 0)))
        self.assertEqual(r["cost"], 10.0)

    def test_weighted_costs(self):
        costs = {(0, 1): 10.0}
        r = S.astar((0, 0), (0, 2), grid(3, costs=costs), man((0, 2)))
        self.assertEqual(r["cost"], 4.0)
        self.assertNotIn((0, 1), r["path"])

    def test_unreachable(self):
        walls = frozenset({(0, 1), (1, 0)})
        self.assertIsNone(S.astar((0, 0), (2, 2), grid(3, walls), man((2, 2))))

    def test_start_is_goal(self):
        r = S.astar((1, 1), (1, 1), grid(3), man((1, 1)))
        self.assertEqual((r["path"], r["cost"], r["expanded"]), ([(1, 1)], 0.0, 1))

    def test_path_valid(self):
        r = S.astar((0, 0), (3, 4), grid(6, frozenset({(1, 1), (2, 2)})), man((3, 4)))
        for a, b in zip(r["path"], r["path"][1:]):
            self.assertEqual(abs(a[0] - b[0]) + abs(a[1] - b[1]), 1)


if __name__ == "__main__":
    unittest.main()
