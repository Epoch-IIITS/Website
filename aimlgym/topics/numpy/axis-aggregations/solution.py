r"""Reference solution for NP-05 Aggregations Along Axes.

Each entry is one reduction along the appropriate axis. The global maximum's flat index is
converted to a 2-D position with `unravel_index`, and `keepdims=True` preserves a column shape
for later broadcasting.
"""
import numpy as np


def summarize(X):
    X = np.asarray(X)
    if X.ndim != 2 or X.size == 0:
        raise ValueError("X must be a non-empty 2-D array")
    r, c = np.unravel_index(X.argmax(), X.shape)
    return {
        "col_means": X.mean(axis=0),
        "row_sums": X.sum(axis=1),
        "row_argmax": X.argmax(axis=1),
        "max_pos": (int(r), int(c)),
        "row_means_keep": X.mean(axis=1, keepdims=True),
    }
