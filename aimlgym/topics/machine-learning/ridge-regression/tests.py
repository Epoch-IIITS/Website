"""Tests for ML-20 Ridge Regression (Closed Form).

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

class TestRidge(unittest.TestCase):
    def test_collinear(self):
        X = np.array([[1., 1.], [2., 2.], [3., 3.]]); y = np.array([2., 4., 6.])
        np.testing.assert_allclose(S.Ridge(alpha=1e-6).fit(X, y).coef_, [1, 1], atol=1e-5)

    def test_alpha0_is_ols(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(40, 3)); y = X @ [1., -2., 3.] + 5 + rng.normal(0, 0.1, 40)
        m = S.Ridge(alpha=0.0).fit(X, y)
        sol = np.linalg.lstsq(np.column_stack([np.ones(40), X]), y, rcond=None)[0]
        np.testing.assert_allclose(np.r_[m.intercept_, m.coef_], sol, atol=1e-10)

    def test_shrinkage(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(50, 4)); y = X @ [3., -1., 2., 0.5] + rng.normal(0, 0.5, 50)
        norms = [np.linalg.norm(S.Ridge(alpha=a).fit(X, y).coef_) for a in (0.0, 1.0, 10.0, 1000.0)]
        self.assertTrue(all(norms[i + 1] < norms[i] for i in range(3)))

    def test_large_alpha_predicts_mean(self):
        X = np.array([[0.], [1.], [2.]]); y = np.array([1., 2., 6.])
        np.testing.assert_allclose(S.Ridge(alpha=1e12).fit(X, y).predict(X), y.mean(), atol=1e-6)

    def test_intercept_not_penalised(self):
        X = np.array([[0.], [0.], [0.]]); y = np.array([10., 10., 10.])
        m = S.Ridge(alpha=100.0).fit(X, y)
        self.assertAlmostEqual(m.intercept_, 10.0)

    def test_closed_form(self):
        X = np.array([[1., 0.], [0., 1.], [1., 1.]]); y = np.array([1., 2., 4.])
        m = S.Ridge(alpha=2.0).fit(X, y)
        Xc, yc = X - X.mean(0), y - y.mean()
        np.testing.assert_allclose(m.coef_, np.linalg.solve(Xc.T @ Xc + 2 * np.eye(2), Xc.T @ yc))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.Ridge(alpha=-1).fit(np.ones((2, 1)), np.ones(2))
        with self.assertRaises(RuntimeError):
            S.Ridge().predict(np.ones((1, 1)))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_ridge(self):
        import numpy as np
        from sklearn.linear_model import Ridge as SkRidge
        rng = np.random.default_rng(0)
        X = rng.normal(size=(30, 4))
        y = X @ np.array([1.0, -2.0, 0.5, 0.0]) + 3 + rng.normal(0, 0.1, 30)
        for alpha in (0.1, 5.0):
            ours, sk = S.Ridge(alpha).fit(X, y), SkRidge(alpha=alpha).fit(X, y)
            np.testing.assert_allclose(ours.coef_, sk.coef_, atol=1e-8)
            self.assertAlmostEqual(ours.intercept_, sk.intercept_, places=8)


if __name__ == "__main__":
    unittest.main()
