"""Tests for CV-10 2D Filtering (Blur).

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

def naive(img, K, mode):
    rh, rw = K.shape[0] // 2, K.shape[1] // 2
    P = np.pad(img, ((rh, rh), (rw, rw)), mode="constant" if mode == "zero" else "edge")
    return np.array([[(P[i:i + K.shape[0], j:j + K.shape[1]] * K).sum() for j in range(img.shape[1])]
                     for i in range(img.shape[0])])

class TestFilter2d(unittest.TestCase):
    def test_box_zero(self):
        exp = np.array([[4, 6, 4], [6, 9, 6], [4, 6, 4]]) / 9
        np.testing.assert_allclose(S.filter2d(np.ones((3, 3)), S.box_kernel(3)), exp)

    def test_box_edge(self):
        np.testing.assert_allclose(S.filter2d(np.ones((3, 3)), S.box_kernel(3), "edge"), np.ones((3, 3)))

    def test_against_naive(self):
        rng = np.random.default_rng(0)
        img, K = rng.normal(size=(6, 7)), rng.normal(size=(3, 5))
        for mode in ("zero", "edge"):
            np.testing.assert_allclose(S.filter2d(img, K, mode), naive(img, K, mode), atol=1e-12)

    def test_no_flip(self):
        img = np.zeros((3, 3)); img[1, 1] = 1
        K = np.arange(9.).reshape(3, 3)
        np.testing.assert_allclose(S.filter2d(img, K), K[::-1, ::-1])

    def test_gaussian(self):
        g = S.gaussian_kernel(5, 1.0)
        self.assertAlmostEqual(g.sum(), 1.0)
        self.assertEqual(np.unravel_index(g.argmax(), g.shape), (2, 2))
        np.testing.assert_allclose(g, g.T)

    def test_identity_kernel(self):
        img = np.random.default_rng(1).normal(size=(4, 4))
        K = np.zeros((3, 3)); K[1, 1] = 1
        np.testing.assert_allclose(S.filter2d(img, K), img)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.filter2d(np.ones((3, 3)), np.ones((2, 2)))
        with self.assertRaises(ValueError):
            S.box_kernel(4)


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_ndimage_correlate(self):
        import numpy as np
        from scipy.ndimage import correlate
        rng = np.random.default_rng(0)
        img = rng.integers(0, 255, (7, 9)).astype(float)
        K = rng.normal(size=(3, 5))
        np.testing.assert_allclose(S.filter2d(img, K), correlate(img, K, mode="constant", cval=0.0), atol=1e-9)
        np.testing.assert_allclose(S.filter2d(img, K, mode="edge"), correlate(img, K, mode="nearest"), atol=1e-9)


if __name__ == "__main__":
    unittest.main()
