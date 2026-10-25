# Aggregating Along Axes

## Learning outcomes

After this lesson you can:

- Aggregate along axis 0 and axis 1
- Use argmax and unravel_index
- Keep dimensions with keepdims

## Intuition
For a table of shape `(students, subjects)`, "average per subject" collapses the student axis;
"total per student" collapses the subject axis. The `axis` argument says **which axis
disappears**.

## Precise explanation
* `X.mean(axis=0)` → one value per column (rows collapsed), shape `(n_cols,)`.
* `X.sum(axis=1)` → one value per row, shape `(n_rows,)`.
* `keepdims=True` keeps the collapsed axis with length 1: `X.mean(axis=1, keepdims=True)` has
  shape `(n_rows, 1)` and broadcasts back against `X` (NP-07).
* `X.argmax(axis=1)` → index of the max in each row (first occurrence on ties).
* `X.argmax()` with no axis indexes the *flattened* array; `np.unravel_index(i, X.shape)` turns
  it back into `(row, col)`.

## Worked example
```python
X = np.array([[1, 5, 2],
              [7, 0, 3]])
X.mean(axis=0)     # [4. , 2.5, 2.5]
X.sum(axis=1)      # [ 8, 10]
X.argmax(axis=1)   # [1, 0]
np.unravel_index(X.argmax(), X.shape)   # (1, 0)
```

## Common mistakes
* Mixing up axis 0 and 1 (remember: the named axis is the one removed).
* Using flat `argmax()` and treating it as a row index.
* Forgetting `keepdims` and then failing to broadcast.

## Why this matters
Per-feature means for scaling (ML-08), per-sample predicted classes (`argmax(axis=1)`), batch
statistics in batch norm (DL-23) — all are axis reductions.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
