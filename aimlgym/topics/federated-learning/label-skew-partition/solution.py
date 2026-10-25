r"""Reference solution for FL-04 Label-Skewed (non-IID) Partition.

Sorting by label groups each class together, so contiguous shards contain one (or two) classes.
Randomly dealing shards to clients produces pathological label skew; `bincount` per client reveals
the resulting label distribution.
"""
import numpy as np


def shard_partition(labels, n_clients, shards_per_client, seed):
    labels = np.asarray(labels)
    n_shards = n_clients * shards_per_client
    if n_clients < 1 or shards_per_client < 1 or len(labels) < n_shards:
        raise ValueError("not enough examples for the requested shards")
    order = np.argsort(labels, kind="stable")
    shards = np.array_split(order, n_shards)
    ids = np.random.default_rng(seed).permutation(n_shards)
    s = shards_per_client
    return [np.sort(np.concatenate([shards[i] for i in ids[k * s:(k + 1) * s]])) for k in range(n_clients)]


def label_counts(labels, parts, n_classes):
    labels = np.asarray(labels)
    return np.array([np.bincount(labels[p], minlength=n_classes) for p in parts])
