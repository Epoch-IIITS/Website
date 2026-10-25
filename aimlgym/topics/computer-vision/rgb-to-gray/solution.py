r"""Reference solution for CV-02 RGB to Grayscale.

Casting to float avoids uint8 overflow; a matrix product with the weight vector collapses the
channel axis. Conversion back rounds, clips and casts, in that order.
"""
import numpy as np

WEIGHTS = np.array([0.299, 0.587, 0.114])


def rgb_to_gray(img):
    img = np.asarray(img)
    if img.ndim != 3 or img.shape[-1] != 3:
        raise ValueError("expected an (H, W, 3) image")
    return img.astype(float) @ WEIGHTS


def to_uint8(x):
    return np.clip(np.rint(np.asarray(x, dtype=float)), 0, 255).astype(np.uint8)
