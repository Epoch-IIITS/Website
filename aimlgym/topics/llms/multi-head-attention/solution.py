r"""Reference solution for LM-10 Multi-Head Attention.

Reshape-then-transpose keeps each position's features together while grouping them by head.
Batched matrix products compute all heads' attention at once; merging reverses the split and the
output projection mixes information across heads.
"""
import numpy as np


def split_heads(X, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    if h < 1 or d % h:
        raise ValueError("d_model must be divisible by h")
    return X.reshape(T, h, d // h).transpose(1, 0, 2)


def merge_heads(Xh):
    h, T, dh = Xh.shape
    return Xh.transpose(1, 0, 2).reshape(T, h * dh)


def multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal=False):
    X = np.asarray(X, dtype=float)
    Qh, Kh, Vh = (split_heads(X @ W, h) for W in (Wq, Wk, Wv))
    dh = Qh.shape[-1]
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(dh)
    if causal:
        T = X.shape[0]
        scores = np.where(np.tril(np.ones((T, T), dtype=bool))[None], scores, -np.inf)
    scores = scores - scores.max(axis=-1, keepdims=True)
    w = np.exp(scores)
    w = w / w.sum(axis=-1, keepdims=True)
    return merge_heads(w @ Vh) @ Wo
