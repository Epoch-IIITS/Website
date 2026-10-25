r"""Reference solution for ML-05 Seeded Train/Test Split.

A single permutation of row indices is used for both X and y, so pairs stay aligned. The
stratified variant applies the same idea per class, preserving class proportions. All randomness
flows through one seeded generator.
"""
import numpy as np


def train_test_split(X, y, test_size=0.25, seed=0, stratify=False):
    X = np.asarray(X)
    y = np.asarray(y)
    n = len(X)
    if len(y) != n:
        raise ValueError("X and y must have the same length")
    if n < 2:
        raise ValueError("need at least two samples")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be in (0, 1)")
    rng = np.random.default_rng(seed)
    if not stratify:
        perm = rng.permutation(n)
        n_test = min(max(round(n * test_size), 1), n - 1)
        te, tr = perm[:n_test], perm[n_test:]
    else:
        te_parts, tr_parts = [], []
        for c in np.unique(y):
            idx = rng.permutation(np.flatnonzero(y == c))
            k = round(len(idx) * test_size)
            te_parts.append(idx[:k])
            tr_parts.append(idx[k:])
        te, tr = np.concatenate(te_parts), np.concatenate(tr_parts)
    return X[tr], X[te], y[tr], y[te]
