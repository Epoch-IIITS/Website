"""Tests for MA-05 Vector Norm and Unit Vector.

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


class TestNorms(unittest.TestCase):
    def test_l2(self):
        self.assertAlmostEqual(S.norm([3, -4]), 5.0)

    def test_l1(self):
        self.assertAlmostEqual(S.norm([3, -4], p=1), 7.0)

    def test_linf(self):
        self.assertAlmostEqual(S.norm([3, -4, 1], p=float("inf")), 4.0)

    def test_bad_p(self):
        with self.assertRaises(ValueError):
            S.norm([1, 2], p=3)

    def test_empty(self):
        self.assertEqual(S.norm([]), 0.0)

    def test_unit(self):
        u = S.unit([3, -4])
        self.assertAlmostEqual(u[0], 0.6)
        self.assertAlmostEqual(u[1], -0.8)

    def test_unit_has_length_one(self):
        u = S.unit([1, 2, 2, 4])
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in u)), 1.0, places=12)

    def test_unit_zero(self):
        with self.assertRaises(ValueError):
            S.unit([0, 0])


if __name__ == "__main__":
    unittest.main()
