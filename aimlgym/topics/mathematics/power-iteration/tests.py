"""Tests for MA-16 Dominant Eigenvalue by Power Iteration.

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


class TestPower(unittest.TestCase):
    def test_symmetric(self):
        lam, v = S.power_iteration([[2, 1], [1, 2]])
        self.assertAlmostEqual(lam, 3.0, places=8)
        self.assertAlmostEqual(v[0], 1 / math.sqrt(2), places=6)
        self.assertAlmostEqual(v[1], 1 / math.sqrt(2), places=6)

    def test_diagonal_negative(self):
        lam, v = S.power_iteration([[4, 0], [0, -1]])
        self.assertAlmostEqual(lam, 4.0, places=8)
        # eigenvectors converge more slowly than the Rayleigh quotient (~sqrt(tol))
        self.assertAlmostEqual(v[0], 1.0, delta=1e-4)
        self.assertAlmostEqual(v[1], 0.0, delta=1e-4)

    def test_eigen_equation(self):
        A = [[4, 1, 0], [1, 3, 1], [0, 1, 2]]
        lam, v = S.power_iteration(A)
        Av = [sum(a * x for a, x in zip(r, v)) for r in A]
        for i in range(3):
            self.assertAlmostEqual(Av[i], lam * v[i], places=5)

    def test_unit_length(self):
        _, v = S.power_iteration([[5, 2], [2, 1]])
        self.assertAlmostEqual(math.sqrt(sum(x * x for x in v)), 1.0, places=10)

    def test_sign_convention(self):
        _, v = S.power_iteration([[-3, 0], [0, 1]])
        self.assertGreater(max(v, key=abs), 0)

    def test_not_square(self):
        with self.assertRaises(ValueError):
            S.power_iteration([[1, 2, 3], [4, 5, 6]])

    def test_zero_matrix(self):
        with self.assertRaises(ValueError):
            S.power_iteration([[0, 0], [0, 0]])

    def test_1x1(self):
        lam, v = S.power_iteration([[7]])
        self.assertAlmostEqual(lam, 7.0)
        self.assertEqual(v, [1.0])


import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_eigh(self):
        A = [[4.0, 1.0, 0.5], [1.0, 3.0, 0.2], [0.5, 0.2, 1.0]]
        lam, v = S.power_iteration(A)
        w, V = np.linalg.eigh(np.array(A))
        self.assertAlmostEqual(lam, w[-1], places=8)
        top = V[:, -1] * np.sign(V[np.argmax(np.abs(V[:, -1])), -1])
        np.testing.assert_allclose(v, top, atol=1e-4)


if __name__ == "__main__":
    unittest.main()
