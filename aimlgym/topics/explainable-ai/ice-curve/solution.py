r"""Reference solution for XA-04 Individual Conditional Expectation.

Tiling creates independent copies of the instance, one per grid value, so the original stays intact.
Overwriting a single column and predicting the whole matrix gives the ICE curve in one model call.
"""
import numpy as np


def ice_curve(predict, x, feature, grid):
    x = np.asarray(x, dtype=float)
    grid = np.asarray(grid, dtype=float)
    if grid.size == 0:
        raise ValueError("grid must be non-empty")
    if not 0 <= feature < x.shape[0]:
        raise ValueError("feature index out of range")
    X = np.tile(x, (grid.size, 1))
    X[:, feature] = grid
    return np.asarray(predict(X), dtype=float)
