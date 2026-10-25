"""Tests for CV-04 Flips, Rotations and Affine Warps.

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

IMG = np.arange(20, dtype=np.uint8).reshape(4, 5)


class TestGeometricTransforms(unittest.TestCase):

    def test_flips(self):
        self.assertTrue(np.array_equal(S.transform(IMG, "flip_h"), IMG[:, ::-1]))
        self.assertTrue(np.array_equal(S.transform(IMG, "flip_v"), IMG[::-1, :]))

    def test_quarter_turns(self):
        self.assertTrue(np.array_equal(S.transform(IMG, "rot90_cw"), np.rot90(IMG, -1)))
        self.assertTrue(np.array_equal(S.transform(IMG, "rot90_ccw"), np.rot90(IMG, 1)))
        self.assertTrue(np.array_equal(S.transform(IMG, "rot180"), np.rot90(IMG, 2)))

    def test_rotate_about_centre_is_counter_clockwise(self):
        square = np.arange(25, dtype=np.uint8).reshape(5, 5)
        self.assertTrue(np.array_equal(S.rotate_about_centre(square, 90), np.rot90(square, 1)))

    def test_rotation_keeps_size_and_dtype(self):
        out = S.rotate_about_centre(IMG, 30, scale=0.8)
        self.assertEqual((out.shape, out.dtype), ((4, 5), np.uint8))

    def test_translate(self):
        out = S.translate(IMG, 2, 1)
        self.assertTrue(np.array_equal(out[1:, 2:], IMG[:-1, :-2]))
        self.assertEqual(int(out[0].sum()) + int(out[:, :2].sum()), 0)

    def test_unknown_op(self):
        with self.assertRaises(ValueError):
            S.transform(IMG, "rot45")


if __name__ == "__main__":
    unittest.main()
