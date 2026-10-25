"""Tests for CV-09 Intensity Histogram.

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

class TestHist(unittest.TestCase):
    def test_hist(self):
        h = S.histogram256(np.array([[0, 0], [255, 7]], dtype=np.uint8))
        self.assertEqual(len(h), 256)
        self.assertEqual((h[0], h[7], h[255], h.sum()), (2, 1, 1, 4))

    def test_dtype_check(self):
        with self.assertRaises(ValueError):
            S.histogram256(np.zeros((2, 2), dtype=float))

    def test_cdf(self):
        np.testing.assert_array_equal(S.cdf([1, 0, 2]), [1, 1, 3])

    def test_equalize(self):
        g = np.array([[50, 50], [51, 52]], dtype=np.uint8)
        np.testing.assert_array_equal(S.equalize(g), [[0, 0], [128, 255]])

    def test_full_range(self):
        g = np.array([[100, 101, 102, 103]], dtype=np.uint8)
        e = S.equalize(g)
        self.assertEqual((e.min(), e.max()), (0, 255))
        self.assertEqual(e.dtype, np.uint8)

    def test_monotone(self):
        rng = np.random.default_rng(0)
        g = rng.integers(60, 120, size=(16, 16)).astype(np.uint8)
        e = S.equalize(g)
        order = np.argsort(g.ravel(), kind="stable")
        self.assertTrue((np.diff(e.ravel()[order].astype(int)) >= 0).all())

    def test_constant(self):
        g = np.full((3, 3), 77, dtype=np.uint8)
        np.testing.assert_array_equal(S.equalize(g), g)


if __name__ == "__main__":
    unittest.main()
