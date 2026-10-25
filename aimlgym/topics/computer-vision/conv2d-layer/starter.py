import numpy as np


def conv_output_size(n, k, padding=0, stride=1):
    # TODO
    return n - k + 1


def conv2d(x, weight, bias=None, stride=1, padding=0):
    x = np.asarray(x, dtype=float)
    weight = np.asarray(weight, dtype=float)
    # TODO: pad, then loop over output channels and positions
    return np.zeros((weight.shape[0], 1, 1))


def conv_params(c_in, c_out, k):
    # TODO
    return 0
