"""Tests for MA-10 Numerical Derivative (Central Difference).

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


class TestDiff(unittest.TestCase):
    def test_central_cubic(self):
        self.assertAlmostEqual(S.central_diff(lambda x: x ** 3, 2.0), 12.0, delta=1e-6)

    def test_forward_h01(self):
        self.assertAlmostEqual(S.forward_diff(lambda x: x ** 3, 2.0, h=0.1), 12.61, places=9)

    def test_central_h01(self):
        self.assertAlmostEqual(S.central_diff(lambda x: x ** 3, 2.0, h=0.1), 12.01, places=9)

    def test_sin(self):
        self.assertAlmostEqual(S.central_diff(math.sin, 0.7), math.cos(0.7), delta=1e-8)

    def test_exp(self):
        self.assertAlmostEqual(S.central_diff(math.exp, 1.0), math.e, delta=1e-7)

    def test_bad_h(self):
        with self.assertRaises(ValueError):
            S.central_diff(math.sin, 0.0, h=0)
        with self.assertRaises(ValueError):
            S.forward_diff(math.sin, 0.0, h=-1e-3)

    def test_central_more_accurate(self):
        f, x, h = math.exp, 0.5, 1e-3
        ef = abs(S.forward_diff(f, x, h) - math.exp(x))
        ec = abs(S.central_diff(f, x, h) - math.exp(x))
        self.assertLess(ec, ef / 100)


if __name__ == "__main__":
    unittest.main()
