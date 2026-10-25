r"""Reference solution for ML-10 Linear Regression by Gradient Descent.

The residual vector gives both the loss and the gradients in two matrix expressions. The training
loop records the current loss and takes a step against the gradient. For a convex loss with a
suitable learning rate, the parameters converge to the least-squares solution.
"""
import numpy as np


def mse_grad(X, y, w, b):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float)
    if X.ndim != 2 or X.shape[0] != y.shape[0] or X.shape[1] != w.shape[0]:
        raise ValueError("shape mismatch")
    n = X.shape[0]
    r = X @ w + b - y
    return float(np.mean(r ** 2)), 2.0 / n * (X.T @ r), float(2.0 / n * r.sum())


def fit_gd(X, y, lr=0.1, epochs=1000):
    if lr <= 0 or epochs < 1:
        raise ValueError("lr must be > 0 and epochs >= 1")
    X = np.asarray(X, dtype=float)
    w = np.zeros(X.shape[1])
    b = 0.0
    history = []
    for _ in range(epochs):
        loss, gw, gb = mse_grad(X, y, w, b)
        history.append(loss)
        w = w - lr * gw
        b = b - lr * gb
    return w, b, history
