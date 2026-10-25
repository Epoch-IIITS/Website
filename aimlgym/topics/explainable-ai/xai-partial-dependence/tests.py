"""Tests for XA-05 Partial Dependence with sklearn.inspection.

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
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def data(seed=0, n=300):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 3))
    return X, 2 * X[:, 0] + X[:, 1] ** 2 + rng.normal(scale=0.1, size=n)


class TestPdCurve(unittest.TestCase):
    def test_linear_slope(self):
        X, y = data()
        model = make_pipeline(StandardScaler(), LinearRegression()).fit(X, y)
        r = S.pd_curve(model, X, 0, grid_resolution=5)
        slopes = np.diff(r["values"]) / np.diff(r["grid"])
        self.assertTrue(np.allclose(slopes, model[-1].coef_[0] / model[0].scale_[0]))
        self.assertAlmostEqual(slopes[0], 2.0, delta=0.1)

    def test_u_shape_for_forest(self):
        X, y = data(1)
        model = RandomForestRegressor(50, random_state=0).fit(X, y)
        values = S.pd_curve(model, X, 1, grid_resolution=9)["values"]
        self.assertLess(values[4], values[0])
        self.assertLess(values[4], values[-1])

    def test_grid_within_percentiles(self):
        X, y = data(2)
        r = S.pd_curve(LinearRegression().fit(X, y), X, 0, grid_resolution=7)
        self.assertEqual(len(r["grid"]), 7)
        self.assertEqual(r["grid"], sorted(r["grid"]))
        lo, hi = np.percentile(X[:, 0], [2, 8]), np.percentile(X[:, 0], [92, 98])
        self.assertTrue(lo[0] <= r["grid"][0] <= lo[1] and hi[0] <= r["grid"][-1] <= hi[1])

    def test_individual_curves_average(self):
        X, y = data(3, n=60)
        model = make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(X, y)
        ice = S.pd_curve(model, X, 0, grid_resolution=4, kind="individual")
        avg = S.pd_curve(model, X, 0, grid_resolution=4)
        self.assertEqual((len(ice["values"]), len(ice["values"][0])), (60, 4))
        self.assertTrue(np.allclose(np.mean(ice["values"], axis=0), avg["values"]))

    def test_types(self):
        X, y = data(4, n=40)
        r = S.pd_curve(LinearRegression().fit(X, y), X, 2, grid_resolution=3)
        self.assertTrue(all(type(v) is float for v in r["grid"] + r["values"]))

    def test_invalid(self):
        X, y = data(5, n=20)
        model = LinearRegression().fit(X, y)
        with self.assertRaises(ValueError):
            S.pd_curve(model, X, 3)
        with self.assertRaises(ValueError):
            S.pd_curve(model, X, 0, kind="both")


if __name__ == "__main__":
    unittest.main()
