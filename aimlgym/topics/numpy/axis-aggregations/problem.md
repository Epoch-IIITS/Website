# NP-05 · Aggregations Along Axes

**Topic:** NumPy · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** NP-02 Vectorised Arithmetic and ufuncs

Read the lesson first: [article.md](article.md)

## Task

Write `summarize(X)` for a non-empty 2-D array, returning a dict:
* `"col_means"`: mean of each column (shape `(n_cols,)`),
* `"row_sums"`: sum of each row,
* `"row_argmax"`: index of the max in each row,
* `"max_pos"`: `(row, col)` tuple of Python ints of the overall maximum (first occurrence),
* `"row_means_keep"`: row means with shape `(n_rows, 1)`.

Raise `ValueError` if `X` is not 2-D or is empty. No Python loops.

**Example**
```python
s = summarize(np.array([[1, 5, 2], [7, 0, 3]]))
s["col_means"]   # array([4. , 2.5, 2.5])
s["max_pos"]     # (1, 0)
s["row_means_keep"].shape   # (2, 1)
```

## Hints

<details><summary>Hint 1</summary>

Validate `X.ndim == 2 and X.size > 0`.

</details>

<details><summary>Hint 2</summary>

Reductions: `X.mean(axis=0)`, `X.sum(axis=1)`, `X.argmax(axis=1)`.

</details>

<details><summary>Hint 3</summary>

`r, c = np.unravel_index(X.argmax(), X.shape)` then `(int(r), int(c))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_col_means` | Column means collapse axis 0. |
| `test_max_pos` | Use np.unravel_index on the flat argmax. |
| `test_keepdims` | Pass keepdims=True so the shape is (n_rows, 1). |
| `test_bad_input` | Reject arrays with ndim != 2. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each entry is one reduction along the appropriate axis. The global maximum's flat index is
converted to a 2-D position with `unravel_index`, and `keepdims=True` preserves a column shape
for later broadcasting.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
