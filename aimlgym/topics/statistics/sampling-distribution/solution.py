r"""Reference solution for ST-12 Sampling Distributions and Standard Error.

A single seeded generator produces every draw, so the whole simulation is reproducible and
uses only `random()`, whose output Python guarantees across versions. The standard error uses the
unbiased $n-1$ variance, and the interval combines it with the exact 97.5% normal quantile.
"""
import math
import random
from statistics import NormalDist


def sample_means(population, n, reps, seed):
    rng = random.Random(seed)
    size = len(population)
    means = []
    for _ in range(reps):
        total = 0
        for _ in range(n):
            total += population[int(rng.random() * size)]
        means.append(total / n)
    return means


def standard_error(sample):
    n = len(sample)
    if n < 2:
        raise ValueError("need at least two values")
    m = sum(sample) / n
    var = sum((x - m) ** 2 for x in sample) / (n - 1)
    return math.sqrt(var) / math.sqrt(n)


def mean_ci95(sample):
    m = sum(sample) / len(sample)
    se = standard_error(sample)
    z = NormalDist().inv_cdf(0.975)
    return (m - z * se, m + z * se)
