r"""Reference solution for XA-14 Integrated Gradients.

All points along the straight path are built at once and their gradients computed in one batch; the
midpoint average approximates the path integral, and multiplying by the input–baseline difference
gives the attribution per feature.
"""
import numpy as np


def integrated_gradients(grad_fn, x, baseline, steps=50):
    x = np.asarray(x, dtype=float)
    base = np.asarray(baseline, dtype=float)
    if steps < 1 or x.shape != base.shape:
        raise ValueError("steps must be >= 1 and shapes must match")
    alphas = (np.arange(steps) + 0.5) / steps
    points = base + alphas[:, None] * (x - base)
    grads = np.asarray(grad_fn(points), dtype=float)
    return (x - base) * grads.mean(axis=0), alphas
