r"""Reference solution for ML-01 Features, Labels and Baseline Models.

Each baseline learns a single value in `fit` and repeats it in `predict`, using the row count of
`X` so the output has one prediction per example. `np.unique` returns sorted labels, so taking
the first maximum count resolves ties toward the smallest label. Missing attributes signal an
unfitted model.
"""
import numpy as np


class MeanRegressor:
    def fit(self, X, y):
        self.mean_ = float(np.mean(np.asarray(y, dtype=float)))
        return self

    def predict(self, X):
        if not hasattr(self, "mean_"):
            raise ValueError("call fit before predict")
        return np.full(len(X), self.mean_)


class MajorityClassifier:
    def fit(self, X, y):
        labels, counts = np.unique(np.asarray(y), return_counts=True)
        self.label_ = labels[np.argmax(counts)]
        return self

    def predict(self, X):
        if not hasattr(self, "label_"):
            raise ValueError("call fit before predict")
        return np.full(len(X), self.label_)


def _check(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    if len(y_true) != len(y_pred) or len(y_true) == 0:
        raise ValueError("inputs must be non-empty and the same length")
    return y_true, y_pred


def mse(y_true, y_pred):
    y_true, y_pred = _check(y_true, y_pred)
    return float(np.mean((y_true.astype(float) - y_pred.astype(float)) ** 2))


def accuracy(y_true, y_pred):
    y_true, y_pred = _check(y_true, y_pred)
    return float(np.mean(y_true == y_pred))
