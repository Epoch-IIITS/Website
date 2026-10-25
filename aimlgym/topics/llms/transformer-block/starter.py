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
    # TODO
    return x


def feed_forward(x, W1, b1, W2, b2):
    # TODO
    return x


def transformer_block(x, params, h):
    # TODO: x + MHA(LN1(x)), then + FFN(LN2(.))
    return x
