"""Tests for CV-05 Flip and Rotate.

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

A = np.array([[1, 2, 3], [4, 5, 6]])

class TestFlipRotate(unittest.TestCase):
    def test_flips(self):
        np.testing.assert_array_equal(S.flip_horizontal(A), [[3, 2, 1], [6, 5, 4]])
        np.testing.assert_array_equal(S.flip_vertical(A), [[4, 5, 6], [1, 2, 3]])

    def test_cw(self):
        np.testing.assert_array_equal(S.rotate90_cw(A), [[4, 1], [5, 2], [6, 3]])

    def test_matches_rot90_negative(self):
        for k in range(-3, 6):
            np.testing.assert_array_equal(S.rotate90_cw(A, k), np.rot90(A, -k))

    def test_four_is_identity(self):
        np.testing.assert_array_equal(S.rotate90_cw(A, 4), A)

    def test_color(self):
        img = np.arange(2 * 3 * 3).reshape(2, 3, 3)
        out = S.rotate90_cw(img)
        self.assertEqual(out.shape, (3, 2, 3))
        np.testing.assert_array_equal(out[0, 0], img[1, 0])

    def test_double_flip(self):
        np.testing.assert_array_equal(S.flip_horizontal(S.flip_horizontal(A)), A)


if __name__ == "__main__":
    unittest.main()
