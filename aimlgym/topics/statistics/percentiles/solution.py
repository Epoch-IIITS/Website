r"""Reference solution for ST-03 Percentiles by Linear Interpolation.

The fractional rank r locates the percentile between two neighbouring sorted values, and linear
interpolation blends them. The IQR and Tukey fences are built from the 25th and 75th percentiles.
"""
import math


def percentile(data, q):
    if not data:
        raise ValueError("empty data")
    if not 0 <= q <= 100:
        raise ValueError("q must be in [0, 100]")
    s = sorted(data)
    r = q / 100 * (len(s) - 1)
    i = math.floor(r)
    f = r - i
    if i + 1 < len(s):
        return s[i] + f * (s[i + 1] - s[i])
    return float(s[i])


def iqr(data):
    return percentile(data, 75) - percentile(data, 25)


def tukey_outliers(data, k=1.5):
    q1, q3 = percentile(data, 25), percentile(data, 75)
    spread = q3 - q1
    lo, hi = q1 - k * spread, q3 + k * spread
    return sorted(x for x in data if x < lo or x > hi)
