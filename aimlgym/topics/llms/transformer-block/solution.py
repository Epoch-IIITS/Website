r"""Reference solution for LM-12 A Pre-Norm Transformer Block by Hand.

Layer norm standardises each token's feature vector with its own mean and population variance.
The block applies "normalise → sub-layer → add back the input" twice: once with causal
multi-head attention, once with the feed-forward network. Because every operation either works
row by row or uses a causal mask, output row t never sees input rows after t.
"""
import numpy as np


def _softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal=False):
    T, d = X.shape
    dh = d // h
    split = lambda M: (X @ M).reshape(T, h, dh).transpose(1, 0, 2)
    Q, K, V = split(Wq), split(Wk), split(Wv)
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(dh)
    if causal:
        scores = np.where(np.tril(np.ones((T, T), dtype=bool)), scores, -np.inf)
    out = _softmax(scores) @ V
    return out.transpose(1, 0, 2).reshape(T, d) @ Wo


def layer_norm(x, gamma, beta, eps=1e-5):
    x = np.asarray(x, dtype=float)
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mu) / np.sqrt(var + eps) + beta


def feed_forward(x, W1, b1, W2, b2):
    return np.maximum(x @ W1 + b1, 0) @ W2 + b2


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    a = layer_norm(x, p["ln1_g"], p["ln1_b"])
    h1 = x + multi_head_attention(a, p["Wq"], p["Wk"], p["Wv"], p["Wo"], h, causal=True)
    f = layer_norm(h1, p["ln2_g"], p["ln2_b"])
    return h1 + feed_forward(f, p["W1"], p["b1"], p["W2"], p["b2"])
