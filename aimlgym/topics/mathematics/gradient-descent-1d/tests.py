"""Tests for MA-13 Gradient Descent in 1D.

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


def df(x):
    return 2 * (x - 3)


class TestGD(unittest.TestCase):
    def test_converges(self):
        x, h = S.gradient_descent(df, 0.0, 0.25)
        self.assertAlmostEqual(x, 3.0, delta=1e-7)

    def test_first_iterates(self):
        _, h = S.gradient_descent(df, 0.0, 0.25)
        for got, exp in zip(h[:4], [0.0, 1.5, 2.25, 2.625]):
            self.assertAlmostEqual(got, exp)

    def test_diverges_with_large_lr(self):
        x, h = S.gradient_descent(df, 0.0, 1.5, max_steps=5)
        self.assertEqual(len(h), 6)
        errs = [abs(v - 3) for v in h]
        self.assertTrue(all(errs[i + 1] > errs[i] for i in range(5)))

    def test_max_steps_respected(self):
        _, h = S.gradient_descent(df, 0.0, 0.01, max_steps=3)
        self.assertEqual(len(h), 4)

    def test_already_at_min(self):
        x, h = S.gradient_descent(df, 3.0, 0.1)
        self.assertEqual(x, 3.0)
        self.assertEqual(len(h), 2)

    def test_bad_lr(self):
        with self.assertRaises(ValueError):
            S.gradient_descent(df, 0.0, 0.0)

    def test_quartic(self):
        x, _ = S.gradient_descent(lambda x: 4 * (x - 1) ** 3, 2.0, 0.1, max_steps=20000, tol=1e-12)
        self.assertAlmostEqual(x, 1.0, delta=1e-2)

    def test_nonfinite_stops(self):
        x, h = S.gradient_descent(lambda x: x * x * x, 10.0, 1.0, max_steps=50)
        self.assertFalse(math.isfinite(x))
        self.assertLess(len(h), 51)


if __name__ == "__main__":
    unittest.main()
