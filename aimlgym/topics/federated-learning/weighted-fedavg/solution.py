r"""Reference solution for FL-02 Weighted Federated Averaging.

After validating structure, each parameter tensor is averaged with weights n_k / N, so larger clients
count more and the weights sum to one.
"""
import numpy as np


def fedavg(client_params, sizes):
    if not client_params or len(client_params) != len(sizes):
        raise ValueError("need one size per client and at least one client")
    if any(s < 0 for s in sizes):
        raise ValueError("sizes must be non-negative")
    total = float(sum(sizes))
    if total == 0:
        raise ValueError("total size is zero")
    keys = set(client_params[0])
    for p in client_params:
        if set(p) != keys or any(np.shape(p[k]) != np.shape(client_params[0][k]) for k in keys):
            raise ValueError("clients have mismatched parameters")
    return {k: sum((s / total) * np.asarray(p[k], dtype=float) for s, p in zip(sizes, client_params))
            for k in client_params[0]}
