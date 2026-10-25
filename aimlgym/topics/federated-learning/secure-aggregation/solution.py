r"""Reference solution for FL-12 Secure Aggregation with Pairwise Masks.

Each pair's mask enters one client's message with + and the other's with −, so they cancel in the
sum. When a client drops, its partners' masks with it are left uncancelled; regenerating exactly
those pairwise masks and removing them recovers the survivors' true sum.
"""
import numpy as np


def pair_mask(i, j, dim, base_seed):
    if i >= j:
        raise ValueError("pair_mask requires i < j")
    return np.random.default_rng([base_seed, i, j]).normal(size=dim)


def mask_update(i, update, n_clients, base_seed):
    y = np.array(update, dtype=float)
    dim = y.shape[0]
    for j in range(n_clients):
        if j > i:
            y = y + pair_mask(i, j, dim, base_seed)
        elif j < i:
            y = y - pair_mask(j, i, dim, base_seed)
    return y


def aggregate(masked, n_clients, dim, base_seed, dropped=()):
    total = np.zeros(dim)
    for v in masked.values():
        total = total + np.asarray(v, dtype=float)
    for d in dropped:
        for s in masked:
            if s < d:
                total = total - pair_mask(s, d, dim, base_seed)
            elif s > d:
                total = total + pair_mask(d, s, dim, base_seed)
    return total
