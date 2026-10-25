r"""Reference solution for NP-02 Vectorised Arithmetic and ufuncs.

Converting inputs to float arrays makes every operator element-wise. The dot product becomes one
multiplication and one reduction; RMS chains a power, a mean and a square root. The sigmoid only
exponentiates non-positive numbers, so both branches given to `np.where` are finite everywhere.
"""
import numpy as np


def dot_loop(a, b):
    if len(a) != len(b):
        raise ValueError("length mismatch")
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total


def dot_vectorized(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("shape mismatch")
    return float((a * b).sum())


def fahrenheit(celsius):
    return np.asarray(celsius, dtype=float) * 9 / 5 + 32


def rms(x):
    x = np.asarray(x, dtype=float)
    return float(np.sqrt(np.mean(x ** 2)))


def sigmoid(x):
    x = np.asarray(x, dtype=float)
    e = np.exp(-np.abs(x))
    return np.where(x >= 0, 1 / (1 + e), e / (1 + e))
