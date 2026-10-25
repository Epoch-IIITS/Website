r"""Reference solution for ST-20 Permutation Test for a Mean Difference by Hand.

The Fisher–Yates loop picks each position's element uniformly from the not-yet-fixed prefix,
giving every permutation equal probability. Each permutation reassigns labels at random; the
fraction of shuffles at least as extreme as the observed difference (plus the observed
arrangement itself) is the p-value.
"""
import random


def fisher_yates(items, rng):
    a = list(items)
    for i in range(len(a) - 1, 0, -1):
        j = int(rng.random() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


def permutation_test(x, y, n_perm=5000, seed=0):
    if not x or not y:
        raise ValueError("both groups must be non-empty")
    if n_perm < 1:
        raise ValueError("n_perm must be >= 1")
    nx = len(x)
    d_obs = sum(x) / nx - sum(y) / len(y)
    pool = list(x) + list(y)
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        p = fisher_yates(pool, rng)
        d = sum(p[:nx]) / nx - sum(p[nx:]) / (len(p) - nx)
        if abs(d) >= abs(d_obs) - 1e-12:
            hits += 1
    return {"observed": d_obs, "p_value": (hits + 1) / (n_perm + 1)}
