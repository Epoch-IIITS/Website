"""Tests for CV-17 MSE and PSNR by Hand.

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

A = np.array([[0, 0]], np.uint8); B = np.array([[0, 255]], np.uint8)

class TestPSNR(unittest.TestCase):
    def test_mse(self):
        self.assertAlmostEqual(S.mse(A, B), 32512.5)

    def test_psnr(self):
        self.assertAlmostEqual(S.psnr(A, B), 10 * math.log10(2))

    def test_overflow(self):
        self.assertEqual(S.mse(np.array([3], np.uint8), np.array([5], np.uint8)), 4.0)

    def test_identical(self):
        self.assertEqual(S.psnr(A, A), math.inf)

    def test_max_val(self):
        a = np.zeros((2, 2)); b = np.full((2, 2), 0.1)
        self.assertAlmostEqual(S.psnr(a, b, max_val=1.0), 20.0)

    def test_six_db_rule(self):
        a = np.zeros(100); p1 = S.psnr(a, np.full(100, 4.0)); p2 = S.psnr(a, np.full(100, 2.0))
        self.assertAlmostEqual(p2 - p1, 20 * math.log10(2))

    def test_shape(self):
        with self.assertRaises(ValueError):
            S.mse(np.zeros(3), np.zeros(4))


if __name__ == "__main__":
    unittest.main()
