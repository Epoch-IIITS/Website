r"""Reference solution for DL-07 MLP Forward Pass.

Each iteration applies one dense layer, records its input and pre-activation for later
backpropagation, and applies ReLU except at the output. Class predictions use argmax on the
logits.
"""
import numpy as np


def mlp_forward(X, params):
    if not params:
        raise ValueError("params must contain at least one layer")
    a = np.asarray(X, dtype=float)
    cache = []
    last = len(params) - 1
    for l, (W, b) in enumerate(params):
        z = a @ W + b
        cache.append({"a_prev": a, "z": z})
        a = z if l == last else np.maximum(z, 0.0)
    return a, cache


def predict_classes(X, params):
    return mlp_forward(X, params)[0].argmax(axis=1)
