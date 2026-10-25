r"""Reference solution for CV-05 Flip and Rotate.

Negative-step slices reverse an axis. Swapping the two spatial axes and then reversing columns
maps pixel (r, c) to (c, H−1−r), a clockwise quarter turn; channels stay last because only axes
0 and 1 are swapped.
"""
import numpy as np


def flip_horizontal(img):
    return np.asarray(img)[:, ::-1]


def flip_vertical(img):
    return np.asarray(img)[::-1]


def rotate90_cw(img, k=1):
    out = np.asarray(img)
    for _ in range(k % 4):
        out = np.swapaxes(out, 0, 1)[:, ::-1]
    return out
