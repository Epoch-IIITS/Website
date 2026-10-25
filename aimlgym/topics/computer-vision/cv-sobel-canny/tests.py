"""Tests for CV-11 Edges with Sobel and Canny.

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


def square(size=32, lo=8, hi=24):
    img = np.zeros((size, size), np.uint8)
    img[lo:hi, lo:hi] = 200
    return img


class TestEdges(unittest.TestCase):
    def test_vertical_edge_in_gx_only(self):
        img = np.zeros((10, 10), np.uint8); img[:, 5:] = 100
        r = S.edges(img, 50, 150)
        self.assertGreater(r["gx"][5, 4], 0)
        self.assertEqual(float(np.abs(r["gy"][2:8, 2:8]).max()), 0.0)

    def test_negative_gradients_kept(self):
        img = np.zeros((10, 10), np.uint8); img[:, :5] = 100
        self.assertLess(S.edges(img, 50, 150)["gx"][5, 4], 0)

    def test_magnitude(self):
        r = S.edges(square(), 50, 150)
        self.assertTrue(np.allclose(r["magnitude"], np.sqrt(r["gx"] ** 2 + r["gy"] ** 2)))
        self.assertEqual(r["gx"].dtype, np.float64)

    def test_canny_outline(self):
        r = S.edges(square(), 50, 150)
        canny = r["canny"]
        self.assertEqual(canny.dtype, np.uint8)
        self.assertTrue(set(np.unique(canny).tolist()) <= {0, 255})
        ys, xs = np.nonzero(canny)
        self.assertTrue(6 <= ys.min() <= 9 and 22 <= ys.max() <= 25)
        self.assertEqual(int(canny[14:18, 14:18].sum()), 0)

    def test_flat_image_has_no_edges(self):
        r = S.edges(np.full((16, 16), 80, np.uint8), 10, 30)
        self.assertEqual(int(r["canny"].sum()), 0)
        self.assertEqual(float(r["magnitude"].max()), 0.0)

    def test_invalid(self):
        img = square()
        for args in ((img, 150, 50), (img, 50, 150, 4), (img.astype(np.float32), 50, 150)):
            with self.assertRaises(ValueError):
                S.edges(*args)


if __name__ == "__main__":
    unittest.main()
