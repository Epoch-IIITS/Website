r"""Reference solution for ST-04 Histogram with Equal-Width Bins.

Defaults and degenerate ranges are resolved before computing the width. Edges are computed by
multiplication (and the last edge pinned to hi to avoid rounding drift). Each in-range value's
bin index is the floor of its scaled position; the value equal to hi would land in a non-existent
bin `bins`, so it is clamped into the last, closed bin.
"""
def histogram(data, bins, lo=None, hi=None):
    if bins < 1:
        raise ValueError("bins must be >= 1")
    if lo is None or hi is None:
        if not data:
            raise ValueError("empty data needs explicit lo and hi")
        lo = min(data) if lo is None else lo
        hi = max(data) if hi is None else hi
    if lo > hi:
        raise ValueError("lo must be <= hi")
    if lo == hi:
        lo, hi = lo - 0.5, hi + 0.5
    lo, hi = float(lo), float(hi)
    w = (hi - lo) / bins
    edges = [lo + j * w for j in range(bins + 1)]
    edges[-1] = hi
    counts = [0] * bins
    for x in data:
        if x < lo or x > hi:
            continue
        j = int((x - lo) / w)
        if j >= bins:
            j = bins - 1
        counts[j] += 1
    return edges, counts
