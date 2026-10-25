"""Tests for MA-09 Inverse of a 2x2 Matrix.

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


def _mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


class TestInverse(unittest.TestCase):
    def assertMatAlmost(self, X, Y, places=10):
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(X[i][j], Y[i][j], places=places)

    def test_example(self):
        self.assertMatAlmost(S.inverse_2x2([[4, 7], [2, 6]]), [[0.6, -0.7], [-0.2, 0.4]])

    def test_singular(self):
        with self.assertRaises(ValueError):
            S.inverse_2x2([[2, 4], [1, 2]])

    def test_identity(self):
        self.assertMatAlmost(S.inverse_2x2([[1, 0], [0, 1]]), [[1, 0], [0, 1]])

    def test_product_is_identity(self):
        A = [[0.5, -1.25], [3.0, 2.0]]
        self.assertMatAlmost(_mm(A, S.inverse_2x2(A)), [[1, 0], [0, 1]])
        self.assertMatAlmost(_mm(S.inverse_2x2(A), A), [[1, 0], [0, 1]])

    def test_inverse_of_inverse(self):
        A = [[3, 1], [-2, 5]]
        self.assertMatAlmost(S.inverse_2x2(S.inverse_2x2(A)), A)

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            S.inverse_2x2([[1, 2]])

    def test_diagonal(self):
        self.assertMatAlmost(S.inverse_2x2([[2, 0], [0, -4]]), [[0.5, 0], [0, -0.25]])


if __name__ == "__main__":
    unittest.main()
