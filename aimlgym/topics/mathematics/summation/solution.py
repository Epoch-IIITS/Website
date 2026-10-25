r"""Reference solution for MA-01 Summation and Product Notation.

Σ and Π become loops over `range(start, stop + 1)` starting from their identity elements 0 and
1, which also gives the correct empty results. The mean reuses `summation` over list indices.
The closed form uses integer arithmetic on the full product before dividing, and `math.fsum`
compensates for rounding errors that a plain loop accumulates.
"""
import math


def summation(f, start, stop):
    total = 0
    for i in range(start, stop + 1):
        total += f(i)
    return total


def product(f, start, stop):
    result = 1
    for i in range(start, stop + 1):
        result *= f(i)
    return result


def mean(xs):
    if not xs:
        raise ValueError("mean of empty data")
    return summation(lambda i: xs[i], 0, len(xs) - 1) / len(xs)


def sum_of_squares(n):
    return n * (n + 1) * (2 * n + 1) // 6


def accurate_sum(xs):
    return math.fsum(xs)
