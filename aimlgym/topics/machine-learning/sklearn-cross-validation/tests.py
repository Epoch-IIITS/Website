"""Tests for ML-16 Cross-Validation with scikit-learn.

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
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold, StratifiedKFold


def regression_data(seed=0, n=50):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 3))
    return X, X @ np.array([2.0, -1.0, 0.5]) + rng.normal(scale=0.5, size=n)


class TestCvReport(unittest.TestCase):
    def test_matches_manual_loop(self):
        X, y = regression_data()
        r = S.cv_report(LinearRegression(), X, y, n_splits=5, seed=1)
        manual = []
        for train, test in KFold(5, shuffle=True, random_state=1).split(X):
            manual.append(LinearRegression().fit(X[train], y[train]).score(X[test], y[test]))
        self.assertEqual(len(r["scores"]), 5)
        for a, b in zip(r["scores"], manual):
            self.assertAlmostEqual(a, b, places=10)

    def test_mean_and_std(self):
        X, y = regression_data(1)
        r = S.cv_report(LinearRegression(), X, y)
        self.assertAlmostEqual(r["mean"], float(np.mean(r["scores"])))
        self.assertAlmostEqual(r["std"], float(np.std(r["scores"])))

    def test_model_not_fitted(self):
        X, y = regression_data(2)
        model = LinearRegression()
        S.cv_report(model, X, y)
        self.assertFalse(hasattr(model, "coef_"))

    def test_stratified_folds(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(40, 2)); y = np.array([0] * 30 + [1] * 10)
        r = S.cv_report(LogisticRegression(), X, y, n_splits=5, seed=0, stratified=True, scoring="accuracy")
        manual = []
        for train, test in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
            self.assertEqual(int(y[test].sum()), 2)
            manual.append(LogisticRegression().fit(X[train], y[train]).score(X[test], y[test]))
        self.assertTrue(np.allclose(r["scores"], manual))

    def test_scoring_argument(self):
        X, y = regression_data(4)
        r = S.cv_report(LinearRegression(), X, y, scoring="neg_mean_squared_error")
        self.assertTrue(all(s <= 0 for s in r["scores"]))
        self.assertTrue(all(type(s) is float for s in r["scores"]))

    def test_invalid(self):
        X, y = regression_data()
        with self.assertRaises(ValueError):
            S.cv_report(LinearRegression(), X, y, n_splits=1)
        with self.assertRaises(ValueError):
            S.cv_report(LinearRegression(), X, y[:-1])


if __name__ == "__main__":
    unittest.main()
