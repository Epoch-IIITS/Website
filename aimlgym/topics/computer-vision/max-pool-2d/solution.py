r"""Reference solution for CV-14 2D Max Pooling.

`sliding_window_view` exposes every window; taking every `stride`-th window along both axes gives
exactly the pooled grid, whose shape matches the output-size formula. Reducing over the last two
axes computes the max or mean of each window.
"""
import numpy as np


def pool2d(x, size=2, stride=None, mode="max"):
    x = np.asarray(x)
    stride = size if stride is None else stride
    if size < 1 or stride < 1 or mode not in ("max", "avg"):
        raise ValueError("invalid size, stride or mode")
    H, W = x.shape
    if size > H or size > W:
        raise ValueError("window larger than input")
    win = np.lib.stride_tricks.sliding_window_view(x, (size, size))[::stride, ::stride]
    return win.max(axis=(2, 3)) if mode == "max" else win.mean(axis=(2, 3))
