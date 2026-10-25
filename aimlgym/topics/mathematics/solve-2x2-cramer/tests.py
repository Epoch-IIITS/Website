"""Tests for MA-08 Solve a 2x2 System (Cramer's Rule).

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


class TestSolve(unittest.TestCase):
    def test_example(self):
        x, y = S.solve_2x2([[2, 1], [1, -1]], [5, 1])
        self.assertAlmostEqual(x, 2.0)
        self.assertAlmostEqual(y, 1.0)

    def test_singular(self):
        with self.assertRaises(ValueError):
            S.solve_2x2([[1, 2], [2, 4]], [3, 6])

    def test_near_singular_tolerance(self):
        with self.assertRaises(ValueError):
            S.solve_2x2([[1, 1], [1, 1 + 1e-15]], [1, 2])

    def test_identity(self):
        self.assertEqual(S.solve_2x2([[1, 0], [0, 1]], [3.5, -2]), (3.5, -2.0))

    def test_residual(self):
        A, b = [[0.3, -1.7], [2.2, 0.9]], [1.1, -0.4]
        x, y = S.solve_2x2(A, b)
        self.assertAlmostEqual(A[0][0] * x + A[0][1] * y, b[0], places=10)
        self.assertAlmostEqual(A[1][0] * x + A[1][1] * y, b[1], places=10)

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            S.solve_2x2([[1, 2, 3], [4, 5, 6]], [1, 2])

    def test_returns_floats(self):
        x, y = S.solve_2x2([[2, 0], [0, 4]], [2, 2])
        self.assertIsInstance(x, float)
        self.assertEqual((x, y), (1.0, 0.5))


if __name__ == "__main__":
    unittest.main()
