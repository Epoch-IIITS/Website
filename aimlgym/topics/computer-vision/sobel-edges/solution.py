r"""Reference solution for CV-12 Sobel Edge Magnitude.

A valid cross-correlation helper applies each 3×3 kernel; the two gradient maps combine into a
magnitude with `hypot`. Using floats preserves negative gradients.
"""
import numpy as np

KX = np.array([[-1., 0., 1.], [-2., 0., 2.], [-1., 0., 1.]])
KY = KX.T


def _valid(g, K):
    H, W = g.shape
    out = np.zeros((H - 2, W - 2))
    for u in range(3):
        for v in range(3):
            out += K[u, v] * g[u:u + H - 2, v:v + W - 2]
    return out


def sobel(gray):
    g = np.asarray(gray, dtype=float)
    if g.ndim != 2 or g.shape[0] < 3 or g.shape[1] < 3:
        raise ValueError("image must be at least 3x3")
    gx, gy = _valid(g, KX), _valid(g, KY)
    return gx, gy, np.hypot(gx, gy)


def edges(gray, t):
    return sobel(gray)[2] > t
