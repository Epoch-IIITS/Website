"""Tests for CV-16 Image Quality: MSE and PSNR.

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


class TestImageQuality(unittest.TestCase):
    def test_off_by_one(self):
        ref = np.full((8, 8), 100, np.uint8)
        r = S.image_quality(ref, ref + 1)
        self.assertEqual(r["mse"], 1.0)
        self.assertAlmostEqual(r["psnr"], 10 * math.log10(255 ** 2), places=6)

    def test_no_wraparound(self):
        a = np.array([[3]], np.uint8); b = np.array([[5]], np.uint8)
        self.assertEqual(S.image_quality(a, b)["mse"], 4.0)

    def test_identical_is_infinite(self):
        img = np.arange(16, dtype=np.uint8).reshape(4, 4)
        r = S.image_quality(img, img.copy())
        self.assertEqual(r["mse"], 0.0)
        self.assertEqual(r["psnr"], math.inf)

    def test_more_noise_lower_psnr(self):
        rng = np.random.default_rng(0)
        ref = rng.integers(20, 230, size=(32, 32, 3)).astype(np.uint8)
        mild = np.clip(ref + rng.integers(-3, 4, ref.shape), 0, 255).astype(np.uint8)
        strong = np.clip(ref + rng.integers(-30, 31, ref.shape), 0, 255).astype(np.uint8)
        self.assertGreater(S.image_quality(ref, mild)["psnr"], S.image_quality(ref, strong)["psnr"])

    def test_symmetric_and_formula(self):
        rng = np.random.default_rng(1)
        a = rng.integers(0, 256, (10, 10)).astype(np.uint8); b = rng.integers(0, 256, (10, 10)).astype(np.uint8)
        r1, r2 = S.image_quality(a, b), S.image_quality(b, a)
        self.assertEqual(r1, r2)
        self.assertAlmostEqual(r1["psnr"], 10 * math.log10(255 ** 2 / r1["mse"]), places=6)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.image_quality(np.zeros((2, 2), np.uint8), np.zeros((2, 3), np.uint8))
        with self.assertRaises(ValueError):
            S.image_quality(np.zeros((2, 2), np.float32), np.zeros((2, 2), np.float32))


if __name__ == "__main__":
    unittest.main()
