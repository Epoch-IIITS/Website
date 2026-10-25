r"""Reference solution for ML-14 Polynomial Features and Validation Curves.

`validation_curve` refits the pipeline for every degree and fold; averaging across folds and
negating the scores gives mean squared errors. The minimum of the validation curve is the degree
that generalises best on this data.
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, validation_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def degree_curve(x, y, degrees, n_splits=5, seed=0):
    if not degrees or len(x) != len(y):
        raise ValueError("need degrees and matching x and y")
    X = np.asarray(x, dtype=float).reshape(-1, 1)
    model = make_pipeline(PolynomialFeatures(include_bias=False), LinearRegression())
    train, val = validation_curve(model, X, np.asarray(y, dtype=float),
                                  param_name="polynomialfeatures__degree", param_range=list(degrees),
                                  cv=KFold(n_splits, shuffle=True, random_state=seed),
                                  scoring="neg_mean_squared_error")
    train_mse = [float(v) for v in -train.mean(axis=1)]
    val_mse = [float(v) for v in -val.mean(axis=1)]
    best = min(range(len(degrees)), key=lambda i: (val_mse[i], degrees[i]))
    return {"train_mse": train_mse, "val_mse": val_mse, "best_degree": int(degrees[best])}
