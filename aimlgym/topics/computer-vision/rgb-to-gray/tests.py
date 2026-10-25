"""Tests for CV-02 RGB to Grayscale.

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

IMG = np.array([[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]], dtype=np.uint8)

class TestGray(unittest.TestCase):
    def test_values(self):
        np.testing.assert_allclose(S.rgb_to_gray(IMG), [[76.245, 149.685], [29.07, 255.0]])

    def test_uint8(self):
        np.testing.assert_array_equal(S.to_uint8(S.rgb_to_gray(IMG)), [[76, 150], [29, 255]])

    def test_no_overflow(self):
        g = S.rgb_to_gray(np.full((1, 1, 3), 255, dtype=np.uint8))
        self.assertAlmostEqual(float(g[0, 0]), 255.0)

    def test_clip_round(self):
        np.testing.assert_array_equal(S.to_uint8(np.array([-5., 300., 12.5, 12.6])), [0, 255, 12, 13])
        self.assertEqual(S.to_uint8(np.array([1.0])).dtype, np.uint8)

    def test_shape(self):
        self.assertEqual(S.rgb_to_gray(np.zeros((4, 5, 3))).shape, (4, 5))

    def test_bad_shape(self):
        with self.assertRaises(ValueError):
            S.rgb_to_gray(np.zeros((4, 4)))


if __name__ == "__main__":
    unittest.main()
