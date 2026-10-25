"""Tests for CV-19 Bilinear Resize.

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

IMG = np.array([[0., 10.], [20., 30.]])

class TestResize(unittest.TestCase):
    def test_point(self):
        self.assertAlmostEqual(S.resize_bilinear(IMG, 4, 4)[1, 1], 7.5)

    def test_corners_clamped(self):
        out = S.resize_bilinear(IMG, 4, 4)
        self.assertEqual((out[0, 0], out[0, 3], out[3, 0], out[3, 3]), (0.0, 10.0, 20.0, 30.0))

    def test_identity(self):
        img = np.random.default_rng(0).normal(size=(5, 7))
        np.testing.assert_allclose(S.resize_bilinear(img, 5, 7), img)

    def test_center(self):
        np.testing.assert_allclose(S.resize_bilinear(IMG, 1, 1), [[15.0]])

    def test_constant(self):
        np.testing.assert_allclose(S.resize_bilinear(np.full((3, 4), 2.5), 7, 2), 2.5)

    def test_linear_ramp_interior(self):
        img = np.tile(np.arange(8.0), (4, 1))
        out = S.resize_bilinear(img, 4, 16)
        exp = np.clip((np.arange(16) + 0.5) * 0.5 - 0.5, 0, 7)
        np.testing.assert_allclose(out[0], exp)

    def test_downscale_average(self):
        img = np.array([[0., 2.], [4., 6.]])
        np.testing.assert_allclose(S.resize_bilinear(img, 1, 2), [[2., 4.]])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.resize_bilinear(IMG, 0, 3)


if __name__ == "__main__":
    unittest.main()
