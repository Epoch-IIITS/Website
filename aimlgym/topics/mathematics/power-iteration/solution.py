r"""Reference solution for MA-16 Dominant Eigenvalue by Power Iteration.

Repeated multiplication amplifies the dominant eigen-direction; normalising each step keeps the
numbers bounded. The Rayleigh quotient of the unit vector estimates the eigenvalue and provides
the stopping test. Finally the sign is fixed (largest-magnitude entry positive) so the
eigenvector is reported reproducibly.
"""
import math


def _matvec(A, v):
    return [sum(a * x for a, x in zip(row, v)) for row in A]


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def power_iteration(A, num_iters=1000, tol=1e-10):
    n = len(A)
    if n == 0 or any(len(row) != n for row in A):
        raise ValueError("A must be a non-empty square matrix")
    b = [1.0] * n
    lam = None
    for _ in range(num_iters):
        w = _matvec(A, b)
        nrm = math.sqrt(_dot(w, w))
        if nrm == 0:
            raise ValueError("A b is the zero vector; choose another start")
        b = [x / nrm for x in w]
        new_lam = _dot(b, _matvec(A, b))
        if lam is not None and abs(new_lam - lam) < tol:
            lam = new_lam
            break
        lam = new_lam
    k = max(range(n), key=lambda i: abs(b[i]))
    if b[k] < 0:
        b = [-x for x in b]
    return lam, b
