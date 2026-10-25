"""Tests for CV-22 Data Augmentation.

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


def bar(horizontal=True, size=16):
    img = np.zeros((size, size), np.uint8)
    if horizontal:
        img[8, 3:13] = 200
    else:
        img[3:13, 8] = 200
    return img


class TestAugmentation(unittest.TestCase):
    def test_shape_and_dtype(self):
        rng = np.random.default_rng(0)
        for image in (bar(), np.zeros((12, 10, 3), np.uint8)):
            out = S.augment(image, rng)
            self.assertEqual((out.shape, out.dtype), (image.shape, np.uint8))

    def test_reproducible(self):
        images = np.stack([bar(i % 2 == 0) for i in range(6)])
        self.assertTrue(np.array_equal(S.augment_batch(images, seed=4), S.augment_batch(images, seed=4)))
        self.assertFalse(np.array_equal(S.augment_batch(images, seed=4), S.augment_batch(images, seed=5)))

    def test_label_preserved(self):
        rng = np.random.default_rng(1)
        for _ in range(20):
            out = S.augment(bar(True), rng).astype(int)
            self.assertGreater(out.sum(axis=1).max(), 3 * out.sum(axis=0).max())

    def test_values_clipped(self):
        rng = np.random.default_rng(2)
        bright = np.full((8, 8), 250, np.uint8)
        outs = [S.augment(bright, rng, max_shift=0) for _ in range(20)]
        self.assertTrue(all(int(o.max()) <= 255 for o in outs))
        self.assertTrue(any(int(o.max()) == 255 for o in outs))

    def test_zero_shift_and_flip_frequency(self):
        rng = np.random.default_rng(3)
        img = np.zeros((6, 6), np.uint8); img[:, 0] = 100
        flips = sum(int(S.augment(img, rng, max_shift=0)[0, 5] > 0) for _ in range(200))
        self.assertTrue(60 < flips < 140)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.augment(np.zeros((4, 4), np.float32), np.random.default_rng(0))


if __name__ == "__main__":
    unittest.main()
