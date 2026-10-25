r"""Reference solution for XA-11 Exact Shapley Values.

The value function mixes the instance and the baseline according to the coalition. For each feature,
every coalition of the other features is enumerated and its weighted marginal contribution added.
A cache ensures each of the 2^d coalitions is evaluated only once.
"""
import math
from itertools import combinations

import numpy as np


def coalition_value(predict, x, baseline, subset):
    x = np.asarray(x, dtype=float)
    z = np.asarray(baseline, dtype=float).copy()
    idx = list(subset)
    z[idx] = x[idx]
    return float(np.asarray(predict(z[None, :]))[0])


def shapley_values(predict, x, baseline):
    x = np.asarray(x, dtype=float)
    baseline = np.asarray(baseline, dtype=float)
    if x.shape != baseline.shape:
        raise ValueError("x and baseline must have the same shape")
    d = x.shape[0]
    if d > 12:
        raise ValueError("exact Shapley values are limited to d <= 12")
    cache = {}

    def v(S):
        key = tuple(sorted(S))
        if key not in cache:
            cache[key] = coalition_value(predict, x, baseline, key)
        return cache[key]

    phi = np.zeros(d)
    for j in range(d):
        others = [i for i in range(d) if i != j]
        for size in range(d):
            w = math.factorial(size) * math.factorial(d - size - 1) / math.factorial(d)
            for S in combinations(others, size):
                phi[j] += w * (v(S + (j,)) - v(S))
    return phi
