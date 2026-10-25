r"""Reference solution for CV-15 A Convolution Layer with Channels.

Padding is applied once to the spatial axes. For each output position the input patch has shape
`(C_in, k, k)`; contracting it with all filters at once (`tensordot` over the channel and kernel
axes) yields one value per output channel, to which the bias is added. The output size follows
the floor formula, which also rejects impossible configurations.
"""
import numpy as np


def conv_output_size(n, k, padding=0, stride=1):
    out = (n + 2 * padding - k) // stride + 1
    if out < 1:
        raise ValueError("kernel larger than padded input")
    return out


def conv2d(x, weight, bias=None, stride=1, padding=0):
    x = np.asarray(x, dtype=float)
    weight = np.asarray(weight, dtype=float)
    c_out, c_in, k, _ = weight.shape
    if x.shape[0] != c_in:
        raise ValueError("input channels do not match the weights")
    bias = np.zeros(c_out) if bias is None else np.asarray(bias, dtype=float)
    h_out = conv_output_size(x.shape[1], k, padding, stride)
    w_out = conv_output_size(x.shape[2], k, padding, stride)
    xp = np.pad(x, ((0, 0), (padding, padding), (padding, padding)))
    out = np.zeros((c_out, h_out, w_out))
    for i in range(h_out):
        for j in range(w_out):
            patch = xp[:, i * stride:i * stride + k, j * stride:j * stride + k]
            out[:, i, j] = np.tensordot(weight, patch, axes=([1, 2, 3], [0, 1, 2])) + bias
    return out


def conv_params(c_in, c_out, k):
    return c_out * (c_in * k * k + 1)
