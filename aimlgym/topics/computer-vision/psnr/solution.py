r"""Reference solution for CV-17 MSE and PSNR by Hand.

Converting to float before subtraction avoids uint8 wrap-around. PSNR applies the logarithmic
formula, handling the zero-error case explicitly.
"""
import math

import numpy as np


def mse(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape or a.size == 0:
        raise ValueError("images must be non-empty and the same shape")
    return float(np.mean((a - b) ** 2))


def psnr(a, b, max_val=255.0):
    m = mse(a, b)
    if m == 0:
        return math.inf
    return 10 * math.log10(max_val ** 2 / m)
