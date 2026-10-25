r"""Reference solution for ST-13 Bootstrap Confidence Interval.

Each bootstrap replicate resamples n values with replacement using the documented index recipe
and records the statistic. Sorting the replicates and reading off the α/2 and 1−α/2 percentiles
gives the percentile interval.
"""
import math
import random


def _percentile(s_sorted, q):
    r = q / 100 * (len(s_sorted) - 1)
    i = math.floor(r)
    f = r - i
    if i + 1 < len(s_sorted):
        return s_sorted[i] + f * (s_sorted[i + 1] - s_sorted[i])
    return float(s_sorted[i])


def bootstrap_ci(data, n_boot=2000, alpha=0.05, seed=0, stat=None):
    if not data:
        raise ValueError("empty data")
    if n_boot < 1:
        raise ValueError("n_boot must be >= 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    if stat is None:
        stat = lambda xs: sum(xs) / len(xs)
    rng = random.Random(seed)
    n = len(data)
    boots = []
    for _ in range(n_boot):
        sample = [data[int(rng.random() * n)] for _ in range(n)]
        boots.append(stat(sample))
    boots.sort()
    return float(_percentile(boots, 100 * alpha / 2)), float(_percentile(boots, 100 * (1 - alpha / 2)))
