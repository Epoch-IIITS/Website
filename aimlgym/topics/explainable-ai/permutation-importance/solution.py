r"""Reference solution for XA-08 Permutation Feature Importance by Hand.

The baseline score is computed once. Each feature is permuted on a fresh copy of X, which breaks
its link with y while keeping its marginal distribution; the average drop in score across repeats is
the importance and the spread shows its uncertainty.
"""
import numpy as np


def permutation_importance(predict, X, y, score, n_repeats=5, seed=0):
    if n_repeats < 1:
        raise ValueError("n_repeats must be >= 1")
    X = np.asarray(X, dtype=float)
    n, d = X.shape
    base = float(score(y, predict(X)))
    rng = np.random.default_rng(seed)
    drops = np.zeros((d, n_repeats))
    for j in range(d):
        for r in range(n_repeats):
            Xp = X.copy()
            Xp[:, j] = X[rng.permutation(n), j]
            drops[j, r] = base - float(score(y, predict(Xp)))
    return {"baseline": base, "mean": drops.mean(axis=1), "std": drops.std(axis=1)}
