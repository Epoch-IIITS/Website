r"""Reference solution for ML-11 Logistic Regression from Scratch.

The sigmoid only ever exponentiates a non-positive number, so it cannot overflow. Clipping keeps
the logs finite. The log-loss gradient with respect to the linear score is p − y, so training is
the same loop as ML-10 with a different output function.
"""
import numpy as np


def sigmoid(z):
    z = np.asarray(z, dtype=float)
    e = np.exp(-np.abs(z))
    out = np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))
    return out if out.ndim else float(out)


def log_loss(y, p, eps=1e-12):
    y = np.asarray(y, dtype=float)
    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


class LogisticRegression:
    def __init__(self, lr=0.1, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.w_ = None
        self.b_ = None
        self.history_ = []

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if not np.isin(y, (0, 1)).all():
            raise ValueError("y must contain only 0 and 1")
        n, d = X.shape
        self.w_, self.b_, self.history_ = np.zeros(d), 0.0, []
        for _ in range(self.epochs):
            p = sigmoid(X @ self.w_ + self.b_)
            self.history_.append(log_loss(y, p))
            g = p - y
            self.w_ = self.w_ - self.lr * (X.T @ g) / n
            self.b_ = self.b_ - self.lr * float(g.mean())
        return self

    def predict_proba(self, X):
        return sigmoid(np.asarray(X, dtype=float) @ self.w_ + self.b_)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)
