r"""Reference solution for XA-06 Partial Dependence by Hand.

The helper builds the full ICE matrix (instances × grid values). Averaging over instances gives PD;
centring each ICE curve and measuring the spread across instances quantifies heterogeneity that
signals interactions.
"""
import numpy as np


def _ice_matrix(predict, X, feature, grid):
    X = np.asarray(X, dtype=float)
    grid = np.asarray(grid, dtype=float)
    if X.ndim != 2 or X.shape[0] == 0 or grid.size == 0:
        raise ValueError("X and grid must be non-empty")
    if not 0 <= feature < X.shape[1]:
        raise ValueError("feature index out of range")
    cols = []
    for g in grid:
        Xg = X.copy()
        Xg[:, feature] = g
        cols.append(np.asarray(predict(Xg), dtype=float))
    return np.column_stack(cols)


def partial_dependence(predict, X, feature, grid):
    return _ice_matrix(predict, X, feature, grid).mean(axis=0)


def ice_spread(predict, X, feature, grid):
    ice = _ice_matrix(predict, X, feature, grid)
    centred = ice - ice[:, [0]]
    return float(centred.std(axis=0).mean())
