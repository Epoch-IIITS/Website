# PY-20 · Matrix Transpose with Validation

**Topic:** Python · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** PY-19 Validated Factorial

Read the lesson first: [article.md](article.md)

## Task

Write `transpose(matrix)` for a list of lists of numbers.

**Requirements**
* Return a new list of lists equal to the transpose. Do not modify the input.
* If rows have different lengths, raise `ValueError("ragged matrix")`.
* `[]` and any matrix whose rows are all empty return `[]`.
* Do not use NumPy.

**Constraints:** up to 500×500.

**Examples**
```python
transpose([[1, 2, 3], [4, 5, 6]])   # [[1, 4], [2, 5], [3, 6]]
transpose([[7]])                    # [[7]]
transpose([[1, 2], [3]])            # raises ValueError — ragged
```

## Hints

<details><summary>Hint 1</summary>

Let `n = len(matrix[0])`; every row must satisfy `len(row) == n`.

</details>

<details><summary>Hint 2</summary>

Output row `j` is `[row[j] for row in matrix]`.

</details>

<details><summary>Hint 3</summary>

`[[row[j] for row in matrix] for j in range(n)]` builds the whole result.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_ragged` | Check every row length before transposing; zip() hides ragged rows. |
| `test_2x3` | The outer loop must run over columns (j), the inner over rows. |
| `test_independent_rows` | Don't create rows with `[[0]*m]*n`; each row must be a separate list. |
| `test_empty_rows` | Rows of length 0 give n = 0, so the result is []. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Validation runs first so the comprehension can assume a rectangle. The outer comprehension loops
over column indices of the input (rows of the output), the inner one collects that column from
every row. When rows are empty, `n == 0` and the result is `[]`, which correctly represents a
0-row matrix. New lists are built, so the input is untouched.

## References

- [The Python Tutorial (Python 3.15.1 docs)](https://docs.python.org/3/tutorial/) — Python Software Foundation (`S001`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
