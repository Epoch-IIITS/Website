"""Tests for ML-26 k-Means Clustering by Hand.

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

class TestKMeans(unittest.TestCase):
    def test_1d(self):
        r = S.kmeans(np.array([[0.], [1.], [10.], [11.]]), np.array([[0.], [1.]]))
        np.testing.assert_allclose(r["centroids"].ravel(), [0.5, 10.5])
        np.testing.assert_array_equal(r["labels"], [0, 0, 1, 1])
        self.assertAlmostEqual(r["inertia"], 1.0)

    def test_n_iter(self):
        r = S.kmeans(np.array([[0.], [1.], [10.], [11.]]), np.array([[0.], [1.]]))
        self.assertEqual(r["n_iter"], 3)

    def test_blobs(self):
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(0, 0.3, (40, 2)), rng.normal(5, 0.3, (40, 2))])
        r = S.kmeans(X, X[[0, 79]])
        self.assertEqual(len(set(r["labels"][:40])), 1)
        self.assertEqual(len(set(r["labels"][40:])), 1)

    def test_empty_cluster_kept(self):
        r = S.kmeans(np.array([[0.], [0.2]]), np.array([[0.], [100.]]))
        np.testing.assert_allclose(r["centroids"].ravel(), [0.1, 100.0])

    def test_inertia_matches(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(30, 3))
        r = S.kmeans(X, X[:3])
        C, lab = r["centroids"], r["labels"]
        self.assertAlmostEqual(r["inertia"], float(((X - C[lab]) ** 2).sum()), places=10)

    def test_monotone_with_iterations(self):
        rng = np.random.default_rng(4)
        X = rng.normal(size=(50, 2))
        inert = [S.kmeans(X, X[:4], max_iter=m)["inertia"] for m in (1, 2, 5, 50)]
        self.assertTrue(all(inert[i + 1] <= inert[i] + 1e-12 for i in range(3)))

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.kmeans(np.zeros((2, 2)), np.zeros((3, 2)))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_lloyd(self):
        import numpy as np
        from sklearn.cluster import KMeans
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(c, 0.5, (20, 2)) for c in (0.0, 4.0, 8.0)])
        init = X[[0, 25, 45]]
        ours = S.kmeans(X, init)
        sk = KMeans(n_clusters=3, init=init, n_init=1, algorithm="lloyd", tol=0).fit(X)
        np.testing.assert_allclose(ours["centroids"], sk.cluster_centers_, atol=1e-8)
        np.testing.assert_array_equal(ours["labels"], sk.labels_)
        self.assertAlmostEqual(ours["inertia"], sk.inertia_, places=6)


if __name__ == "__main__":
    unittest.main()
