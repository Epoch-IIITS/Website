"""Tests for NP-12 Solve Linear Systems Safely.

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


import numpy as np

class TestLinalg(unittest.TestCase):
    def test_solve(self):
        np.testing.assert_allclose(S.solve(np.array([[3., 1.], [1., 2.]]), np.array([9., 8.])), [2, 3])

    def test_singular(self):
        with self.assertRaises(ValueError):
            S.solve(np.array([[1., 2.], [2., 4.]]), np.array([1., 2.]))

    def test_ill_conditioned(self):
        with self.assertRaises(ValueError):
            S.solve(np.array([[1., 1.], [1., 1 + 1e-14]]), np.array([2., 2.]))

    def test_shape(self):
        with self.assertRaises(ValueError):
            S.solve(np.ones((2, 3)), np.ones(2))

    def test_residual(self):
        A = np.array([[4., -2, 1], [3, 6, -4], [2, 1, 8]])
        b = np.array([12., -25, 32])
        x = S.solve(A, b)
        self.assertLess(S.residual_norm(A, x, b), 1e-10)
        self.assertIsInstance(S.residual_norm(A, x, b), float)

    def test_fit_line(self):
        i, s = S.fit_line([0, 1, 2], [1, 3, 5])
        self.assertAlmostEqual(i, 1.0)
        self.assertAlmostEqual(s, 2.0)

    def test_fit_line_noisy(self):
        i, s = S.fit_line([0, 1, 2, 3], [1, 2, 2, 4])
        self.assertAlmostEqual(s, 0.9)
        self.assertAlmostEqual(i, 0.9)

    def test_fit_bad(self):
        with self.assertRaises(ValueError):
            S.fit_line([1], [2])


import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_cramer_2x2(self):
        (a, b), (c, d), (e, f) = (2.0, 1.0), (1.0, 3.0), (5.0, 10.0)
        det = a * d - b * c
        x = S.solve([[a, b], [c, d]], [e, f])
        np.testing.assert_allclose(x, [(e * d - b * f) / det, (a * f - e * c) / det])

    def test_library_fit_line_matches_polyfit(self):
        x = [0.0, 1.0, 2.0, 3.0, 4.5]
        y = [1.1, 2.9, 5.2, 7.1, 9.8]
        slope, intercept = np.polyfit(x, y, 1)
        b0, b1 = S.fit_line(x, y)
        self.assertAlmostEqual(b0, intercept, places=10)
        self.assertAlmostEqual(b1, slope, places=10)


if __name__ == "__main__":
    unittest.main()
