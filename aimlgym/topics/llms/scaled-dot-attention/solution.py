r"""Reference solution for LM-07 Scaled Dot-Product Attention.

Scores compare every query with every key, scaled by √d. Masked positions become −∞ so their
softmax weight is exactly 0. A stable row-wise softmax gives attention weights, which mix the value
vectors.
"""
import numpy as np


def attention(Q, K, V, mask=None):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    if Q.ndim != 2 or K.ndim != 2 or V.ndim != 2 or Q.shape[1] != K.shape[1] or K.shape[0] != V.shape[0]:
        raise ValueError("incompatible shapes")
    scores = Q @ K.T / np.sqrt(Q.shape[1])
    if mask is not None:
        m = np.broadcast_to(np.asarray(mask, dtype=bool), scores.shape)
        if not m.any(axis=1).all():
            raise ValueError("a query row has no allowed keys")
        scores = np.where(m, scores, -np.inf)
    scores = scores - scores.max(axis=1, keepdims=True)
    w = np.exp(scores)
    w = w / w.sum(axis=1, keepdims=True)
    return w @ V, w
