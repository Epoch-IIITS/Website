"""Tests for CV-12 Sobel Edge Magnitude.

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

class TestSobel(unittest.TestCase):
    def test_vertical_edge(self):
        g = np.array([[0, 0, 10, 10]] * 4, float)
        gx, gy, mag = S.sobel(g)
        np.testing.assert_allclose(gx, 40)
        np.testing.assert_allclose(gy, 0)
        np.testing.assert_allclose(mag, 40)

    def test_horizontal_edge(self):
        g = np.array([[0] * 4, [0] * 4, [10] * 4, [10] * 4], float)
        gx, gy, _ = S.sobel(g)
        np.testing.assert_allclose(gx, 0)
        np.testing.assert_allclose(gy, 40)

    def test_flat(self):
        _, _, mag = S.sobel(np.full((5, 5), 7.0))
        np.testing.assert_allclose(mag, 0)

    def test_ramp(self):
        g = np.tile(np.arange(6.0), (5, 1))
        gx, _, _ = S.sobel(g)
        np.testing.assert_allclose(gx, 8.0)

    def test_shape_and_uint8(self):
        g = np.array([[0, 255, 0]] * 3, dtype=np.uint8)
        gx, _, _ = S.sobel(g)
        self.assertEqual(gx.shape, (1, 1))
        self.assertEqual(gx[0, 0], 0.0)
        g2 = np.array([[255, 0, 0]] * 3, dtype=np.uint8)
        self.assertEqual(S.sobel(g2)[0][0, 0], -1020.0)

    def test_edges(self):
        g = np.array([[0, 0, 10, 10]] * 4, float)
        np.testing.assert_array_equal(S.edges(g, 39), True)
        np.testing.assert_array_equal(S.edges(g, 40), False)

    def test_small(self):
        with self.assertRaises(ValueError):
            S.sobel(np.zeros((2, 5)))


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_ndimage_sobel(self):
        import numpy as np
        from scipy import ndimage
        rng = np.random.default_rng(1)
        img = rng.random((6, 7))
        gx, gy, _ = S.sobel(img)
        np.testing.assert_allclose(gx, ndimage.sobel(img, axis=1)[1:-1, 1:-1], atol=1e-12)
        np.testing.assert_allclose(gy, ndimage.sobel(img, axis=0)[1:-1, 1:-1], atol=1e-12)


if __name__ == "__main__":
    unittest.main()
