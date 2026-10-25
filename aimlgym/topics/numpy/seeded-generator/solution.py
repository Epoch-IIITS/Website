r"""Reference solution for NP-10 Seeded Random Generators.

Each function owns one seeded generator, so results depend only on the arguments. Draw order is
fixed (x then noise). The permutation guarantees train and test indices are disjoint and cover
0..n−1.
"""
import numpy as np


def make_regression(n, seed, noise=0.1):
    if n < 1 or noise < 0:
        raise ValueError("invalid n or noise")
    rng = np.random.default_rng(seed)
    x = rng.uniform(0, 1, n)
    eps = rng.normal(0, noise, n)
    return x, 2 * x + 1 + eps


def split_indices(n, test_frac, seed):
    if not 0 < test_frac < 1:
        raise ValueError("test_frac must be in (0, 1)")
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n)
    k = round(n * test_frac)
    return perm[k:], perm[:k]
