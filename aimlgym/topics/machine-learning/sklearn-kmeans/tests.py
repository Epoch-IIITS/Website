"""Tests for ML-25 k-Means and Silhouette Scores.

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
from sklearn.cluster import KMeans


def three_blobs(seed=0, n=40):
    rng = np.random.default_rng(seed)
    centres = np.array([[0, 0], [6, 0], [3, 6]])
    return np.vstack([rng.normal(c, 0.6, size=(n, 2)) for c in centres])


class TestChooseK(unittest.TestCase):
    def test_three_blobs(self):
        r = S.choose_k(three_blobs(), [2, 3, 4, 5])
        self.assertEqual(r["best_k"], 3)
        self.assertEqual(len(set(r["labels"])), 3)

    def test_inertia_decreases(self):
        r = S.choose_k(three_blobs(1), [2, 3, 4, 5])
        for a, b in zip(r["inertia"], r["inertia"][1:]):
            self.assertLess(b, a)

    def test_matches_kmeans(self):
        X = three_blobs(2)
        r = S.choose_k(X, [3], seed=5)
        km = KMeans(n_clusters=3, n_init=10, random_state=5).fit(X)
        self.assertAlmostEqual(r["inertia"][0], float(km.inertia_))
        self.assertEqual(r["labels"], km.labels_.tolist())

    def test_silhouette_range(self):
        r = S.choose_k(three_blobs(3), [2, 3, 6])
        self.assertTrue(all(-1 <= s <= 1 for s in r["silhouette"]))
        self.assertGreater(max(r["silhouette"]), 0.5)

    def test_types(self):
        r = S.choose_k(three_blobs(4), [2, 3])
        self.assertTrue(all(type(v) is float for v in r["inertia"] + r["silhouette"]))
        self.assertTrue(all(type(v) is int for v in r["labels"]))
        self.assertEqual(len(r["labels"]), 120)

    def test_invalid(self):
        X = three_blobs(n=2)
        for ks in ([], [1], [6]):
            with self.assertRaises(ValueError):
                S.choose_k(X, ks)


if __name__ == "__main__":
    unittest.main()
