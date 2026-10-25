r"""Reference solution for MA-03 The Sigmoid Function.

Each branch of `sigmoid` only exponentiates a non-positive number, so `math.exp` never
overflows; the two formulas are algebraically equal. The derivative reuses the forward value,
which is how backpropagation computes it cheaply. `logit` validates its domain before the log.
"""
import math


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    z = math.exp(x)
    return z / (1 + z)


def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)


def logit(p):
    if not 0 < p < 1:
        raise ValueError("p must be strictly between 0 and 1")
    return math.log(p / (1 - p))
