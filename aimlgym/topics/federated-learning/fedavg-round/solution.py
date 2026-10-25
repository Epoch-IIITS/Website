r"""Reference solution for FL-07 One FedAvg Round.

Every client starts from the same broadcast weights and trains with its own seed. The server
combines the returned models by data-size-weighted averaging. With one full-batch epoch, the weighted
average of one-step updates equals a single gradient step on the pooled data.
"""
import numpy as np


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
            w = w - lr * 2.0 / len(b) * X[b].T @ (X[b] @ w - y[b])
    return w


def fedavg_round(global_w, clients, lr, epochs, batch_size, seed):
    if not clients:
        raise ValueError("need at least one client")
    locals_, sizes = [], []
    for k, (X, y) in enumerate(clients):
        bs = len(y) if batch_size is None else batch_size
        locals_.append(local_sgd(global_w, X, y, lr, epochs, bs, seed + k))
        sizes.append(len(y))
    total = float(sum(sizes))
    new_global = sum((n / total) * w for n, w in zip(sizes, locals_))
    return new_global, locals_
