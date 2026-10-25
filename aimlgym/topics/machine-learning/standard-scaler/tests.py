"""Tests for ML-08 Standard Scaler (fit on train only).

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

class TestScaler(unittest.TestCase):
    def test_fit_params(self):
        sc = S.StandardScaler().fit(np.array([[1., 10.], [3., 10.]]))
        np.testing.assert_allclose(sc.mean_, [2, 10])
        np.testing.assert_allclose(sc.scale_, [1, 1])

    def test_transform_test_point(self):
        sc = S.StandardScaler().fit(np.array([[1., 10.], [3., 10.]]))
        np.testing.assert_allclose(sc.transform([[5., 10.]]), [[3., 0.]])

    def test_fit_returns_self(self):
        sc = S.StandardScaler()
        self.assertIs(sc.fit(np.ones((2, 2))), sc)

    def test_not_fitted(self):
        with self.assertRaises(RuntimeError):
            S.StandardScaler().transform(np.ones((1, 2)))

    def test_wrong_columns(self):
        sc = S.StandardScaler().fit(np.ones((3, 2)))
        with self.assertRaises(ValueError):
            sc.transform(np.ones((3, 3)))

    def test_roundtrip(self):
        X = np.random.default_rng(0).normal(3, 2, size=(20, 4))
        sc = S.StandardScaler()
        np.testing.assert_allclose(sc.inverse_transform(sc.fit_transform(X)), X)

    def test_no_leakage(self):
        Xtr = np.array([[0.], [2.]])
        Xte = np.array([[100.]])
        sc = S.StandardScaler().fit(Xtr)
        sc.transform(Xte)
        np.testing.assert_allclose(sc.mean_, [1.0])


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_scaler(self):
        import numpy as np
        from sklearn.preprocessing import StandardScaler as SkScaler
        Xtr = np.array([[1.0, 5.0, 2.0], [2.0, 5.0, 4.0], [4.0, 5.0, 9.0]])
        Xte = np.array([[3.0, 5.0, 1.0]])
        ours, theirs = S.StandardScaler().fit(Xtr), SkScaler().fit(Xtr)
        np.testing.assert_allclose(ours.transform(Xte), theirs.transform(Xte))
        np.testing.assert_allclose(ours.scale_, theirs.scale_)


if __name__ == "__main__":
    unittest.main()
