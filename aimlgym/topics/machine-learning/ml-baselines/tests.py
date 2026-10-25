"""Tests for ML-01 Features, Labels and Baseline Models.

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

X_TRAIN = np.zeros((3, 2))
X_TEST = np.zeros((2, 2))


class TestBaselines(unittest.TestCase):
    def test_mean_regressor(self):
        m = S.MeanRegressor().fit(X_TRAIN, [3, 5, 10])
        self.assertEqual(m.mean_, 6.0)
        np.testing.assert_array_equal(m.predict(X_TEST), [6.0, 6.0])

    def test_fit_returns_self(self):
        m = S.MeanRegressor()
        self.assertIs(m.fit(X_TRAIN, [1, 2, 3]), m)
        c = S.MajorityClassifier()
        self.assertIs(c.fit(X_TRAIN, ["a", "b", "b"]), c)

    def test_predict_before_fit(self):
        for model in (S.MeanRegressor(), S.MajorityClassifier()):
            with self.assertRaises(ValueError):
                model.predict(X_TEST)

    def test_majority(self):
        c = S.MajorityClassifier().fit(X_TRAIN, ["a", "b", "b"])
        self.assertEqual(c.predict(X_TEST).tolist(), ["b", "b"])

    def test_majority_tie_smallest(self):
        c = S.MajorityClassifier().fit(np.zeros((4, 1)), [2, 1, 2, 1])
        self.assertEqual(c.label_, 1)

    def test_metrics(self):
        self.assertEqual(S.mse([4, 8], [6, 6]), 4.0)
        self.assertEqual(S.accuracy(["a", "b", "b", "c"], ["a", "b", "a", "a"]), 0.5)
        with self.assertRaises(ValueError):
            S.mse([1, 2], [1])
        with self.assertRaises(ValueError):
            S.accuracy([], [])

    def test_imbalanced_baseline_accuracy(self):
        y = np.array([0] * 95 + [1] * 5)
        c = S.MajorityClassifier().fit(np.zeros((100, 3)), y)
        self.assertEqual(S.accuracy(y, c.predict(np.zeros((100, 3)))), 0.95)


try:
    from sklearn.dummy import DummyClassifier, DummyRegressor
    from sklearn.metrics import accuracy_score, mean_squared_error
except ImportError:
    DummyRegressor = None


@unittest.skipIf(DummyRegressor is None, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_dummy_regressor(self):
        y = [1.5, 2.0, 7.25, 4.0]
        ours = S.MeanRegressor().fit(np.zeros((4, 1)), y).predict(np.zeros((3, 1)))
        theirs = DummyRegressor(strategy="mean").fit(np.zeros((4, 1)), y).predict(np.zeros((3, 1)))
        np.testing.assert_allclose(ours, theirs)

    def test_dummy_classifier_and_metrics(self):
        y = [3, 1, 3, 1, 2]
        ours = S.MajorityClassifier().fit(np.zeros((5, 1)), y).predict(np.zeros((5, 1)))
        theirs = DummyClassifier(strategy="most_frequent").fit(np.zeros((5, 1)), y).predict(np.zeros((5, 1)))
        np.testing.assert_array_equal(ours, theirs)
        self.assertAlmostEqual(S.accuracy(y, ours), accuracy_score(y, theirs))
        self.assertAlmostEqual(S.mse([1, 2, 4], [2, 2, 2]), mean_squared_error([1, 2, 4], [2, 2, 2]))


if __name__ == "__main__":
    unittest.main()
