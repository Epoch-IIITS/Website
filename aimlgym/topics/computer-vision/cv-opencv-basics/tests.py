"""Tests for CV-03 OpenCV Basics: BGR, dtypes and Indexing.

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


class TestOpenCVBasics(unittest.TestCase):
    def test_blue_pixel(self):
        rgb, gray = S.to_rgb_and_gray(np.array([[[255, 0, 0]]], dtype=np.uint8))
        self.assertEqual(rgb.tolist(), [[[0, 0, 255]]])
        self.assertEqual(gray.tolist(), [[29]])

    def test_gray_weights(self):
        rng = np.random.default_rng(0)
        bgr = rng.integers(0, 256, size=(4, 5, 3), dtype=np.uint8)
        _, gray = S.to_rgb_and_gray(bgr)
        b, g, r = (bgr[..., i].astype(float) for i in range(3))
        self.assertTrue(np.all(np.abs(gray - (0.299 * r + 0.587 * g + 0.114 * b)) <= 1))
        self.assertEqual((gray.shape, gray.dtype), ((4, 5), np.uint8))

    def test_rgb_is_reversed_channels(self):
        bgr = np.arange(24, dtype=np.uint8).reshape(2, 4, 3)
        rgb, _ = S.to_rgb_and_gray(bgr)
        self.assertTrue(np.array_equal(rgb, bgr[..., ::-1]))

    def test_crop_rows_then_columns(self):
        image = np.arange(48).reshape(6, 8)
        self.assertEqual(S.crop(image, 4, 1, 3, 2).tolist(), [[12, 13, 14], [20, 21, 22]])

    def test_crop_is_copy(self):
        image = np.zeros((5, 5), dtype=np.uint8)
        patch = S.crop(image, 1, 1, 2, 2)
        patch[:] = 255
        self.assertEqual(int(image.sum()), 0)

    def test_invalid(self):
        for bad in (np.zeros((3, 3), np.uint8), np.zeros((3, 3, 3), np.float32), np.zeros((3, 3, 4), np.uint8)):
            with self.assertRaises(ValueError):
                S.to_rgb_and_gray(bad)
        with self.assertRaises(ValueError):
            S.crop(np.zeros((4, 4)), 2, 2, 3, 1)


if __name__ == "__main__":
    unittest.main()
