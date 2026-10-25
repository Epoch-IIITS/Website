"""Tests for ML-19 Regularisation and Hyperparameter Search.

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
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def noisy(seed=0, n=40, d=30):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)); w = np.zeros(d); w[:3] = [3.0, -2.0, 1.5]
    return X, X @ w + rng.normal(scale=2.0, size=n)


class TestTuneRidge(unittest.TestCase):
    def test_norms_shrink(self):
        X, y = noisy()
        r = S.tune_ridge(X, y, [0.01, 0.1, 1, 10, 100])
        for a, b in zip(r["coef_norms"], r["coef_norms"][1:]):
            self.assertLess(b, a)

    def test_middle_alpha_wins(self):
        X, y = noisy()
        r = S.tune_ridge(X, y, [0.001, 3, 10000])
        self.assertEqual(r["best_alpha"], 3.0)
        self.assertAlmostEqual(r["best_mse"], min(r["mse_by_alpha"]))

    def test_mse_matches_cross_val_score(self):
        X, y = noisy(1)
        r = S.tune_ridge(X, y, [0.5, 5], n_splits=4, seed=2)
        for alpha, mse in zip([0.5, 5], r["mse_by_alpha"]):
            scores = cross_val_score(make_pipeline(StandardScaler(), Ridge(alpha=alpha)), X, y,
                                     cv=KFold(4, shuffle=True, random_state=2), scoring="neg_mean_squared_error")
            self.assertAlmostEqual(mse, float(-scores.mean()), places=9)

    def test_best_model_refit_on_all_data(self):
        X, y = noisy(2)
        r = S.tune_ridge(X, y, [0.1, 1, 10])
        ref = make_pipeline(StandardScaler(), Ridge(alpha=r["best_alpha"])).fit(X, y)
        self.assertTrue(np.allclose(r["model"].predict(X), ref.predict(X)))

    def test_types(self):
        X, y = noisy(3)
        r = S.tune_ridge(X, y, [1, 10])
        self.assertIs(type(r["best_alpha"]), float)
        self.assertTrue(all(type(v) is float and v > 0 for v in r["mse_by_alpha"] + r["coef_norms"]))

    def test_invalid(self):
        X, y = noisy()
        for alphas in ([], [1, 0], [-1]):
            with self.assertRaises(ValueError):
                S.tune_ridge(X, y, alphas)


if __name__ == "__main__":
    unittest.main()
