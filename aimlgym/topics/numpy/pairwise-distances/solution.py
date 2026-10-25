r"""Reference solution for NP-11 Vectorized Pairwise Distances.

Expanding the squared distance turns the problem into two norm vectors and one matrix product,
combined by broadcasting into an m×n matrix. Clipping removes tiny negative rounding errors.
`argmin` along axis 1 picks the closest reference for each query.
"""
import numpy as np


def pairwise_sq_dists(A, B):
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.ndim != 2 or B.ndim != 2 or A.shape[1] != B.shape[1]:
        raise ValueError("A and B must be 2-D with the same number of columns")
    aa = (A ** 2).sum(axis=1)[:, None]
    bb = (B ** 2).sum(axis=1)[None, :]
    return np.maximum(aa + bb - 2 * A @ B.T, 0.0)


def nearest(A, B):
    return pairwise_sq_dists(A, B).argmin(axis=1)
