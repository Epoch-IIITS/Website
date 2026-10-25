r"""Reference solution for NP-06 Matrix Products with @.

The loop version spells out $C_{ij} = \sum_k A_{ik}B_{kj}$; `@` performs the same computation in
compiled code. Checking `A.shape[1] == B.shape[0]` first produces a clear message. Scoring a batch
is one matrix–vector product plus a broadcast scalar, and the Gram matrix collects every pairwise
dot product of the rows.
"""
import numpy as np


def matmul_loops(A, B):
    n = len(B)
    if any(len(row) != n for row in A):
        raise ValueError("inner dimensions differ")
    p = len(B[0]) if B else 0
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)] for i in range(len(A))]


def matmul(A, B):
    A = np.asarray(A)
    B = np.asarray(B)
    if A.shape[1] != B.shape[0]:
        raise ValueError(f"cannot multiply {A.shape} by {B.shape}")
    return A @ B


def batch_scores(X, w, b):
    return np.asarray(X, dtype=float) @ np.asarray(w, dtype=float) + b


def gram(X):
    X = np.asarray(X, dtype=float)
    return X @ X.T
