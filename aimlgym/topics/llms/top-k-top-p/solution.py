r"""Reference solution for LM-13 Top-k and Top-p Filtering.

A stable descending argsort gives the ranking. Top-k keeps a fixed prefix; top-p finds the first
prefix whose cumulative mass reaches the threshold (a tiny tolerance absorbs rounding such as
0.5 + 0.2 + 0.15 being slightly below 0.85) and keeps it. Both renormalise in vocabulary order.
Sampling inverts the CDF with `searchsorted`.
"""
import numpy as np


def _keep(p, idx):
    out = np.zeros_like(p)
    out[idx] = p[idx]
    return out / out.sum()


def top_k_filter(p, k):
    p = np.asarray(p, dtype=float)
    if not 1 <= k <= len(p):
        raise ValueError("k out of range")
    return _keep(p, np.argsort(-p, kind="stable")[:k])


def top_p_filter(p, top_p):
    p = np.asarray(p, dtype=float)
    if not 0 < top_p <= 1:
        raise ValueError("top_p must be in (0, 1]")
    order = np.argsort(-p, kind="stable")
    c = np.cumsum(p[order])
    n_keep = min(int(np.searchsorted(c, top_p - 1e-12)) + 1, len(p))
    return _keep(p, order[:n_keep])


def sample(p, u):
    p = np.asarray(p, dtype=float)
    if not 0 <= u < 1:
        raise ValueError("u must be in [0, 1)")
    i = int(np.searchsorted(np.cumsum(p), u, side="right"))
    if i >= len(p):
        i = int(np.flatnonzero(p > 0)[-1])
    return i
