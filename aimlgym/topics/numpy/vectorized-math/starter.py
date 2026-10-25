import numpy as np


def dot_loop(a, b):
    if len(a) != len(b):
        raise ValueError("length mismatch")
    total = 0.0
    for x, y in zip(a, b):
        total += x * y
    return total


def dot_vectorized(a, b):
    # TODO: element-wise multiply, then sum
    return 0.0


def fahrenheit(celsius):
    # TODO
    return np.asarray(celsius, dtype=float)


def rms(x):
    # TODO
    return 0.0


def sigmoid(x):
    x = np.asarray(x, dtype=float)
    # TODO: stable version with np.exp(-np.abs(x)) and np.where
    return 1 / (1 + np.exp(-x))
