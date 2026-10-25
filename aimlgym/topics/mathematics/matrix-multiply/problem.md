# MA-06 · Matrix Multiplication

**Topic:** Mathematics for AI/ML · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** MA-04 Dot Product, PY-20 Matrix Transpose with Validation

Read the lesson first: [article.md](article.md)

## Task

Write `matmul(A, B)` multiplying two matrices given as lists of rows (pure Python).

* Raise `ValueError` if `A` or `B` is empty/ragged, or if `len(A[0]) != len(B)`.
* Return a new list of lists of shape `len(A) × len(B[0])`.

**Examples**
```python
matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])   # [[19, 22], [43, 50]]
matmul([[1, 2, 3]], [[1], [0], [-1]])        # [[-2]]   — (1×3)(3×1) = 1×1
matmul([[1, 2]], [[1, 2]])                   # raises ValueError — (1×2)(1×2)
```

## Hints

<details><summary>Hint 1</summary>

Write a helper that checks a matrix is non-empty and rectangular.

</details>

<details><summary>Hint 2</summary>

Compatibility: number of columns of A (`len(A[0])`) must equal rows of B (`len(B)`).

</details>

<details><summary>Hint 3</summary>

Triple loop over i, j, k, or a comprehension using `zip(*B)` to get B's columns.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_incompatible` | Compare columns of A with rows of B: len(A[0]) vs len(B). |
| `test_2x2` | Entry (i, j) is row i of A dotted with column j of B — not element-wise. |
| `test_column_times_row` | Output shape is len(A) × len(B[0]). |
| `test_ragged` | Validate every row length. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`_shape` validates each matrix and returns its dimensions. After checking the inner dimensions,
`zip(*B)` gives B's columns (safe now that B is rectangular), and each output entry is the dot
product of a row of A with a column of B — the definition, written once.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
