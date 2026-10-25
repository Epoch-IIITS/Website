r"""Reference solution for MA-05 Vector Norm and Unit Vector.

Each norm is a direct translation of its formula. The empty-vector branch returns 0.0 for
valid `p` (avoiding `max()` of an empty sequence) and falls through to the final `raise` for an
invalid `p`. `unit` reuses the L2 norm and refuses to divide by zero.
"""
import math


def norm(v, p=2):
    if not v:
        if p in (1, 2, math.inf):
            return 0.0
    if p == 1:
        return float(sum(abs(x) for x in v))
    if p == 2:
        return math.sqrt(sum(x * x for x in v))
    if p == math.inf:
        return float(max(abs(x) for x in v))
    raise ValueError("p must be 1, 2 or inf")


def unit(v):
    n = norm(v)
    if n == 0:
        raise ValueError("cannot normalise the zero vector")
    return [x / n for x in v]
