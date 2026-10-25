"""Tests for MA-14 Numerical Gradient of f(x1..xn).

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


class TestNumGrad(unittest.TestCase):
    def assertListAlmost(self, a, b, delta):
        self.assertEqual(len(a), len(b))
        for p, q in zip(a, b):
            self.assertAlmostEqual(p, q, delta=delta)

    def test_example(self):
        f = lambda v: v[0] ** 2 + 3 * v[0] * v[1]
        self.assertListAlmost(S.numerical_gradient(f, [1.0, 2.0]), [8.0, 3.0], 1e-6)

    def test_not_modified(self):
        x = [1.0, 2.0, 3.0]
        S.numerical_gradient(lambda v: sum(t * t for t in v), x)
        self.assertEqual(x, [1.0, 2.0, 3.0])

    def test_sum_of_squares(self):
        x = [0.5, -1.5, 2.0]
        self.assertListAlmost(S.numerical_gradient(lambda v: sum(t * t for t in v), x),
                              [1.0, -3.0, 4.0], 1e-6)

    def test_single_variable(self):
        self.assertListAlmost(S.numerical_gradient(lambda v: math.sin(v[0]), [0.3]),
                              [math.cos(0.3)], 1e-8)

    def test_gd_step(self):
        self.assertListAlmost(S.gd_step(lambda v: v[0] ** 2 + v[1] ** 2, [1.0, -2.0], 0.25),
                              [0.5, -1.0], 1e-6)

    def test_gd_converges(self):
        f = lambda v: (v[0] - 1) ** 2 + 2 * (v[1] + 0.5) ** 2
        x = [0.0, 0.0]
        for _ in range(200):
            x = S.gd_step(f, x, 0.1)
        self.assertListAlmost(x, [1.0, -0.5], 1e-4)

    def test_bad_h(self):
        with self.assertRaises(ValueError):
            S.numerical_gradient(lambda v: v[0], [1.0], h=0)


if __name__ == "__main__":
    unittest.main()
