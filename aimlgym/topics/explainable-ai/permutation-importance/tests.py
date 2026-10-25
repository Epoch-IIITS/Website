"""Tests for XA-08 Permutation Feature Importance by Hand.

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

def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()

rng0 = np.random.default_rng(42)
X = rng0.normal(size=(200, 2))
Y = 3 * X[:, 0] + rng0.normal(0, 0.1, 200)
MODEL = lambda X: 3 * X[:, 0]

class TestPermImp(unittest.TestCase):
    def test_relevant_vs_irrelevant(self):
        r = S.permutation_importance(MODEL, X, Y, r2, n_repeats=5, seed=0)
        self.assertGreater(r["mean"][0], 1.0)
        self.assertAlmostEqual(r["mean"][1], 0.0, places=12)

    def test_baseline(self):
        r = S.permutation_importance(MODEL, X, Y, r2)
        self.assertAlmostEqual(r["baseline"], r2(Y, MODEL(X)))

    def test_recipe(self):
        r = S.permutation_importance(MODEL, X, Y, r2, n_repeats=2, seed=3)
        rng = np.random.default_rng(3)
        base = r2(Y, MODEL(X)); drops = []
        for j in range(2):
            for _ in range(2):
                Xp = X.copy(); Xp[:, j] = X[rng.permutation(200), j]; drops.append(base - r2(Y, MODEL(Xp)))
        np.testing.assert_allclose(r["mean"], [np.mean(drops[:2]), np.mean(drops[2:])])

    def test_std_shape(self):
        r = S.permutation_importance(MODEL, X, Y, r2, n_repeats=4)
        self.assertEqual(r["std"].shape, (2,))
        self.assertEqual(r["std"][1], 0.0)

    def test_no_mutation(self):
        Xc = X.copy()
        S.permutation_importance(MODEL, Xc, Y, r2, n_repeats=1)
        np.testing.assert_array_equal(Xc, X)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.permutation_importance(MODEL, X, Y, r2, n_repeats=0)


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_same_ranking_as_sklearn(self):
        import numpy as np
        from sklearn.inspection import permutation_importance as sk_pi
        from sklearn.linear_model import LinearRegression
        rng = np.random.default_rng(0)
        X = rng.normal(size=(200, 3))
        y = 5 * X[:, 0] + 1 * X[:, 1] + rng.normal(0, 0.1, 200)
        model = LinearRegression().fit(X, y)
        r2 = lambda yt, yp: 1 - np.sum((yt - yp) ** 2) / np.sum((yt - yt.mean()) ** 2)
        ours = S.permutation_importance(model.predict, X, y, r2, n_repeats=10, seed=0)
        theirs = sk_pi(model, X, y, n_repeats=10, random_state=0)
        self.assertEqual(list(np.argsort(-ours["mean"])), list(np.argsort(-theirs.importances_mean)))
        np.testing.assert_allclose(ours["mean"], theirs.importances_mean, rtol=0.2, atol=0.02)


if __name__ == "__main__":
    unittest.main()
