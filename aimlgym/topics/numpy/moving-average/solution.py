r"""Reference solution for NP-14 Moving Average with cumsum.

Prefix sums turn each window sum into one subtraction, so all n − w + 1 means come from two
vector slices. `sliding_window_view` exposes every window as a strided view without copying.
"""
import numpy as np


def moving_average(x, w):
    x = np.asarray(x, dtype=float)
    if not 1 <= w <= len(x):
        raise ValueError("w must satisfy 1 <= w <= len(x)")
    c = np.concatenate([[0.0], np.cumsum(x)])
    return (c[w:] - c[:-w]) / w


def windows(x, w):
    x = np.asarray(x)
    if not 1 <= w <= len(x):
        raise ValueError("w must satisfy 1 <= w <= len(x)")
    return np.lib.stride_tricks.sliding_window_view(x, w)
