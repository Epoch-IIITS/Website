r"""Reference solution for NP-12 Solve Linear Systems Safely.

`solve` validates shapes and refuses ill-conditioned systems before factorising. The residual is
a direct norm. `fit_line` builds the design matrix with an intercept column and lets `lstsq`
minimise the squared residual.
"""
import numpy as np


def solve(A, b, max_cond=1e12):
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1] or b.shape[0] != A.shape[0]:
        raise ValueError("A must be square and match b")
    c = np.linalg.cond(A)
    if not np.isfinite(c) or c > max_cond:
        raise ValueError(f"ill-conditioned system (cond={c:.3g})")
    return np.linalg.solve(A, b)


def residual_norm(A, x, b):
    return float(np.linalg.norm(np.asarray(A) @ np.asarray(x) - np.asarray(b)))


def fit_line(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("need at least two matching points")
    X = np.column_stack([np.ones(len(x)), x])
    w, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(w[0]), float(w[1])
