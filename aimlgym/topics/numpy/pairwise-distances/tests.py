"""Tests for NP-11 Vectorized Pairwise Distances.

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

class TestPairwise(unittest.TestCase):
    def test_example(self):
        A = np.array([[0., 0.], [1., 1.]]); B = np.array([[1., 0.], [3., 4.]])
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), [[1, 25], [1, 13]], atol=1e-12)

    def test_against_loops(self):
        rng = np.random.default_rng(0)
        A, B = rng.normal(size=(7, 3)), rng.normal(size=(5, 3))
        ref = np.array([[((a - b) ** 2).sum() for b in B] for a in A])
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), ref, rtol=1e-10, atol=1e-10)

    def test_self_zero_diag_nonneg(self):
        A = np.array([[1e8, 1.0], [1e8 + 1, 2.0]])
        D = S.pairwise_sq_dists(A, A)
        self.assertTrue((D >= 0).all())
        self.assertEqual(D.shape, (2, 2))

    def test_nearest(self):
        A = np.array([[0., 0.], [1., 1.]]); B = np.array([[1., 0.], [3., 4.]])
        np.testing.assert_array_equal(S.nearest(A, B), [0, 0])

    def test_nearest_tie(self):
        np.testing.assert_array_equal(S.nearest(np.array([[0., 0.]]), np.array([[1., 0.], [-1., 0.]])), [0])

    def test_dim_mismatch(self):
        with self.assertRaises(ValueError):
            S.pairwise_sq_dists(np.zeros((2, 3)), np.zeros((2, 2)))

    def test_shape(self):
        self.assertEqual(S.pairwise_sq_dists(np.zeros((4, 2)), np.zeros((9, 2))).shape, (4, 9))


try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_double_loop(self):
        import numpy as np
        rng = np.random.default_rng(0)
        A, B = rng.normal(size=(4, 3)), rng.normal(size=(5, 3))
        loop = [[sum((a - b) ** 2 for a, b in zip(r, s)) for s in B] for r in A]
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), loop, atol=1e-10)

    @unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
    def test_library_matches_cdist(self):
        import numpy as np
        from scipy.spatial.distance import cdist
        rng = np.random.default_rng(1)
        A, B = rng.normal(size=(6, 4)), rng.normal(size=(3, 4))
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), cdist(A, B, "sqeuclidean"), atol=1e-10)


if __name__ == "__main__":
    unittest.main()
