r"""Reference solution for FL-09 Clipping Client Updates.

Updates inside the ball are returned unchanged (as copies); larger ones are rescaled to lie exactly
on the sphere of radius max_norm, preserving direction. The zero vector falls in the first branch,
avoiding division by zero.
"""
import numpy as np


def clip_update(delta, max_norm):
    if max_norm <= 0:
        raise ValueError("max_norm must be positive")
    d = np.asarray(delta, dtype=float)
    n = float(np.linalg.norm(d))
    if n <= max_norm:
        return d.copy()
    return d * (max_norm / n)


def clip_all(deltas, max_norm):
    clipped = [clip_update(d, max_norm) for d in deltas]
    n_clipped = sum(1 for d in deltas if np.linalg.norm(d) > max_norm)
    return clipped, int(n_clipped)
