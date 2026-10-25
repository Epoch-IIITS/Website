r"""Reference solution for FL-06 Local SGD on a Client.

`np.array(w)` copies the global weights so the caller's array is untouched. One generator produces a
fresh permutation per epoch; each minibatch takes one gradient step with its own batch-mean gradient.
"""
import numpy as np


def mse_grad(w, X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    return 2.0 / len(y) * X.T @ (X @ w - y)


def local_sgd(w, X, y, lr, epochs, batch_size, seed):
    if lr <= 0 or epochs < 1 or batch_size < 1:
        raise ValueError("invalid lr, epochs or batch_size")
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.array(w, dtype=float)
    rng = np.random.default_rng(seed)
    n = len(y)
    for _ in range(epochs):
        order = rng.permutation(n)
        for s in range(0, n, batch_size):
            b = order[s:s + batch_size]
            w = w - lr * mse_grad(w, X[b], y[b])
    return w
