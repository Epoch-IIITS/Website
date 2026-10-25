"""Tests for XA-07 Permutation Importance with sklearn.inspection.

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
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def frame(seed, n=300):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({"x0": rng.normal(size=n), "x1": rng.normal(size=n), "noise": rng.normal(size=n),
                      "city": rng.choice(["a", "b", "c"], n)})
    y = 3 * X["x0"] + 0.5 * X["x1"] + X["city"].map({"a": 0.0, "b": 2.0, "c": -2.0}) + rng.normal(scale=0.1, size=n)
    return X, y


def pipeline():
    prep = ColumnTransformer([("num", "passthrough", ["x0", "x1", "noise"]),
                              ("cat", OneHotEncoder(sparse_output=False), ["city"])])
    return Pipeline([("prep", prep), ("model", LinearRegression())])


class TestImportanceTable(unittest.TestCase):
    def test_order(self):
        X, y = frame(0)
        Xt, yt = frame(1)
        table = S.importance_table(pipeline().fit(X, y), Xt, yt)
        self.assertEqual([row[0] for row in table][:2], ["x0", "city"])
        self.assertEqual(table[-1][0], "noise")

    def test_original_columns(self):
        X, y = frame(2)
        table = S.importance_table(pipeline().fit(X, y), X, y, n_repeats=3)
        self.assertEqual(sorted(row[0] for row in table), ["city", "noise", "x0", "x1"])

    def test_noise_near_zero(self):
        X, y = frame(3)
        Xt, yt = frame(4)
        noise = {r[0]: r for r in S.importance_table(pipeline().fit(X, y), Xt, yt)}["noise"]
        self.assertLess(abs(noise[1]), 0.01)

    def test_matches_library(self):
        X, y = frame(5)
        model = pipeline().fit(X, y)
        table = S.importance_table(model, X, y, n_repeats=4, seed=2, scoring="r2")
        ref = permutation_importance(model, X, y, n_repeats=4, random_state=2, scoring="r2")
        means = dict(zip(X.columns, ref.importances_mean))
        for column, mean, std in table:
            self.assertAlmostEqual(mean, float(means[column]))

    def test_types_and_reproducible(self):
        X, y = frame(6, n=80)
        model = pipeline().fit(X, y)
        a = S.importance_table(model, X, y, n_repeats=3, seed=1)
        self.assertEqual(a, S.importance_table(model, X, y, n_repeats=3, seed=1))
        self.assertTrue(all(type(m) is float and type(s) is float for _, m, s in a))

    def test_invalid(self):
        X, y = frame(7, n=20)
        model = pipeline().fit(X, y)
        with self.assertRaises(ValueError):
            S.importance_table(model, X.to_numpy(), y)
        with self.assertRaises(ValueError):
            S.importance_table(model, X, y, n_repeats=0)


if __name__ == "__main__":
    unittest.main()
