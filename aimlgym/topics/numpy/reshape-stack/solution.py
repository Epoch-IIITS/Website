r"""Reference solution for NP-08 Reshape and Stack.

Truncating to a multiple of the batch size makes the reshape valid. The bias column is a
column of ones joined horizontally. Flattening keeps the batch axis and lets `-1` compute H·W.
"""
import numpy as np


def to_batches(x, batch_size):
    x = np.asarray(x)
    if batch_size < 1 or batch_size > len(x):
        raise ValueError("invalid batch_size")
    m = len(x) // batch_size
    return x[: m * batch_size].reshape(m, batch_size)


def add_bias_column(X):
    X = np.asarray(X, dtype=float)
    return np.hstack([np.ones((X.shape[0], 1)), X])


def flatten_images(imgs):
    imgs = np.asarray(imgs)
    if imgs.ndim != 3:
        raise ValueError("expected (N, H, W)")
    return imgs.reshape(imgs.shape[0], -1)
