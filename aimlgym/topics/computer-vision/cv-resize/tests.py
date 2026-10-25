"""Tests for CV-18 Resizing with cv2.resize.

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


class TestResize(unittest.TestCase):
    def test_size_order(self):
        out = S.resize(np.zeros((10, 20), np.uint8), 8, 4)
        self.assertEqual(out.shape, (4, 8))

    def test_area_halving_averages_blocks(self):
        img = np.arange(16, dtype=np.uint8).reshape(4, 4)
        self.assertEqual(S.resize(img, 2, 2, "area").tolist(), [[3, 5], [11, 13]])

    def test_nearest_keeps_labels(self):
        mask = np.array([[0, 1], [2, 3]], np.uint8)
        out = S.resize(mask, 7, 5, "nearest")
        self.assertTrue(set(np.unique(out).tolist()) <= {0, 1, 2, 3})
        linear = S.resize(np.array([[0, 255]], np.uint8), 8, 1, "linear")
        self.assertTrue(len(set(linear.ravel().tolist())) > 2)

    def test_linear_upscale_is_monotone(self):
        out = S.resize(np.array([[0, 100]], np.uint8), 4, 1, "linear")
        self.assertEqual(out.tolist(), [[0, 25, 75, 100]])

    def test_colour_and_dtype_kept(self):
        img = np.random.default_rng(0).integers(0, 256, (6, 9, 3)).astype(np.uint8)
        out = S.resize(img, 3, 2, "cubic")
        self.assertEqual((out.shape, out.dtype), ((2, 3, 3), np.uint8))

    def test_invalid(self):
        img = np.zeros((4, 4), np.uint8)
        with self.assertRaises(ValueError):
            S.resize(img, 2, 2, "lanczos9")
        with self.assertRaises(ValueError):
            S.resize(img, 0, 2)


if __name__ == "__main__":
    unittest.main()
