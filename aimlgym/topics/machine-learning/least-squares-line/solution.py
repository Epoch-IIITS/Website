r"""Reference solution for ML-09 Least-Squares Line.

The slope is the centred cross-product over the centred sum of squares of x; the intercept makes
the line pass through the means. Prediction is a vectorised affine map; `score` computes R² from
residuals.
"""
import numpy as np


class SimpleLinearRegression:
    def __init__(self):
        self.intercept_ = None
        self.slope_ = None

    def fit(self, x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        if x.shape != y.shape or x.size < 2:
            raise ValueError("need at least two matching points")
        dx, dy = x - x.mean(), y - y.mean()
        sxx = float((dx ** 2).sum())
        if sxx == 0:
            raise ValueError("x is constant; slope undefined")
        self.slope_ = float((dx * dy).sum() / sxx)
        self.intercept_ = float(y.mean() - self.slope_ * x.mean())
        return self

    def predict(self, x):
        if self.slope_ is None:
            raise RuntimeError("model is not fitted")
        return self.intercept_ + self.slope_ * np.asarray(x, dtype=float)

    def score(self, x, y):
        y = np.asarray(y, dtype=float)
        res = ((y - self.predict(x)) ** 2).sum()
        tot = ((y - y.mean()) ** 2).sum()
        return float(1 - res / tot)
