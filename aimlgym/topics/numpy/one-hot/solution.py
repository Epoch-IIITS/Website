r"""Reference solution for NP-13 One-Hot Encoding.

After validating type and range, paired fancy indexing writes exactly one 1 per row. Decoding
checks the matrix really is one-hot (only zeros/ones, one 1 per row) and returns the argmax.
"""
import numpy as np


def one_hot(labels, num_classes=None):
    labels = np.asarray(labels)
    if labels.size == 0:
        raise ValueError("labels must be non-empty")
    if not np.issubdtype(labels.dtype, np.integer):
        raise ValueError("labels must be integers")
    if labels.min() < 0:
        raise ValueError("labels must be non-negative")
    K = int(labels.max()) + 1 if num_classes is None else int(num_classes)
    if labels.max() >= K:
        raise ValueError("label out of range")
    Y = np.zeros((labels.size, K))
    Y[np.arange(labels.size), labels.ravel()] = 1.0
    return Y


def from_one_hot(Y):
    Y = np.asarray(Y)
    if Y.ndim != 2 or not np.isin(Y, (0, 1)).all() or not (Y.sum(axis=1) == 1).all():
        raise ValueError("not a valid one-hot matrix")
    return Y.argmax(axis=1)
