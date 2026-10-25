r"""Reference solution for LM-03 Logits, Temperature and Softmax.

Scaling logits by 1/T before a stable softmax implements temperature. Entropy ignores zero
entries, matching the 0·log 0 = 0 convention.
"""
import numpy as np


def softmax_t(logits, T=1.0):
    if T <= 0:
        raise ValueError("temperature must be positive")
    z = np.asarray(logits, dtype=float) / T
    e = np.exp(z - z.max())
    return e / e.sum()


def entropy(p):
    p = np.asarray(p, dtype=float)
    nz = p[p > 0]
    return float(-(nz * np.log(nz)).sum())
