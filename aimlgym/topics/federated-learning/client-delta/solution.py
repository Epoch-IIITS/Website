r"""Reference solution for FL-03 Client Updates as Deltas.

Deltas are local minus global parameters. The server takes their size-weighted mean and steps in
that direction with its own learning rate; with rate 1 the result is algebraically identical to
FedAvg.
"""
import numpy as np


def client_delta(global_w, local_w):
    g = np.asarray(global_w, dtype=float)
    l = np.asarray(local_w, dtype=float)
    if g.shape != l.shape:
        raise ValueError("shape mismatch")
    return l - g


def server_update(global_w, deltas, sizes, server_lr=1.0):
    if not deltas or len(deltas) != len(sizes):
        raise ValueError("need one size per delta")
    total = float(sum(sizes))
    if total == 0:
        raise ValueError("total size is zero")
    g = np.asarray(global_w, dtype=float)
    mean = sum((n / total) * np.asarray(d, dtype=float) for n, d in zip(sizes, deltas))
    return g + server_lr * mean
