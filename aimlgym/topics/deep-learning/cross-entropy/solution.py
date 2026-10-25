r"""Reference solution for DL-03 Cross-Entropy Loss.

A stable log-softmax gives log-probabilities directly, and paired indexing selects each row's
correct-class entry. The gradient is softmax minus one-hot, divided by the batch size because the
loss is a mean.
"""
import numpy as np


def _check(logits, labels):
    z = np.asarray(logits, dtype=float)
    y = np.asarray(labels, dtype=int)
    if z.ndim != 2 or y.shape != (z.shape[0],):
        raise ValueError("logits must be (n, K) and labels (n,)")
    if y.size and (y.min() < 0 or y.max() >= z.shape[1]):
        raise ValueError("label out of range")
    s = z - z.max(axis=1, keepdims=True)
    lsm = s - np.log(np.exp(s).sum(axis=1, keepdims=True))
    return lsm, y


def cross_entropy(logits, labels):
    lsm, y = _check(logits, labels)
    return float(-lsm[np.arange(len(y)), y].mean())


def cross_entropy_grad(logits, labels):
    lsm, y = _check(logits, labels)
    n = len(y)
    g = np.exp(lsm)
    g[np.arange(n), y] -= 1.0
    return g / n
