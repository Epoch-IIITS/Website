r"""Reference solution for XA-01 Linear Model Contributions.

Each feature's contribution is its weight times its deviation from the baseline; by linearity these
sum exactly to the change in prediction relative to the baseline input.
"""
import numpy as np


def contributions(w, b, x, baseline):
    w, x, base = (np.asarray(a, dtype=float) for a in (w, x, baseline))
    if not (w.shape == x.shape == base.shape):
        raise ValueError("w, x and baseline must have the same shape")
    return {"phi": w * (x - base), "prediction": float(w @ x + b),
            "baseline_prediction": float(w @ base + b)}
