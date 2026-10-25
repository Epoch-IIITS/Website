"""Tests for MA-06 Matrix Multiplication.

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


class TestMatmul(unittest.TestCase):
    def test_2x2(self):
        self.assertEqual(S.matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])

    def test_not_commutative(self):
        self.assertEqual(S.matmul([[5, 6], [7, 8]], [[1, 2], [3, 4]]), [[23, 34], [31, 46]])

    def test_row_times_column(self):
        self.assertEqual(S.matmul([[1, 2, 3]], [[1], [0], [-1]]), [[-2]])

    def test_column_times_row(self):
        self.assertEqual(S.matmul([[1], [2]], [[3, 4]]), [[3, 4], [6, 8]])

    def test_incompatible(self):
        with self.assertRaises(ValueError):
            S.matmul([[1, 2]], [[1, 2]])

    def test_ragged(self):
        with self.assertRaises(ValueError):
            S.matmul([[1, 2], [3]], [[1], [2]])

    def test_identity(self):
        A = [[2, -1, 0], [4, 3, 5]]
        I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.assertEqual(S.matmul(A, I), A)

    def test_shape(self):
        C = S.matmul([[1, 2, 3], [4, 5, 6]], [[1, 0], [0, 1], [1, 1]])
        self.assertEqual((len(C), len(C[0])), (2, 2))
        self.assertEqual(C, [[4, 5], [10, 11]])


if __name__ == "__main__":
    unittest.main()
