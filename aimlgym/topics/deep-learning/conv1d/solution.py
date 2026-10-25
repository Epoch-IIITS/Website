r"""Reference solution for DL-25 1D Convolution by Hand (valid, stride).

The output length comes from the formula, which also validates the configuration. After zero
padding, each output is the dot product of the kernel with the window starting at i·stride — the
cross-correlation used by deep-learning libraries.
"""
import numpy as np


def conv_output_length(n, k, stride, padding):
    if k < 1 or stride < 1 or padding < 0:
        raise ValueError("invalid k, stride or padding")
    out = (n + 2 * padding - k) // stride + 1
    if out < 1:
        raise ValueError("kernel larger than padded input")
    return int(out)


def conv1d(x, kernel, stride=1, padding=0, bias=0.0):
    x = np.asarray(x, dtype=float)
    w = np.asarray(kernel, dtype=float)
    k = len(w)
    m = conv_output_length(len(x), k, stride, padding)
    xp = np.pad(x, padding)
    return np.array([xp[i * stride:i * stride + k] @ w for i in range(m)]) + bias
