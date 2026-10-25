"""Tests for ML-17 k-Fold Cross-Validation by Hand.

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

def fit_mean(X, y):
    return float(np.mean(y))

def neg_mse(m, X, y):
    return -float(np.mean((y - m) ** 2))

class TestCV(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual([t.tolist() for _, t in S.kfold_indices(7, 3)], [[0, 1, 2], [3, 4], [5, 6]])

    def test_partition(self):
        pairs = S.kfold_indices(23, 5, seed=1)
        tests = np.concatenate([t for _, t in pairs])
        self.assertEqual(sorted(tests.tolist()), list(range(23)))
        for tr, te in pairs:
            self.assertEqual(len(set(tr) & set(te)), 0)
            self.assertEqual(len(tr) + len(te), 23)

    def test_seeded_recipe(self):
        perm = np.random.default_rng(4).permutation(10)
        np.testing.assert_array_equal(S.kfold_indices(10, 2, seed=4)[0][1], perm[:5])

    def test_bad_k(self):
        with self.assertRaises(ValueError):
            S.kfold_indices(3, 4)
        with self.assertRaises(ValueError):
            S.kfold_indices(3, 1)

    def test_cv_score_count(self):
        s = S.cross_val_score(fit_mean, neg_mse, np.zeros((10, 1)), np.arange(10.0), k=5)
        self.assertEqual(s.shape, (5,))

    def test_cv_values(self):
        y = np.array([1.0, 1.0, 3.0, 3.0])
        s = S.cross_val_score(fit_mean, neg_mse, np.zeros((4, 1)), y, k=2, seed=None)
        np.testing.assert_allclose(s, [-4.0, -4.0])

    def test_model_selection(self):
        rng = np.random.default_rng(0)
        X = rng.uniform(-1, 1, (60, 1)); y = 3 * X[:, 0] + rng.normal(0, 0.1, 60)
        fit_lin = lambda X, y: np.polyfit(X[:, 0], y, 1)
        sc_lin = lambda m, X, y: -float(np.mean((np.polyval(m, X[:, 0]) - y) ** 2))
        self.assertGreater(S.cross_val_score(fit_lin, sc_lin, X, y).mean(),
                           S.cross_val_score(fit_mean, neg_mse, X, y).mean())


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_folds_match_kfold(self):
        import numpy as np
        from sklearn.model_selection import KFold
        ours = S.kfold_indices(11, 3)
        theirs = list(KFold(n_splits=3).split(np.zeros(11)))
        for (tr, te), (str_, ste) in zip(ours, theirs):
            np.testing.assert_array_equal(np.sort(tr), str_)
            np.testing.assert_array_equal(te, ste)


if __name__ == "__main__":
    unittest.main()
