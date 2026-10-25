"""Tests for ML-23 Gradient Boosting.

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
from sklearn.ensemble import HistGradientBoostingClassifier


def noisy_moons(seed, n=300):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4))
    y = ((X[:, 0] ** 2 + X[:, 1] > 0.5).astype(int))
    flip = rng.random(n) < 0.2
    return X, np.where(flip, 1 - y, y)


class TestBoostingCurve(unittest.TestCase):
    def test_curve_lengths(self):
        X, y = noisy_moons(0)
        Xv, yv = noisy_moons(1)
        r = S.boosting_curve(X, y, Xv, yv, max_iter=30)
        self.assertEqual((len(r["train_loss"]), len(r["val_loss"])), (30, 30))

    def test_training_loss_falls(self):
        X, y = noisy_moons(2)
        r = S.boosting_curve(X, y, X[:50], y[:50], max_iter=60, learning_rate=0.3)
        self.assertLess(r["train_loss"][-1], 0.6 * r["train_loss"][0])
        self.assertLess(r["train_loss"][-1], r["train_loss"][len(r["train_loss"]) // 2])

    def test_validation_overfits_late(self):
        X, y = noisy_moons(3)
        Xv, yv = noisy_moons(4, n=600)
        r = S.boosting_curve(X, y, Xv, yv, max_iter=200, learning_rate=0.5)
        self.assertLess(r["best_iteration"], 200)
        self.assertGreater(r["val_loss"][-1], min(r["val_loss"]))
        self.assertEqual(r["val_loss"][r["best_iteration"] - 1], min(r["val_loss"]))

    def test_final_accuracy(self):
        X, y = noisy_moons(5)
        Xv, yv = noisy_moons(6)
        r = S.boosting_curve(X, y, Xv, yv, max_iter=40, seed=1)
        ref = HistGradientBoostingClassifier(max_iter=40, early_stopping=False, random_state=1).fit(X, y)
        self.assertAlmostEqual(r["val_accuracy"], float(ref.score(Xv, yv)))
        self.assertGreater(r["val_accuracy"], 0.65)

    def test_types(self):
        X, y = noisy_moons(7, n=80)
        r = S.boosting_curve(X, y, X, y, max_iter=5)
        self.assertTrue(all(type(v) is float for v in r["train_loss"] + r["val_loss"]))
        self.assertIs(type(r["best_iteration"]), int)

    def test_invalid(self):
        X, y = noisy_moons(8, n=40)
        with self.assertRaises(ValueError):
            S.boosting_curve(X, y, X, y, max_iter=0)
        with self.assertRaises(ValueError):
            S.boosting_curve(X, y, X, y, learning_rate=0)


if __name__ == "__main__":
    unittest.main()
