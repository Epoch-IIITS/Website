"""Tests for NL-11 Cosine Similarity Retrieval.

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

D = np.array([[2., 2., 0.], [0., 0., 5.], [1., 0., 0.]])

class TestRetrieval(unittest.TestCase):
    def test_search(self):
        r = S.search(np.array([1., 1., 0.]), D, 2)
        self.assertEqual([i for i, _ in r], [0, 2])
        self.assertAlmostEqual(r[0][1], 1.0)
        self.assertAlmostEqual(r[1][1], 1 / np.sqrt(2))

    def test_matrix(self):
        C = S.cosine_matrix(D, D)
        np.testing.assert_allclose(np.diag(C), 1.0)
        self.assertAlmostEqual(C[0, 1], 0.0)

    def test_zero_vector(self):
        C = S.cosine_matrix(np.zeros((1, 3)), D)
        np.testing.assert_array_equal(C, [[0, 0, 0]])

    def test_length_invariance(self):
        a = S.cosine_matrix(np.array([[1., 2., 3.]]), np.array([[2., 4., 6.]]))
        self.assertAlmostEqual(a[0, 0], 1.0)

    def test_ties_stable(self):
        r = S.search(np.array([1., 0.]), np.array([[1., 0.], [3., 0.], [0., 1.]]), 3)
        self.assertEqual([i for i, _ in r], [0, 1, 2])

    def test_bad_k(self):
        with self.assertRaises(ValueError):
            S.search(np.array([1., 0., 0.]), D, 4)


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_cosine_similarity(self):
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        rng = np.random.default_rng(0)
        A, B = rng.random((3, 5)), rng.random((4, 5))
        np.testing.assert_allclose(S.cosine_matrix(A, B), cosine_similarity(A, B), atol=1e-12)


if __name__ == "__main__":
    unittest.main()
