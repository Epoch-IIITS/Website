r"""Reference solution for FL-01 IID Client Partitioning.

One seeded permutation randomises assignment; `array_split` yields disjoint, covering shards whose
sizes differ by at most one. Sorting each shard only makes outputs easier to read.
"""
import numpy as np


def iid_partition(n, n_clients, seed):
    if not 1 <= n_clients <= n:
        raise ValueError("need 1 <= n_clients <= n")
    perm = np.random.default_rng(seed).permutation(n)
    return [np.sort(p) for p in np.array_split(perm, n_clients)]


def client_sizes(parts):
    return [int(len(p)) for p in parts]
