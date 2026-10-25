r"""Reference solution for CV-07 Binary Thresholding.

A comparison produces the mask; inversion is logical NOT. The mean of a boolean mask is the
foreground fraction. Masking uses `np.where`, adding a channel axis for colour images so the mask
broadcasts, and preserves the input dtype.
"""
import numpy as np


def threshold(gray, t, invert=False):
    m = np.asarray(gray) > t
    return ~m if invert else m


def foreground_fraction(mask):
    mask = np.asarray(mask, dtype=bool)
    if mask.size == 0:
        raise ValueError("empty mask")
    return float(mask.mean())


def apply_mask(img, mask):
    img = np.asarray(img)
    mask = np.asarray(mask, dtype=bool)
    if img.shape[:2] != mask.shape:
        raise ValueError("mask must match image height and width")
    m = mask if img.ndim == 2 else mask[..., None]
    return np.where(m, img, 0).astype(img.dtype)
