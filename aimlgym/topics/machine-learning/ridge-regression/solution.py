r"""Reference solution for ML-20 Ridge Regression (Closed Form).

Centring removes the intercept from the penalised problem; the α·I term makes the system
well-conditioned. The intercept is recovered from the means so that the fitted plane passes
through (X̄, ȳ).
"""
import numpy as np


class Ridge:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        if self.alpha < 0:
            raise ValueError("alpha must be >= 0")
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        xm, ym = X.mean(axis=0), y.mean()
        Xc, yc = X - xm, y - ym
        A = Xc.T @ Xc + self.alpha * np.eye(X.shape[1])
        self.coef_ = np.linalg.solve(A, Xc.T @ yc)
        self.intercept_ = float(ym - xm @ self.coef_)
        return self

    def predict(self, X):
        if self.coef_ is None:
            raise RuntimeError("model is not fitted")
        return np.asarray(X, dtype=float) @ self.coef_ + self.intercept_
