r"""Reference solution for DL-02 Numerically Stable Softmax.

Subtracting the maximum along the chosen axis keeps every exponent ≤ 0, so `exp` cannot overflow
and the denominator is at least 1. Log-softmax uses the same shift and the log-sum-exp identity
to avoid `log(0)`.
"""
import numpy as np


def softmax(z, axis=-1):
    z = np.asarray(z, dtype=float)
    e = np.exp(z - z.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)


def log_softmax(z, axis=-1):
    z = np.asarray(z, dtype=float)
    s = z - z.max(axis=axis, keepdims=True)
    return s - np.log(np.exp(s).sum(axis=axis, keepdims=True))
