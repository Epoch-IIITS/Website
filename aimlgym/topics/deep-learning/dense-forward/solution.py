r"""Reference solution for DL-04 Dense Layer Forward Pass.

The forward pass is one matrix product plus a broadcast bias, guarded by shape checks. Each
layer has (inputs + 1) × outputs parameters. He initialisation scales the weight spread by the
fan-in to keep signal variance stable through ReLU layers.
"""
import numpy as np


def dense(X, W, b):
    X, W, b = (np.asarray(a, dtype=float) for a in (X, W, b))
    if X.ndim != 2 or W.ndim != 2 or X.shape[1] != W.shape[0] or b.shape != (W.shape[1],):
        raise ValueError("shape mismatch")
    return X @ W + b


def n_params(layer_sizes):
    if len(layer_sizes) < 2 or any(s < 1 for s in layer_sizes):
        raise ValueError("need at least two positive layer sizes")
    return int(sum((a + 1) * c for a, c in zip(layer_sizes[:-1], layer_sizes[1:])))


def he_init(fan_in, fan_out, rng):
    W = rng.normal(0.0, np.sqrt(2.0 / fan_in), size=(fan_in, fan_out))
    return W, np.zeros(fan_out)
