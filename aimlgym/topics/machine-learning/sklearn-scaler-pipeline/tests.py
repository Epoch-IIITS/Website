"""Tests for ML-07 Scaling inside a Pipeline.

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
from sklearn.linear_model import LogisticRegression


class TestScaledPipeline(unittest.TestCase):
    def test_example(self):
        pipe, pred = S.train_and_predict([[0, 100], [1, 110], [2, 300], [3, 310]], [0, 0, 1, 1], [[0.5, 105], [2.5, 305]])
        self.assertEqual(pred, [0, 1])
        self.assertEqual(pipe.named_steps["scale"].mean_.tolist(), [1.5, 205.0])

    def test_scaler_uses_training_statistics(self):
        rng = np.random.default_rng(0)
        X_train = rng.normal(5, 2, size=(30, 3)); y_train = (X_train[:, 0] > 5).astype(int)
        X_test = rng.normal(50, 9, size=(10, 3))
        pipe, _ = S.train_and_predict(X_train, y_train, X_test)
        scaler = pipe.named_steps["scale"]
        self.assertTrue(np.allclose(scaler.mean_, X_train.mean(axis=0)))
        self.assertTrue(np.allclose(scaler.scale_, X_train.std(axis=0)))

    def test_matches_manual_scaling(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(40, 2)) * [1, 100]; y = (X[:, 0] + X[:, 1] / 100 > 0).astype(int)
        pipe, pred = S.train_and_predict(X[:30], y[:30], X[30:])
        mu, sd = X[:30].mean(axis=0), X[:30].std(axis=0)
        manual = LogisticRegression().fit((X[:30] - mu) / sd, y[:30]).predict((X[30:] - mu) / sd)
        self.assertEqual(pred, manual.tolist())

    def test_step_names(self):
        pipe, _ = S.train_and_predict([[0], [1], [2], [3]], [0, 0, 1, 1], [[1.5]])
        self.assertEqual(list(pipe.named_steps), ["scale", "model"])

    def test_new_pipeline_each_call(self):
        a, _ = S.train_and_predict([[0], [1], [2], [3]], [0, 0, 1, 1], [[1]])
        b, _ = S.train_and_predict([[10], [11], [12], [13]], [0, 0, 1, 1], [[11]])
        self.assertIsNot(a, b)
        self.assertEqual(a.named_steps["scale"].mean_.tolist(), [1.5])

    def test_plain_ints(self):
        _, pred = S.train_and_predict([[0], [1], [2], [3]], [0, 0, 1, 1], [[0], [3]])
        self.assertTrue(all(type(v) is int for v in pred))


if __name__ == "__main__":
    unittest.main()
