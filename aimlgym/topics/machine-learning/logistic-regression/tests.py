"""Tests for ML-11 Logistic Regression from Scratch.

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


import warnings
import numpy as np

class TestLogReg(unittest.TestCase):
    def test_sigmoid_extremes(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            np.testing.assert_allclose(S.sigmoid(np.array([-1000., 0., 1000.])), [0, 0.5, 1], atol=1e-300)

    def test_sigmoid_scalar(self):
        self.assertAlmostEqual(S.sigmoid(1.0), 1 / (1 + np.exp(-1)))

    def test_sigmoid_symmetry(self):
        z = np.linspace(-20, 20, 41)
        np.testing.assert_allclose(S.sigmoid(z) + S.sigmoid(-z), 1.0, atol=1e-12)

    def test_log_loss(self):
        self.assertAlmostEqual(S.log_loss([1, 0], [0.9, 0.1]), -np.log(0.9))

    def test_log_loss_clipped(self):
        self.assertTrue(np.isfinite(S.log_loss([1], [0.0])))

    def test_fit_separable(self):
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(-2, 1, (50, 2)), rng.normal(2, 1, (50, 2))])
        y = np.array([0] * 50 + [1] * 50)
        m = S.LogisticRegression(lr=0.5, epochs=500).fit(X, y)
        self.assertGreaterEqual((m.predict(X) == y).mean(), 0.97)
        self.assertLess(m.history_[-1], m.history_[0])

    def test_first_step(self):
        X = np.array([[1.0], [-1.0]]); y = np.array([1, 0])
        m = S.LogisticRegression(lr=1.0, epochs=1).fit(X, y)
        np.testing.assert_allclose(m.w_, [0.5])
        self.assertAlmostEqual(m.b_, 0.0)
        self.assertAlmostEqual(m.history_[0], np.log(2))

    def test_bad_labels(self):
        with self.assertRaises(ValueError):
            S.LogisticRegression().fit(np.ones((2, 1)), np.array([0, 2]))


try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False


@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_close_to_sklearn(self):
        import numpy as np
        from sklearn.linear_model import LogisticRegression as SkLR
        rng = np.random.default_rng(0)
        X = rng.normal(size=(200, 2))
        p = 1 / (1 + np.exp(-(X @ np.array([1.5, -2.0]) + 0.3)))
        y = (rng.random(200) < p).astype(int)
        ours = S.LogisticRegression(lr=0.5, epochs=4000).fit(X, y)
        sk = SkLR(C=1e10, max_iter=10000, tol=1e-10).fit(X, y)
        np.testing.assert_allclose(ours.predict_proba(X), sk.predict_proba(X)[:, 1], atol=2e-3)


if __name__ == "__main__":
    unittest.main()
