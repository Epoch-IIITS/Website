"""Tests for CV-14 2D Max Pooling.

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

X = np.arange(1, 17).reshape(4, 4)

class TestPool(unittest.TestCase):
    def test_max(self):
        np.testing.assert_array_equal(S.pool2d(X), [[6, 8], [14, 16]])

    def test_avg(self):
        np.testing.assert_allclose(S.pool2d(X, mode="avg"), [[3.5, 5.5], [11.5, 13.5]])

    def test_overlap(self):
        np.testing.assert_array_equal(S.pool2d(X, size=3, stride=1), [[11, 12], [15, 16]])

    def test_crop(self):
        x = np.arange(25).reshape(5, 5)
        out = S.pool2d(x, 2)
        self.assertEqual(out.shape, (2, 2))
        np.testing.assert_array_equal(out, [[6, 8], [16, 18]])

    def test_shape_formula(self):
        x = np.zeros((10, 7))
        self.assertEqual(S.pool2d(x, 3, 2).shape, ((10 - 3) // 2 + 1, (7 - 3) // 2 + 1))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.pool2d(X, size=5)
        with self.assertRaises(ValueError):
            S.pool2d(X, mode="min")


try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_library_matches_torch_pooling(self):
        import numpy as np
        x = np.random.default_rng(0).normal(size=(7, 8))
        t = torch.tensor(x)[None, None]
        F = torch.nn.functional
        np.testing.assert_allclose(S.pool2d(x, 2), F.max_pool2d(t, 2)[0, 0].numpy())
        np.testing.assert_allclose(S.pool2d(x, 3, 2, mode="avg"), F.avg_pool2d(t, 3, 2)[0, 0].numpy())


if __name__ == "__main__":
    unittest.main()
