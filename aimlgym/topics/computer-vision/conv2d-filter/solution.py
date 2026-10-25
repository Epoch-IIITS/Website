r"""Reference solution for CV-10 2D Filtering (Blur).

Padding by the kernel radius keeps the output size equal to the input. Instead of looping over
pixels, the code loops over the (few) kernel entries and adds a shifted copy of the padded image
weighted by that entry — a vectorised cross-correlation.
"""
import numpy as np


def filter2d(img, kernel, mode="zero"):
    img = np.asarray(img, dtype=float)
    K = np.asarray(kernel, dtype=float)
    if K.ndim != 2 or K.shape[0] % 2 == 0 or K.shape[1] % 2 == 0:
        raise ValueError("kernel dimensions must be odd")
    if mode not in ("zero", "edge"):
        raise ValueError("mode must be 'zero' or 'edge'")
    rh, rw = K.shape[0] // 2, K.shape[1] // 2
    P = np.pad(img, ((rh, rh), (rw, rw)), mode="constant" if mode == "zero" else "edge")
    H, W = img.shape
    out = np.zeros_like(img)
    for u in range(K.shape[0]):
        for v in range(K.shape[1]):
            out += K[u, v] * P[u:u + H, v:v + W]
    return out


def box_kernel(k):
    if k < 1 or k % 2 == 0:
        raise ValueError("k must be odd and >= 1")
    return np.full((k, k), 1.0 / (k * k))


def gaussian_kernel(k, sigma):
    if k < 1 or k % 2 == 0 or sigma <= 0:
        raise ValueError("odd k >= 1 and sigma > 0 required")
    ax = np.arange(k) - k // 2
    g = np.exp(-(ax[:, None] ** 2 + ax[None, :] ** 2) / (2 * sigma ** 2))
    return g / g.sum()
