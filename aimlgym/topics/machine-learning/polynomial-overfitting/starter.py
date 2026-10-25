import numpy as np


def poly_features(x, degree):
    # TODO
    x = np.asarray(x, dtype=float)
    return x.reshape(-1, 1)


def fit_poly(x, y, degree):
    # TODO
    return np.zeros(degree + 1)


def predict_poly(coef, x):
    # TODO
    return np.zeros(len(x))


def errors_by_degree(x_tr, y_tr, x_te, y_te, degrees):
    # TODO
    return {}


def best_degree(errors):
    # TODO
    return min(errors)
