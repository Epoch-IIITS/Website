r"""Reference solution for ST-05 Standardize to z-scores.

The mean and standard deviation are computed once and every value is shifted and scaled. A zero
spread makes standardization meaningless, so it is rejected. `outliers` reuses `z_scores` and
returns indices so the caller can locate the original records.
"""
import math


def z_scores(data, sample=False):
    n = len(data)
    if n == 0 or (sample and n < 2):
        raise ValueError("not enough data")
    m = sum(data) / n
    var = sum((x - m) ** 2 for x in data) / (n - 1 if sample else n)
    sd = math.sqrt(var)
    if sd == 0:
        raise ValueError("standard deviation is zero")
    return [(x - m) / sd for x in data]


def outliers(data, threshold=3.0):
    return [i for i, z in enumerate(z_scores(data)) if abs(z) > threshold]
