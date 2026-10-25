"""Tests for ML-02 The scikit-learn Estimator API.

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
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression


class TestEvaluateRegressor(unittest.TestCase):
    def test_linear_example(self):
        r = S.evaluate_regressor(LinearRegression(), [[1], [2], [3], [4]], [3, 5, 7, 9], [[5], [6]], [11, 14])
        self.assertEqual([round(v, 9) for v in r["predictions"]], [11.0, 13.0])
        self.assertAlmostEqual(r["mse"], 0.5)
        self.assertAlmostEqual(r["mae"], 0.5)

    def test_original_model_not_fitted(self):
        model = LinearRegression()
        r = S.evaluate_regressor(model, [[1], [2], [3]], [1, 2, 3], [[4]], [4])
        self.assertFalse(hasattr(model, "coef_"))
        self.assertIsNot(r["model"], model)
        self.assertTrue(hasattr(r["model"], "coef_"))

    def test_clone_keeps_settings(self):
        model = DummyRegressor(strategy="median")
        r = S.evaluate_regressor(model, [[0], [1], [2]], [1, 2, 10], [[3]], [2])
        self.assertEqual(r["model"].get_params()["strategy"], "median")
        self.assertEqual(r["predictions"], [2.0])

    def test_metrics_match_formulas(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(40, 2)); y = X @ np.array([1.5, -2.0]) + rng.normal(scale=0.3, size=40)
        r = S.evaluate_regressor(LinearRegression(), X[:30], y[:30], X[30:], y[30:])
        pred, yt = np.array(r["predictions"]), y[30:]
        self.assertAlmostEqual(r["mse"], float(np.mean((yt - pred) ** 2)), places=10)
        self.assertAlmostEqual(r["mae"], float(np.mean(np.abs(yt - pred))), places=10)
        self.assertAlmostEqual(r["r2"], 1 - np.sum((yt - pred) ** 2) / np.sum((yt - yt.mean()) ** 2), places=10)

    def test_mean_baseline_r2(self):
        r = S.evaluate_regressor(DummyRegressor(), [[0], [1], [2], [3]], [1, 2, 3, 6], [[4], [5]], [3, 3])
        self.assertEqual(r["predictions"], [3.0, 3.0])
        self.assertEqual(r["mse"], 0.0)

    def test_plain_floats_and_validation(self):
        r = S.evaluate_regressor(LinearRegression(), [[1], [2]], [1, 2], [[3], [4]], [3, 5])
        self.assertTrue(all(type(r[k]) is float for k in ("mse", "mae", "r2")))
        self.assertTrue(all(type(v) is float for v in r["predictions"]))
        with self.assertRaises(ValueError):
            S.evaluate_regressor(LinearRegression(), [[1], [2]], [1], [[3]], [3])


if __name__ == "__main__":
    unittest.main()
