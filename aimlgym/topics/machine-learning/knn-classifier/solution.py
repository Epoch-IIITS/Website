r"""Reference solution for ML-13 k-Nearest Neighbors Classifier by Hand.

All test–train distances are computed at once. For each test point a stable argsort orders
neighbours (ties by training index); the vote counts labels among the first k, and the first
label in neighbour order reaching the maximum count wins, which implements the nearest-member
tie-break.
"""
import numpy as np


def knn_predict(X_train, y_train, X_test, k=3):
    Xtr = np.asarray(X_train, dtype=float)
    ytr = np.asarray(y_train)
    Xte = np.asarray(X_test, dtype=float)
    if Xtr.ndim != 2 or Xte.ndim != 2 or Xtr.shape[1] != Xte.shape[1]:
        raise ValueError("feature dimensions must match")
    if not 1 <= k <= len(Xtr):
        raise ValueError("k must be between 1 and n_train")
    d = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    preds = []
    for row in d:
        labels = ytr[np.argsort(row, kind="stable")[:k]]
        counts = {}
        for lab in labels:
            counts[lab] = counts.get(lab, 0) + 1
        best = max(counts.values())
        preds.append(next(lab for lab in labels if counts[lab] == best))
    return np.array(preds)
