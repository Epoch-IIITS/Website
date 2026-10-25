r"""Reference solution for DL-21 Inverted Dropout.

Training mode samples a keep-mask with probability 1 − p and rescales the survivors, so the
expected output equals the input. Evaluation mode is the identity. The backward pass reuses the
forward mask because the operation is element-wise multiplication by a constant.
"""
import numpy as np


def dropout_forward(x, p, rng, training=True):
    if not 0 <= p < 1:
        raise ValueError("p must be in [0, 1)")
    x = np.asarray(x, dtype=float)
    if not training:
        return x.copy(), None
    mask = rng.random(x.shape) >= p
    return x * mask / (1.0 - p), mask


def dropout_backward(grad_out, mask, p):
    return np.asarray(grad_out, dtype=float) * mask / (1.0 - p)
