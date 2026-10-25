r"""Reference solution for ML-26 k-Means Clustering by Hand.

Each iteration performs one assignment step and one update step. Empty clusters keep their
previous centre, avoiding NaN. Convergence is detected by the largest squared centroid movement.
A final assignment makes labels and inertia consistent with the returned centroids.
"""
import numpy as np


def _assign(X, C):
    d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    labels = d.argmin(axis=1)
    return labels, float(d[np.arange(len(X)), labels].sum())


def kmeans(X, init_centroids, max_iter=100, tol=1e-9):
    X = np.asarray(X, dtype=float)
    C = np.array(init_centroids, dtype=float)
    if X.ndim != 2 or C.ndim != 2 or X.shape[1] != C.shape[1]:
        raise ValueError("dimension mismatch")
    if C.shape[0] > X.shape[0]:
        raise ValueError("k cannot exceed n")
    n_iter = 0
    for _ in range(max_iter):
        labels, _ = _assign(X, C)
        newC = C.copy()
        for j in range(C.shape[0]):
            members = X[labels == j]
            if len(members):
                newC[j] = members.mean(axis=0)
        shift = float(((newC - C) ** 2).sum(axis=1).max())
        C = newC
        n_iter += 1
        if shift <= tol:
            break
    labels, inertia = _assign(X, C)
    return {"centroids": C, "labels": labels, "inertia": inertia, "n_iter": n_iter}
