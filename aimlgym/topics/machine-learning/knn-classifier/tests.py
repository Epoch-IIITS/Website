"""Tests for ML-13 k-Nearest Neighbors Classifier by Hand.

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

XTR = np.array([[0, 0], [1, 0], [5, 5], [6, 5], [5, 6]]); YTR = np.array([0, 0, 1, 1, 1])

class TestKNN(unittest.TestCase):
    def test_k3(self):
        np.testing.assert_array_equal(S.knn_predict(XTR, YTR, np.array([[2, 1]]), k=3), [0])

    def test_k5_majority(self):
        np.testing.assert_array_equal(S.knn_predict(XTR, YTR, np.array([[2, 1]]), k=5), [1])

    def test_k1_training_points(self):
        np.testing.assert_array_equal(S.knn_predict(XTR, YTR, XTR, k=1), YTR)

    def test_vote_tie_nearest_wins(self):
        Xtr = np.array([[0.0], [3.0], [-2.0], [5.0]]); ytr = np.array([1, 0, 1, 0])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[1.0]]), k=4), [1])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[2.0]]), k=4), [0])

    def test_distance_tie_index(self):
        Xtr = np.array([[-1.0], [1.0]]); ytr = np.array([7, 3])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[0.0]]), k=1), [7])

    def test_not_nearest_centroid(self):
        # class-1 centroid is far away (~67), but its member at 2.0 is the nearest point to 1.2
        Xtr = np.array([[0.0], [0.1], [2.0], [100.0], [100.0]]); ytr = np.array([0, 0, 1, 1, 1])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[1.2]]), k=1), [1])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[1.2]]), k=3), [0])

    def test_bad_k(self):
        with self.assertRaises(ValueError):
            S.knn_predict(XTR, YTR, XTR, k=6)

    def test_many_queries(self):
        rng = np.random.default_rng(0)
        Xtr = np.vstack([rng.normal(0, 0.5, (30, 2)), rng.normal(4, 0.5, (30, 2))])
        ytr = np.array([0] * 30 + [1] * 30)
        q = np.array([[0, 0], [4, 4], [0.2, -0.3], [3.8, 4.1]])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, q, k=5), [0, 1, 0, 1])


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_without_ties(self):
        import numpy as np
        from sklearn.neighbors import KNeighborsClassifier
        rng = np.random.default_rng(0)
        Xtr = np.vstack([rng.normal(0, 1, (15, 2)), rng.normal(3, 1, (15, 2))])
        ytr = np.array([0] * 15 + [1] * 15)
        Xte = rng.normal(1.5, 1.5, (20, 2))
        sk = KNeighborsClassifier(n_neighbors=3).fit(Xtr, ytr)
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, Xte, k=3), sk.predict(Xte))


if __name__ == "__main__":
    unittest.main()
