r"""Reference solution for LM-09 Sinusoidal Positional Encoding.

A `(T, d/2)` grid of angles is built by broadcasting positions against frequencies; sines fill even
columns and cosines odd columns.
"""
import numpy as np


def positional_encoding(T, d):
    if T < 1 or d < 2 or d % 2:
        raise ValueError("T >= 1 and even d >= 2 required")
    pos = np.arange(T)[:, None]
    i = np.arange(d // 2)[None, :]
    angles = pos / np.power(10000.0, 2 * i / d)
    pe = np.zeros((T, d))
    pe[:, 0::2] = np.sin(angles)
    pe[:, 1::2] = np.cos(angles)
    return pe
