"""Tests for RL-02 Gridworld Transition Function.

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


ROWS = ["S..G", ".#.X"]

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.g = S.GridWorld(ROWS)

    def test_dims(self):
        self.assertEqual((self.g.n_rows, self.g.n_cols, self.g.n_states, self.g.start), (2, 4, 8, 0))

    def test_moves(self):
        self.assertEqual(self.g.step(0, 1), (1, -1.0, False))
        self.assertEqual(self.g.step(0, 2), (4, -1.0, False))

    def test_goal_and_pit(self):
        self.assertEqual(self.g.step(2, 1), (3, 10.0, True))
        self.assertEqual(self.g.step(6, 1), (7, -10.0, True))

    def test_walls_and_bounds(self):
        self.assertEqual(self.g.step(4, 1), (4, -1.0, False))
        self.assertEqual(self.g.step(0, 0), (0, -1.0, False))
        self.assertEqual(self.g.step(0, 3), (0, -1.0, False))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            self.g.step(3, 0)
        with self.assertRaises(ValueError):
            self.g.step(0, 7)

    def test_P(self):
        P = self.g.build_P()
        self.assertEqual(P[2][1], [(1.0, 3, 10.0, True)])
        self.assertEqual(P[3][0], [(1.0, 3, 0.0, True)])
        self.assertEqual(P[5][2], [(1.0, 5, 0.0, True)])
        self.assertEqual(len(P), 8)
        self.assertTrue(all(len(P[s]) == 4 for s in P))


if __name__ == "__main__":
    unittest.main()
