r"""Reference solution for XA-10 Global Surrogate and Fidelity.

The surrogate is fitted to the black box's own outputs, so it learns to imitate the model rather than
the data. Fidelity is R² between the two models' predictions, with an explicit rule for a constant
black box.
"""
import numpy as np


def fit_linear_surrogate(predict, X):
    X = np.asarray(X, dtype=float)
    yhat = np.asarray(predict(X), dtype=float)
    A = np.column_stack([np.ones(len(X)), X])
    w, *_ = np.linalg.lstsq(A, yhat, rcond=None)
    return float(w[0]), w[1:]


def fidelity_r2(predict, surrogate, X):
    X = np.asarray(X, dtype=float)
    yhat = np.asarray(predict(X), dtype=float)
    s = np.asarray(surrogate(X), dtype=float)
    ss_res = float(((yhat - s) ** 2).sum())
    ss_tot = float(((yhat - yhat.mean()) ** 2).sum())
    if ss_tot == 0:
        return 1.0 if ss_res <= 1e-12 else 0.0
    return 1.0 - ss_res / ss_tot
