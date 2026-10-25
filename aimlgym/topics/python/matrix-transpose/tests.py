"""Tests for PY-20 Matrix Transpose with Validation.

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


class TestTranspose(unittest.TestCase):
    def test_2x3(self):
        self.assertEqual(S.transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])

    def test_1x1(self):
        self.assertEqual(S.transpose([[7]]), [[7]])

    def test_ragged(self):
        with self.assertRaises(ValueError):
            S.transpose([[1, 2], [3]])

    def test_empty(self):
        self.assertEqual(S.transpose([]), [])

    def test_empty_rows(self):
        self.assertEqual(S.transpose([[], []]), [])

    def test_column_vector(self):
        self.assertEqual(S.transpose([[1], [2], [3]]), [[1, 2, 3]])

    def test_involution_and_no_mutation(self):
        m = [[1, 2], [3, 4], [5, 6]]
        copy = [r[:] for r in m]
        self.assertEqual(S.transpose(S.transpose(m)), copy)
        self.assertEqual(m, copy)

    def test_independent_rows(self):
        t = S.transpose([[1, 2], [3, 4]])
        t[0][0] = 99
        self.assertEqual(t[1][0], 2)


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_zip_idiom(self):
        m = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(S.transpose(m), [list(r) for r in zip(*m)])


if __name__ == "__main__":
    unittest.main()
