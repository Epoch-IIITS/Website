r"""Reference solution for DL-01 Activation Functions.

Each function is one vectorised expression. Gradients use strict `z > 0`, giving the framework
convention at zero. All functions build new arrays, so inputs are never modified.
"""
import numpy as np


def relu(z):
    return np.maximum(np.asarray(z, dtype=float), 0.0)


def relu_grad(z):
    return (np.asarray(z) > 0).astype(float)


def leaky_relu(z, alpha=0.01):
    z = np.asarray(z, dtype=float)
    return np.where(z > 0, z, alpha * z)


def leaky_relu_grad(z, alpha=0.01):
    return np.where(np.asarray(z) > 0, 1.0, alpha)


def tanh(z):
    return np.tanh(np.asarray(z, dtype=float))


def tanh_grad(z):
    t = np.tanh(np.asarray(z, dtype=float))
    return 1.0 - t ** 2
