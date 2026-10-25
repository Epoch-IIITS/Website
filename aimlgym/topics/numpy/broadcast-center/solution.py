r"""Reference solution for NP-07 Centering Columns with Broadcasting.

Column statistics have shape (d,), which broadcasts across the n rows. Row weights need an
explicit column shape (n, 1). For constant columns the centred values are already zero, so
dividing by 1 instead of 0 yields zeros without NaN.
"""
import numpy as np


def center_columns(X):
    X = np.asarray(X, dtype=float)
    return X - X.mean(axis=0)


def scale_rows(X, w):
    X = np.asarray(X, dtype=float)
    w = np.asarray(w, dtype=float)
    if w.shape != (X.shape[0],):
        raise ValueError("w must have one weight per row")
    return X * w[:, None]


def standardize(X):
    Xc = center_columns(X)
    std = Xc.std(axis=0)
    std = np.where(std == 0, 1.0, std)
    return Xc / std
