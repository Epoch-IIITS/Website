r"""Reference solution for MA-08 Solve a 2x2 System (Cramer's Rule).

The function validates shapes, computes the determinant, and treats tiny determinants as
singular using a tolerance. Cramer's rule then gives each unknown as a ratio of determinants.
The variable is named `b12` to avoid clashing with the right-hand-side vector `b`.
"""
def solve_2x2(A, b, tol=1e-12):
    if len(A) != 2 or any(len(r) != 2 for r in A) or len(b) != 2:
        raise ValueError("A must be 2x2 and b length 2")
    (a, b12), (c, d) = A
    e, f = b
    det = a * d - b12 * c
    if abs(det) < tol:
        raise ValueError("singular")
    x = (e * d - b12 * f) / det
    y = (a * f - e * c) / det
    return float(x), float(y)
