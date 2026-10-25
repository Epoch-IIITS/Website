r"""Reference solution for MA-06 Matrix Multiplication.

`_shape` validates each matrix and returns its dimensions. After checking the inner dimensions,
`zip(*B)` gives B's columns (safe now that B is rectangular), and each output entry is the dot
product of a row of A with a column of B — the definition, written once.
"""
def _shape(M):
    if not M or not M[0]:
        raise ValueError("matrix must be non-empty")
    n = len(M[0])
    if any(len(row) != n for row in M):
        raise ValueError("ragged matrix")
    return len(M), n


def matmul(A, B):
    m, n = _shape(A)
    n2, p = _shape(B)
    if n != n2:
        raise ValueError(f"incompatible shapes ({m}x{n}) and ({n2}x{p})")
    cols = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in cols] for row in A]
