"""Tests for ML-12 k-Nearest Neighbours with scikit-learn.

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
from sklearn.neighbors import KNeighborsClassifier


def blobs(seed, n=40):
    rng = np.random.default_rng(seed)
    X = np.vstack([rng.normal(0, 1, size=(n, 2)), rng.normal(2.5, 1, size=(n, 2))]) * [1, 50]
    return X, np.array([0] * n + [1] * n)


class TestKnnByK(unittest.TestCase):
    def test_separable_points(self):
        X = [[0, 0], [0, 1], [1, 0], [10, 10], [10, 11], [11, 10]]
        y = [0, 0, 0, 1, 1, 1]
        r = S.knn_accuracy_by_k(X, y, [[0.5, 0.5], [10.5, 10.5]], [0, 1], [1, 3])
        self.assertEqual(r["accuracy"], {1: 1.0, 3: 1.0})
        self.assertEqual(r["best_k"], 1)

    def test_matches_manual_scaled_knn(self):
        X, y = blobs(0)
        Xte, yte = blobs(1, 20)
        r = S.knn_accuracy_by_k(X, y, Xte, yte, [5])
        mu, sd = X.mean(axis=0), X.std(axis=0)
        manual = KNeighborsClassifier(5).fit((X - mu) / sd, y).predict((Xte - mu) / sd)
        self.assertAlmostEqual(r["accuracy"][5], float(np.mean(manual == yte)))

    def test_huge_k_predicts_majority(self):
        X = [[0], [1], [2], [3], [4]]
        y = [0, 0, 0, 1, 1]
        r = S.knn_accuracy_by_k(X, y, [[4], [3.5]], [1, 1], [1, 5])
        self.assertEqual(r["accuracy"][5], 0.0)
        self.assertEqual(r["accuracy"][1], 1.0)
        self.assertEqual(r["best_k"], 1)

    def test_tie_prefers_smaller_k(self):
        X, y = blobs(2)
        r = S.knn_accuracy_by_k(X, y, X[:4], y[:4], [9, 3, 5])
        best = max(r["accuracy"].values())
        self.assertEqual(r["best_k"], min(k for k, a in r["accuracy"].items() if a == best))

    def test_float_accuracies(self):
        X, y = blobs(3)
        r = S.knn_accuracy_by_k(X, y, X, y, [1, 15])
        self.assertTrue(all(type(a) is float and 0 <= a <= 1 for a in r["accuracy"].values()))
        self.assertEqual(r["accuracy"][1], 1.0)

    def test_invalid_k(self):
        for ks in ([], [0], [100]):
            with self.assertRaises(ValueError):
                S.knn_accuracy_by_k([[0], [1]], [0, 1], [[0]], [0], ks)


if __name__ == "__main__":
    unittest.main()
