import numpy as np


def matmul_loops(A, B):
    # TODO: three nested loops
    return []


def matmul(A, B):
    A = np.asarray(A)
    B = np.asarray(B)
    # TODO: check shapes, then use @
    return A * B


def batch_scores(X, w, b):
    # TODO
    return np.zeros(len(X))


def gram(X):
    # TODO
    return np.asarray(X)
