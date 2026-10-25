"""Tests for MA-12 Trapezoidal Integration.

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


class TestTrapezoid(unittest.TestCase):
    def test_n2(self):
        self.assertAlmostEqual(S.trapezoid(lambda x: x ** 2, 0, 1, 2), 0.375)

    def test_linear_exact(self):
        self.assertAlmostEqual(S.trapezoid(lambda x: 3 * x + 1, 0, 2, 1), 8.0)

    def test_reversed(self):
        self.assertAlmostEqual(S.trapezoid(lambda x: x ** 2, 1, 0, 2), -0.375)

    def test_zero_width(self):
        self.assertEqual(S.trapezoid(math.sin, 2.0, 2.0, 5), 0.0)

    def test_sin_converges(self):
        self.assertAlmostEqual(S.trapezoid(math.sin, 0, math.pi, 1000), 2.0, delta=1e-5)

    def test_error_quarters(self):
        f, exact = (lambda x: x ** 2), 1 / 3
        e1 = abs(S.trapezoid(f, 0, 1, 10) - exact)
        e2 = abs(S.trapezoid(f, 0, 1, 20) - exact)
        self.assertAlmostEqual(e1 / e2, 4.0, delta=0.01)

    def test_bad_n(self):
        for bad in (0, -3, 2.0):
            with self.assertRaises(ValueError):
                S.trapezoid(math.sin, 0, 1, bad)


import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_trapezoid(self):
        f = lambda t: math.exp(-t) * math.sin(3 * t)
        x = np.linspace(0.0, 2.0, 41)
        y = np.array([f(t) for t in x])
        integrate = getattr(np, "trapezoid", None) or np.trapz
        self.assertAlmostEqual(S.trapezoid(f, 0.0, 2.0, 40), float(integrate(y, x)), places=12)


if __name__ == "__main__":
    unittest.main()
