r"""Reference solution for ML-15 Polynomial Features and Overfitting by Hand.

Polynomial regression is linear regression on engineered features, so the same least-squares
solver fits every degree. Evaluating each fitted model on both the training and the held-out
points exposes the familiar pattern, and selection uses only the held-out error with a
deterministic tie-break.
"""
import numpy as np


def poly_features(x, degree):
    x = np.asarray(x, dtype=float)
    return np.column_stack([x ** k for k in range(degree + 1)])


def fit_poly(x, y, degree):
    coef, *_ = np.linalg.lstsq(poly_features(x, degree), np.asarray(y, dtype=float), rcond=None)
    return coef


def predict_poly(coef, x):
    return poly_features(x, len(coef) - 1) @ coef


def _mse(y, yhat):
    return float(np.mean((np.asarray(y, dtype=float) - yhat) ** 2))


def errors_by_degree(x_tr, y_tr, x_te, y_te, degrees):
    out = {}
    for d in degrees:
        coef = fit_poly(x_tr, y_tr, d)
        out[d] = (_mse(y_tr, predict_poly(coef, x_tr)), _mse(y_te, predict_poly(coef, x_te)))
    return out


def best_degree(errors):
    return min(errors, key=lambda d: (errors[d][1], d))
