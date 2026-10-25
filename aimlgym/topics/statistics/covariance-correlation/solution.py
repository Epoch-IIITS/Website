r"""Reference solution for ST-11 Covariance and Pearson Correlation.

A shared helper computes the centred cross- and self-sums once. Covariance divides the cross-sum
by n or n−1; Pearson's r normalises it by the geometric mean of the self-sums, so the denominator
choice cancels. Constant variables make the denominator zero and are rejected.
"""
import math


def _centered_sums(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n == 0:
        raise ValueError("empty input")
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return n, sxy, sxx, syy


def covariance(x, y, sample=True):
    n, sxy, _, _ = _centered_sums(x, y)
    if sample and n < 2:
        raise ValueError("need at least two points")
    return sxy / (n - 1 if sample else n)


def pearson(x, y):
    n, sxy, sxx, syy = _centered_sums(x, y)
    if n < 2:
        raise ValueError("need at least two points")
    if sxx == 0 or syy == 0:
        raise ValueError("correlation undefined for a constant variable")
    return sxy / math.sqrt(sxx * syy)
