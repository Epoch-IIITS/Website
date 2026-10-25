r"""Reference solution for XA-12 LIME-style Local Linear Explanation.

Masks map to concrete inputs by mixing the instance with the baseline. Samples closer to the
instance (fewer features removed) get larger kernel weights. Scaling rows by the square root of the
weights turns weighted least squares into ordinary least squares, whose coefficients are the local
explanation.
"""
import numpy as np


def sample_masks(n, d, rng):
    if n < 1 or d < 1:
        raise ValueError("n and d must be >= 1")
    rest = (rng.random((n - 1, d)) < 0.5).astype(int)
    return np.vstack([np.ones((1, d), dtype=int), rest])


def lime_explain(predict, x, baseline, masks, kernel_width=0.75):
    if kernel_width <= 0:
        raise ValueError("kernel_width must be positive")
    x = np.asarray(x, dtype=float)
    base = np.asarray(baseline, dtype=float)
    Z = np.asarray(masks, dtype=float)
    if Z.ndim != 2 or Z.shape[1] != x.shape[0] or base.shape != x.shape:
        raise ValueError("shape mismatch")
    Xz = Z * x + (1 - Z) * base
    y = np.asarray(predict(Xz), dtype=float)
    D = 1.0 - Z.mean(axis=1)
    w = np.exp(-(D ** 2) / kernel_width ** 2)
    sw = np.sqrt(w)
    A = np.column_stack([np.ones(len(Z)), Z]) * sw[:, None]
    beta, *_ = np.linalg.lstsq(A, y * sw, rcond=None)
    return {"intercept": float(beta[0]), "coef": beta[1:], "weights": w}
