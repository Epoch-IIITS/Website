"""Tests for MA-11 Derivative Rules and the Chain Rule.

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


def numeric(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


class TestDerivativeRules(unittest.TestCase):
    def test_power(self):
        f, df = S.power_rule(3)
        self.assertEqual(f(2), 8)
        self.assertEqual(df(2), 12)

    def test_sum(self):
        f, df = S.sum_rule(math.sin, math.cos, *S.power_rule(2))
        for x in (-1.0, 0.3, 2.0):
            self.assertAlmostEqual(f(x), math.sin(x) + x * x)
            self.assertAlmostEqual(df(x), numeric(f, x), places=6)

    def test_product(self):
        f, df = S.product_rule(math.exp, math.exp, *S.power_rule(2))
        self.assertAlmostEqual(df(1.0), 3 * math.e)
        self.assertAlmostEqual(df(-0.5), numeric(f, -0.5), places=6)

    def test_chain(self):
        f, df = S.chain_rule(math.sin, math.cos, *S.power_rule(2))
        for x in (0.0, 0.7, -1.3):
            self.assertAlmostEqual(f(x), math.sin(x * x))
            self.assertAlmostEqual(df(x), math.cos(x * x) * 2 * x)

    def test_sigmoid_of_linear(self):
        h, dh = S.sigmoid_of_linear(3, 1)
        self.assertAlmostEqual(h(0), 1 / (1 + math.exp(-1)))
        s = 1 / (1 + math.exp(-1))
        self.assertAlmostEqual(dh(0), 3 * s * (1 - s))
        self.assertAlmostEqual(dh(-0.4), numeric(h, -0.4), places=6)

    def test_sigmoid_of_linear_stable(self):
        h, dh = S.sigmoid_of_linear(10, 0)
        self.assertEqual(h(-500), 0.0)
        self.assertEqual(dh(-500), 0.0)

    def test_rules_compose(self):
        inner = S.sigmoid_of_linear(2, -1)
        f, df = S.product_rule(*inner, *S.power_rule(3))
        for x in (-1.0, 0.25, 1.5):
            self.assertAlmostEqual(df(x), numeric(f, x), places=5)


if __name__ == "__main__":
    unittest.main()
