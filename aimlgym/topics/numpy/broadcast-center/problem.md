# NP-07 · Centering Columns with Broadcasting

**Topic:** NumPy · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NP-05 Aggregations Along Axes, ST-05 Standardize to z-scores

Read the lesson first: [article.md](article.md)

## Task

For a 2-D float array `X` of shape `(n, d)`, implement without loops:
* `center_columns(X)` → `X` minus its column means.
* `scale_rows(X, w)` → row `i` multiplied by `w[i]`; raise `ValueError` if `len(w) != n`.
* `standardize(X)` → `(X - mean) / std` per column (population std); columns with std 0 become
  all zeros (no division by zero, no NaN).

**Examples**
```python
X = np.array([[1., 2.], [3., 6.]])
center_columns(X)              # [[-1., -2.], [ 1.,  2.]]
scale_rows(X, [10, 0.5])       # [[10., 20.], [ 1.5, 3.]]
standardize(np.array([[1., 5.], [3., 5.]]))   # [[-1., 0.], [1., 0.]]
```

## Hints

<details><summary>Hint 1</summary>

`X - X.mean(axis=0)` broadcasts a (d,) vector over rows.

</details>

<details><summary>Hint 2</summary>

`np.asarray(w)[:, None]` turns w into an (n, 1) column.

</details>

<details><summary>Hint 3</summary>

Replace zero stds with 1 before dividing: `std = np.where(std == 0, 1.0, std)` — the centred column is already 0.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_scale_rows` | Reshape w to (n, 1) with w[:, None] so it stretches across columns. |
| `test_standardize_constant` | Avoid dividing by zero for constant columns; they should become 0. |
| `test_standardize_props` | Use population std (np.std default ddof=0) per column. |
| `test_scale_rows_bad` | Validate len(w) == number of rows. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Column statistics have shape (d,), which broadcasts across the n rows. Row weights need an
explicit column shape (n, 1). For constant columns the centred values are already zero, so
dividing by 1 instead of 0 yields zeros without NaN.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
