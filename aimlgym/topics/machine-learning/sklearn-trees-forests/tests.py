"""Tests for ML-22 Decision Trees and Random Forests.

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


def signal_and_noise(seed, n=300, flip=0.15):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 5))
    y = (X[:, 0] + 0.3 * X[:, 1] > 0).astype(int)
    noise = rng.random(n) < flip
    return X, np.where(noise, 1 - y, y)


class TestTreeForest(unittest.TestCase):
    def test_unlimited_tree_memorises(self):
        X, y = signal_and_noise(0)
        Xt, yt = signal_and_noise(1)
        r = S.compare_tree_forest(X, y, Xt, yt)
        self.assertEqual(r["tree_train_accuracy"], 1.0)
        self.assertLess(r["tree_test_accuracy"], 0.9)

    def test_forest_beats_single_tree(self):
        X, y = signal_and_noise(2)
        Xt, yt = signal_and_noise(3, n=1000)
        r = S.compare_tree_forest(X, y, Xt, yt, n_estimators=200)
        self.assertGreater(r["forest_test_accuracy"], r["tree_test_accuracy"])

    def test_depth_limit(self):
        X, y = signal_and_noise(4)
        r = S.compare_tree_forest(X, y, X, y, max_depth=2)
        self.assertLessEqual(r["tree_depth"], 2)
        self.assertLess(r["tree_train_accuracy"], 1.0)

    def test_importances(self):
        X, y = signal_and_noise(5)
        r = S.compare_tree_forest(X, y, X, y, n_estimators=50)
        self.assertEqual(r["top_feature"], 0)
        self.assertEqual(len(r["importances"]), 5)
        self.assertAlmostEqual(sum(r["importances"]), 1.0)

    def test_reproducible(self):
        X, y = signal_and_noise(6)
        a = S.compare_tree_forest(X, y, X[:50], y[:50], n_estimators=30, seed=4)
        b = S.compare_tree_forest(X, y, X[:50], y[:50], n_estimators=30, seed=4)
        self.assertEqual(a, b)

    def test_invalid(self):
        X, y = signal_and_noise(7, n=20)
        with self.assertRaises(ValueError):
            S.compare_tree_forest(X, y, X, y, n_estimators=0)


if __name__ == "__main__":
    unittest.main()
