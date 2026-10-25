r"""Reference solution for PY-20 Matrix Transpose with Validation.

Validation runs first so the comprehension can assume a rectangle. The outer comprehension loops
over column indices of the input (rows of the output), the inner one collects that column from
every row. When rows are empty, `n == 0` and the result is `[]`, which correctly represents a
0-row matrix. New lists are built, so the input is untouched.
"""
def transpose(matrix):
    if not matrix:
        return []
    n = len(matrix[0])
    for row in matrix:
        if len(row) != n:
            raise ValueError("ragged matrix")
    return [[row[j] for row in matrix] for j in range(n)]
