r"""Reference solution for NP-09 Fancy Indexing and Gather.

Integer-array indexing gathers rows directly. Pairing `arange(n)` with the column indices picks
one element per row. Sorting the negated values with a stable algorithm yields descending order
with ties resolved by original position.
"""
import numpy as np


def gather_rows(X, idx):
    return np.asarray(X)[np.asarray(idx, dtype=int)]


def pick_per_row(P, cols):
    P = np.asarray(P)
    cols = np.asarray(cols, dtype=int)
    if cols.shape != (P.shape[0],):
        raise ValueError("need one column index per row")
    return P[np.arange(P.shape[0]), cols]


def top_k(v, k):
    v = np.asarray(v)
    if not 1 <= k <= len(v):
        raise ValueError("k out of range")
    return np.argsort(-v, kind="stable")[:k]
