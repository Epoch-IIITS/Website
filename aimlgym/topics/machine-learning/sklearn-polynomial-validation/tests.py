"""Tests for ML-14 Polynomial Features and Validation Curves.

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
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold


def quadratic(seed=0, n=40):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-3, 3, n)
    return x, x ** 2 + rng.normal(scale=1.0, size=n)


class TestDegreeCurve(unittest.TestCase):
    def test_quadratic_best_degree(self):
        x, y = quadratic()
        r = S.degree_curve(x, y, [1, 2, 10])
        self.assertEqual(r["best_degree"], 2)

    def test_underfit_line(self):
        x, y = quadratic()
        r = S.degree_curve(x, y, [1, 2])
        self.assertGreater(r["val_mse"][0], 5 * r["val_mse"][1])
        self.assertGreater(r["train_mse"][0], 5 * r["train_mse"][1])

    def test_training_error_never_rises(self):
        x, y = quadratic(1)
        r = S.degree_curve(x, y, [1, 2, 3, 4, 5, 6])
        for a, b in zip(r["train_mse"], r["train_mse"][1:]):
            self.assertLessEqual(b, a + 1e-9)

    def test_degree_one_matches_manual_cv(self):
        x, y = quadratic(2)
        r = S.degree_curve(x, y, [1], n_splits=4, seed=5)
        errors = []
        for train, test in KFold(4, shuffle=True, random_state=5).split(x):
            model = LinearRegression().fit(x[train].reshape(-1, 1), y[train])
            errors.append(np.mean((model.predict(x[test].reshape(-1, 1)) - y[test]) ** 2))
        self.assertAlmostEqual(r["val_mse"][0], float(np.mean(errors)), places=9)

    def test_types_and_lengths(self):
        x, y = quadratic(3)
        r = S.degree_curve(list(x), list(y), [1, 2, 3])
        self.assertEqual((len(r["train_mse"]), len(r["val_mse"])), (3, 3))
        self.assertTrue(all(type(v) is float and v >= 0 for v in r["train_mse"] + r["val_mse"]))
        self.assertIs(type(r["best_degree"]), int)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.degree_curve([1, 2, 3], [1, 2, 3], [])
        with self.assertRaises(ValueError):
            S.degree_curve([1, 2, 3], [1, 2], [1])


if __name__ == "__main__":
    unittest.main()
