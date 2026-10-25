r"""Reference solution for XA-05 Partial Dependence with sklearn.inspection.

`partial_dependence` builds the grid from the feature's central percentiles, predicts with the feature
replaced by each grid value, and either averages over rows (partial dependence) or keeps every row's
curve (ICE). The function returns the grid and the requested curves as plain lists.
"""
import numpy as np
from sklearn.inspection import partial_dependence


def pd_curve(model, X, feature, grid_resolution=20, kind="average"):
    X = np.asarray(X)
    if kind not in ("average", "individual"):
        raise ValueError("kind must be 'average' or 'individual'")
    if not 0 <= feature < X.shape[1]:
        raise ValueError("feature index out of range")
    result = partial_dependence(model, X, features=[feature], grid_resolution=grid_resolution, kind=kind)
    return {"grid": [float(v) for v in result["grid_values"][0]], "values": result[kind][0].tolist()}
