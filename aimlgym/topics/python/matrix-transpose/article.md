# Nested Lists and the Transpose

## Learning outcomes

After this lesson you can:

- Use nested list comprehensions
- Validate rectangular shape
- Reason about rows and columns by index

## Intuition
A matrix stored as a list of rows is like a spreadsheet. The **transpose** flips it over its
diagonal: rows become columns. Row 0 of the result is column 0 of the original.

## Precise explanation
For an $m \times n$ matrix $A$, the transpose $A^\top$ is $n \times m$ with
$(A^\top)_{ji} = A_{ij}$.

As a nested comprehension (outer loop over output rows = input columns):
```python
[[matrix[i][j] for i in range(m)] for j in range(n)]
```
Equivalently with `zip`: `[list(col) for col in zip(*matrix)]`. `zip(*matrix)` unpacks the rows
as separate arguments and groups the i-th elements together. **Warning:** `zip` silently stops
at the shortest row, so it hides ragged input — validate first.

A matrix is **rectangular** when every row has the same length. A "ragged" list of lists is not a
matrix.

Edge cases: an empty matrix `[]` transposes to `[]`. A matrix of empty rows `[[], []]` has
shape 2×0; its transpose is 0×2, which as a list of rows is `[]`.

## Worked example
```
[[1, 2, 3],        [[1, 4],
 [4, 5, 6]]   →     [2, 5],
                    [3, 6]]
```
Shape (2, 3) → (3, 2).

## Common mistakes
* Swapping loop order in the comprehension, which returns a copy instead of the transpose.
* `[[0]*m]*n` to pre-allocate — every row is the **same** list object; writing one cell changes
  all rows.
* Mutating the input in place.

## Why this matters
Transposes are everywhere in ML: $X^\top X$ in least squares (ML-09), switching between
"samples × features" and "features × samples", attention's $QK^\top$ (LM-07). Shape validation
is the habit that prevents silent broadcasting bugs in NumPy.

## Library implementation

The idiomatic transpose of a rectangular list of lists is `[list(row) for row in zip(*matrix)]`:
`zip(*matrix)` passes every row as a separate argument and yields one tuple per column. It does
not validate ragged input (it silently stops at the shortest row), which is why the exercise asks
for explicit checks. In NP-01 and later, NumPy's `array.T` does the same for arrays.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
