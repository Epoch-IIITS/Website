r"""Reference solution for ML-08 Standard Scaler (fit on train only).

`fit` learns per-column statistics only from the data it is given and returns `self` for
chaining. `transform` reuses the stored statistics, so test data is scaled with training
parameters. A shared `_check` enforces fitting and column consistency.
"""
import numpy as np


class StandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[0] == 0:
            raise ValueError("X must be a non-empty 2-D array")
        self.mean_ = X.mean(axis=0)
        std = X.std(axis=0)
        self.scale_ = np.where(std == 0, 1.0, std)
        return self

    def _check(self, X):
        if self.mean_ is None:
            raise RuntimeError("scaler is not fitted")
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[1] != self.mean_.shape[0]:
            raise ValueError("wrong number of columns")
        return X

    def transform(self, X):
        X = self._check(X)
        return (X - self.mean_) / self.scale_

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        Z = self._check(Z)
        return Z * self.scale_ + self.mean_
