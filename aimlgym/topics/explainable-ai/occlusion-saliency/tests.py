"""Tests for XA-09 Occlusion Saliency Map.

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

class TestOcclusion(unittest.TestCase):
    def test_example(self):
        score = lambda im: float(im[:2, :2].sum())
        np.testing.assert_allclose(S.occlusion_map(score, np.ones((4, 4)), 2), [[4, 0], [0, 0]])

    def test_edge_patches(self):
        out = S.occlusion_map(lambda im: float(im.sum()), np.ones((5, 3)), 2)
        self.assertEqual(out.shape, (3, 2))
        np.testing.assert_allclose(out, [[4, 2], [4, 2], [2, 1]])

    def test_linear_model(self):
        rng = np.random.default_rng(0)
        Wt, img = rng.normal(size=(4, 4)), rng.normal(size=(4, 4))
        out = S.occlusion_map(lambda im: float((Wt * im).sum()), img, 1)
        np.testing.assert_allclose(out, Wt * img)

    def test_baseline_value(self):
        out = S.occlusion_map(lambda im: float(im.sum()), np.full((2, 2), 3.0), 2, baseline=1.0)
        np.testing.assert_allclose(out, [[8.0]])

    def test_no_mutation(self):
        img = np.ones((2, 2))
        S.occlusion_map(lambda im: float(im.sum()), img, 1)
        np.testing.assert_array_equal(img, np.ones((2, 2)))

    def test_irrelevant_region_zero(self):
        out = S.occlusion_map(lambda im: float(im[0, 0]), np.arange(16.).reshape(4, 4) + 1, 2)
        self.assertEqual(out[1, 1], 0.0)

    def test_bad_patch(self):
        with self.assertRaises(ValueError):
            S.occlusion_map(lambda im: 0.0, np.ones((2, 2)), 0)


if __name__ == "__main__":
    unittest.main()
