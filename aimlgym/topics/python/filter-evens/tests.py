"""Tests for PY-12 Filter Even Numbers.

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


class TestEvens(unittest.TestCase):
    def test_mixed(self):
        self.assertEqual(S.evens([5, -4, 0, 7, 12]), [-4, 0, 12])

    def test_none_even(self):
        self.assertEqual(S.evens([1, 3, 5]), [])

    def test_empty(self):
        self.assertEqual(S.evens([]), [])

    def test_all_even_order(self):
        self.assertEqual(S.evens([8, 2, 6]), [8, 2, 6])

    def test_negatives(self):
        self.assertEqual(S.evens([-3, -2, -1]), [-2])

    def test_duplicates_kept(self):
        self.assertEqual(S.evens([2, 2, 3, 2]), [2, 2, 2])

    def test_not_modified(self):
        data = [1, 2, 3]
        S.evens(data)
        self.assertEqual(data, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
