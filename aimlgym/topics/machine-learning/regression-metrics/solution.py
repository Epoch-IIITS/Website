r"""Reference solution for ML-03 Regression Metrics.

All four metrics come from the residual vector. R² divides the residual sum of squares by the
total sum of squares around the mean, so it measures improvement over the constant-mean model.
"""
import numpy as np


def regression_report(y_true, y_pred):
    yt = np.asarray(y_true, dtype=float)
    yp = np.asarray(y_pred, dtype=float)
    if yt.size == 0 or yt.shape != yp.shape:
        raise ValueError("inputs must be non-empty and the same shape")
    e = yt - yp
    mse = float(np.mean(e ** 2))
    ss_tot = float(np.sum((yt - yt.mean()) ** 2))
    if ss_tot == 0:
        raise ValueError("R^2 undefined for constant y_true")
    return {"mse": mse, "rmse": float(np.sqrt(mse)), "mae": float(np.mean(np.abs(e))),
            "r2": 1.0 - float(np.sum(e ** 2)) / ss_tot}
