"""Tests for PY-21 Safe Division with Exceptions.

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


class TestSafeDivide(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(S.safe_divide(7, 2), 3.5)

    def test_zero(self):
        self.assertIsNone(S.safe_divide(1, 0))

    def test_float_zero(self):
        self.assertIsNone(S.safe_divide(1.0, 0.0))

    def test_type_error_propagates(self):
        with self.assertRaises(TypeError):
            S.safe_divide("6", 3)

    def test_pairs(self):
        self.assertEqual(S.divide_pairs([(6, 3), (1, 0), (5, 2)]), ([2.0, None, 2.5], [1]))

    def test_pairs_empty(self):
        self.assertEqual(S.divide_pairs([]), ([], []))

    def test_pairs_all_fail(self):
        self.assertEqual(S.divide_pairs([(1, 0), (0, 0)]), ([None, None], [0, 1]))

    def test_zero_numerator_ok(self):
        self.assertEqual(S.divide_pairs([(0, 5)]), ([0.0], []))


if __name__ == "__main__":
    unittest.main()
