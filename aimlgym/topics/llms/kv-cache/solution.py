r"""Reference solution for LM-15 Incremental Decoding with a KV Cache.

The full version builds all queries, keys and values and masks the future. The cached version
computes projections only for the new token, appends its key and value, and attends over every
cached row — exactly the keys a causal mask would allow — so both give identical outputs.
"""
import numpy as np


def _softmax(s, axis=-1):
    s = s - s.max(axis=axis, keepdims=True)
    e = np.exp(s)
    return e / e.sum(axis=axis, keepdims=True)


def full_causal_attention(X, Wq, Wk, Wv):
    X = np.asarray(X, dtype=float)
    Q, K, V = X @ Wq, X @ Wk, X @ Wv
    T, d = Q.shape
    s = Q @ K.T / np.sqrt(d)
    s = np.where(np.tril(np.ones((T, T), dtype=bool)), s, -np.inf)
    return _softmax(s, axis=1) @ V


class KVCache:
    def __init__(self, Wq, Wk, Wv):
        self.Wq = np.asarray(Wq, dtype=float)
        self.Wk = np.asarray(Wk, dtype=float)
        self.Wv = np.asarray(Wv, dtype=float)
        d = self.Wk.shape[1]
        self.K = np.zeros((0, d))
        self.V = np.zeros((0, self.Wv.shape[1]))

    def step(self, x_t):
        x_t = np.asarray(x_t, dtype=float)
        q, k, v = x_t @ self.Wq, x_t @ self.Wk, x_t @ self.Wv
        self.K = np.vstack([self.K, k])
        self.V = np.vstack([self.V, v])
        w = _softmax(self.K @ q / np.sqrt(q.shape[0]))
        return w @ self.V
