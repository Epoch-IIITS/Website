r"""Reference solution for CV-19 Bilinear Resize.

Row and column source coordinates are computed once with half-pixel centres and clamped. Fancy
indexing gathers the four neighbour grids, and broadcasting the fractional weights interpolates
horizontally and then vertically.
"""
import numpy as np


def _coords(n_out, n_in):
    c = (np.arange(n_out) + 0.5) * (n_in / n_out) - 0.5
    c = np.clip(c, 0, n_in - 1)
    c0 = np.floor(c).astype(int)
    c1 = np.minimum(c0 + 1, n_in - 1)
    return c0, c1, c - c0


def resize_bilinear(img, out_h, out_w):
    img = np.asarray(img, dtype=float)
    if img.ndim != 2 or out_h < 1 or out_w < 1:
        raise ValueError("2-D image and positive sizes required")
    H, W = img.shape
    y0, y1, wy = _coords(out_h, H)
    x0, x1, wx = _coords(out_w, W)
    wy = wy[:, None]
    wx = wx[None, :]
    top = img[y0][:, x0] * (1 - wx) + img[y0][:, x1] * wx
    bottom = img[y1][:, x0] * (1 - wx) + img[y1][:, x1] * wx
    return top * (1 - wy) + bottom * wy
