r"""Reference solution for ML-17 k-Fold Cross-Validation by Hand.

`array_split` produces k nearly equal folds; each fold serves once as the test set while the
others are concatenated for training. `cross_val_score` is model-agnostic: it only needs a fit
function and a score function, so any model in this topic can be evaluated.
"""
import numpy as np


def kfold_indices(n, k, seed=None):
    if not 2 <= k <= n:
        raise ValueError("k must satisfy 2 <= k <= n")
    order = np.arange(n) if seed is None else np.random.default_rng(seed).permutation(n)
    folds = np.array_split(order, k)
    pairs = []
    for i in range(k):
        train = np.concatenate([f for j, f in enumerate(folds) if j != i])
        pairs.append((train, folds[i]))
    return pairs


def cross_val_score(fit, score, X, y, k=5, seed=0):
    X = np.asarray(X)
    y = np.asarray(y)
    scores = []
    for tr, te in kfold_indices(len(X), k, seed):
        model = fit(X[tr], y[tr])
        scores.append(float(score(model, X[te], y[te])))
    return np.array(scores)
