"""Tests for CV-06 Thresholding and Otsu's Method.

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


def otsu_brute_force(gray):
    values = gray.ravel().astype(float)
    best_t, best_score = 0, -1.0
    for t in range(256):
        low, high = values[values <= t], values[values > t]
        if len(low) == 0 or len(high) == 0:
            continue
        w0, w1 = len(low) / len(values), len(high) / len(values)
        score = w0 * w1 * (low.mean() - high.mean()) ** 2
        if score > best_score + 1e-9:
            best_t, best_score = t, score
    return best_t


class TestBinarise(unittest.TestCase):
    def test_fixed_threshold_is_strict(self):
        t, mask = S.binarise(np.array([[99, 100, 101]], np.uint8), 100)
        self.assertEqual(t, 100.0)
        self.assertEqual(mask.tolist(), [[0, 0, 255]])

    def test_otsu_example(self):
        t, mask = S.binarise(np.array([[10, 30], [200, 220]], np.uint8))
        self.assertEqual(mask.tolist(), [[0, 0], [255, 255]])
        self.assertTrue(30 <= t < 200)

    def test_otsu_matches_between_class_variance(self):
        rng = np.random.default_rng(0)
        gray = np.clip(np.concatenate([rng.normal(60, 15, 300), rng.normal(170, 20, 200)]), 0, 255).astype(np.uint8).reshape(20, 25)
        t, _ = S.binarise(gray)
        self.assertEqual(int(t), otsu_brute_force(gray))

    def test_invert(self):
        _, mask = S.binarise(np.array([[10, 200]], np.uint8), 100, invert=True)
        self.assertEqual(mask.tolist(), [[255, 0]])

    def test_output_types(self):
        t, mask = S.binarise(np.arange(16, dtype=np.uint8).reshape(4, 4) * 16)
        self.assertIs(type(t), float)
        self.assertEqual(mask.dtype, np.uint8)
        self.assertTrue(set(np.unique(mask).tolist()) <= {0, 255})

    def test_invalid(self):
        for bad in (np.zeros((2, 2), np.float32), np.zeros((2, 2, 3), np.uint8)):
            with self.assertRaises(ValueError):
                S.binarise(bad)


if __name__ == "__main__":
    unittest.main()
