"""Tests for MA-04 Dot Product.

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


class TestDot(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.dot([1, 2, 3], [4, -5, 6]), 12)

    def test_perpendicular(self):
        self.assertEqual(S.dot([1, 0], [0, 1]), 0)

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.dot([1, 2], [1, 2, 3])

    def test_empty(self):
        self.assertEqual(S.dot([], []), 0)

    def test_symmetric(self):
        u, v = [0.5, -1.25, 3.0], [2.0, 4.0, -1.0]
        self.assertAlmostEqual(S.dot(u, v), S.dot(v, u), places=12)

    def test_self_is_squared_norm(self):
        self.assertAlmostEqual(S.dot([3, 4], [3, 4]), 25)

    def test_floats(self):
        self.assertAlmostEqual(S.dot([0.1, 0.2], [0.3, 0.4]), 0.11, places=12)


if __name__ == "__main__":
    unittest.main()
