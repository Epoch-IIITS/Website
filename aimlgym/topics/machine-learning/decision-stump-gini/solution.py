r"""Reference solution for ML-21 Decision Stump with Gini Impurity.

Gini comes from class proportions. The search scans features in order and thresholds in
increasing order, keeping a candidate only if it is strictly better, which implements the
tie-breaking rule. `np.unique` with `argmax` picks the smallest label among majority ties.
"""
import numpy as np


def gini(y):
    y = np.asarray(y)
    if y.size == 0:
        return 0.0
    _, counts = np.unique(y, return_counts=True)
    p = counts / y.size
    return float(1.0 - (p ** 2).sum())


def _majority(y):
    vals, counts = np.unique(y, return_counts=True)
    return int(vals[np.argmax(counts)])


def best_split(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    n = len(y)
    best = None
    for j in range(X.shape[1]):
        u = np.unique(X[:, j])
        for t in (u[:-1] + u[1:]) / 2:
            left = X[:, j] <= t
            yl, yr = y[left], y[~left]
            g = (len(yl) * gini(yl) + len(yr) * gini(yr)) / n
            if best is None or g < best["impurity"] - 1e-15:
                best = {"feature": j, "threshold": float(t), "impurity": float(g),
                        "left_class": _majority(yl), "right_class": _majority(yr)}
    if best is None:
        raise ValueError("no feature can be split")
    return best
