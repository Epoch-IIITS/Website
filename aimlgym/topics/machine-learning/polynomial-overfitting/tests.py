"""Tests for ML-15 Polynomial Features and Overfitting by Hand.

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

X_TR = np.linspace(0, 1, 10)
NOISE = np.array([0.05, -0.05] * 5)
Y_TR = 1 + 2 * X_TR - 3 * X_TR ** 2 + NOISE
X_TE = np.linspace(0.03, 0.97, 9)
Y_TE = 1 + 2 * X_TE - 3 * X_TE ** 2


class TestPolynomial(unittest.TestCase):
    def test_features(self):
        F = S.poly_features([2.0, 3.0], 3)
        np.testing.assert_allclose(F, [[1, 2, 4, 8], [1, 3, 9, 27]])
        self.assertEqual(S.poly_features(X_TR, 0).shape, (10, 1))

    def test_exact_recovery(self):
        x = np.linspace(-1, 2, 7)
        coef = S.fit_poly(x, 1 + 2 * x - 3 * x ** 2, 2)
        np.testing.assert_allclose(coef, [1, 2, -3], atol=1e-9)

    def test_predict(self):
        np.testing.assert_allclose(S.predict_poly(np.array([1.0, 0.0, 2.0]), [0, 1, 2]), [1, 3, 9])

    def test_training_error_non_increasing(self):
        errs = S.errors_by_degree(X_TR, Y_TR, X_TE, Y_TE, range(0, 10))
        train = [errs[d][0] for d in range(10)]
        for a, b in zip(train, train[1:]):
            self.assertLessEqual(b, a + 1e-12)
        self.assertLess(errs[9][0], 1e-12)

    def test_overfitting_visible(self):
        errs = S.errors_by_degree(X_TR, Y_TR, X_TE, Y_TE, [1, 2, 9])
        self.assertGreater(errs[1][1], errs[2][1])
        self.assertGreater(errs[9][1], 10 * errs[2][1])

    def test_best_degree(self):
        errs = S.errors_by_degree(X_TR, Y_TR, X_TE, Y_TE, range(0, 10))
        self.assertEqual(S.best_degree(errs), 2)
        self.assertEqual(S.best_degree({3: (0.0, 1.0), 1: (0.5, 1.0), 2: (0.1, 2.0)}), 1)


try:
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures
except ImportError:
    LinearRegression = None


class TestAgainstLibrary(unittest.TestCase):
    def test_matches_polyfit(self):
        np.testing.assert_allclose(S.fit_poly(X_TR, Y_TR, 3), np.polyfit(X_TR, Y_TR, 3)[::-1], atol=1e-8)

    @unittest.skipIf(LinearRegression is None, "scikit-learn not installed")
    def test_matches_sklearn_pipeline(self):
        model = make_pipeline(PolynomialFeatures(3), LinearRegression()).fit(X_TR.reshape(-1, 1), Y_TR)
        ours = S.predict_poly(S.fit_poly(X_TR, Y_TR, 3), X_TE)
        np.testing.assert_allclose(ours, model.predict(X_TE.reshape(-1, 1)), atol=1e-8)


if __name__ == "__main__":
    unittest.main()
