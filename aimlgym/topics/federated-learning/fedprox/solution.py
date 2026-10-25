r"""Reference solution for FL-14 FedProx Local Objective.

The proximal gradient adds a linear pull towards the fixed global anchor. Running gradient descent on
the augmented objective yields a local model that balances fitting local data against staying close
to the global model, controlled by μ.
"""
import numpy as np


def prox_grad(w, w_global, X, y, mu):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float)
    return 2.0 / len(y) * X.T @ (X @ w - y) + mu * (w - np.asarray(w_global, dtype=float))


def local_prox_gd(w_global, X, y, mu, lr, steps):
    if mu < 0 or lr <= 0 or steps < 1:
        raise ValueError("invalid mu, lr or steps")
    anchor = np.array(w_global, dtype=float)
    w = anchor.copy()
    for _ in range(steps):
        w = w - lr * prox_grad(w, anchor, X, y, mu)
    return w
