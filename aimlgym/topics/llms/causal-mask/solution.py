r"""Reference solution for LM-08 Causal Masking.

`tril` builds the causal pattern; comparing positions with lengths builds padding masks by
broadcasting. Their conjunction over keys, plus the diagonal, gives a per-sequence mask in which
every query has at least one allowed key.
"""
import numpy as np


def causal_mask(T):
    if T < 1:
        raise ValueError("T must be >= 1")
    return np.tril(np.ones((T, T), dtype=bool))


def padding_mask(lengths, T):
    L = np.asarray(lengths)
    if L.ndim != 1 or (L < 1).any() or (L > T).any():
        raise ValueError("lengths must be in 1..T")
    return np.arange(T)[None, :] < L[:, None]


def combined_mask(lengths, T):
    m = causal_mask(T)[None, :, :] & padding_mask(lengths, T)[:, None, :]
    return m | np.eye(T, dtype=bool)[None, :, :]
