"""Tests for CV-07 Binary Thresholding.

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

G = np.array([[10, 200], [128, 127]])

class TestThreshold(unittest.TestCase):
    def test_threshold(self):
        np.testing.assert_array_equal(S.threshold(G, 127), [[False, True], [True, False]])

    def test_invert(self):
        np.testing.assert_array_equal(S.threshold(G, 127, invert=True), [[True, False], [False, True]])

    def test_fraction(self):
        self.assertEqual(S.foreground_fraction(S.threshold(G, 127)), 0.5)

    def test_apply_gray(self):
        np.testing.assert_array_equal(S.apply_mask(G, S.threshold(G, 127)), [[0, 200], [128, 0]])

    def test_apply_color(self):
        img = np.full((2, 2, 3), 9, dtype=np.uint8)
        out = S.apply_mask(img, np.array([[True, False], [False, True]]))
        np.testing.assert_array_equal(out[0, 1], [0, 0, 0])
        np.testing.assert_array_equal(out[1, 1], [9, 9, 9])
        self.assertEqual(out.dtype, np.uint8)

    def test_shape_mismatch(self):
        with self.assertRaises(ValueError):
            S.apply_mask(G, np.ones((3, 3), bool))

    def test_no_mutation(self):
        g = G.copy()
        S.apply_mask(g, np.zeros((2, 2), bool))
        np.testing.assert_array_equal(g, G)


if __name__ == "__main__":
    unittest.main()
