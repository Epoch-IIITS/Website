r"""Reference solution for MA-09 Inverse of a 2x2 Matrix.

The adjugate formula is applied directly after shape and singularity checks. Dividing each entry
by the determinant produces floats.
"""
def inverse_2x2(A, tol=1e-12):
    if len(A) != 2 or any(len(r) != 2 for r in A):
        raise ValueError("A must be 2x2")
    (a, b), (c, d) = A
    det = a * d - b * c
    if abs(det) < tol:
        raise ValueError("matrix is singular")
    return [[d / det, -b / det], [-c / det, a / det]]
