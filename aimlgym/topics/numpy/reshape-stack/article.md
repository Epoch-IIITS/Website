# Reshaping and Stacking

## Learning outcomes

After this lesson you can:

- Reshape arrays with -1
- Stack and concatenate along axes
- Flatten image batches for linear models

## Intuition
Reshaping reinterprets the same numbers in a different grid (12 numbers as 3×4 or 2×6), like
re-folding a strip of paper. Stacking glues arrays together along an axis.

## Precise explanation
* `a.reshape(r, c)` requires `r*c == a.size`; one dimension may be `-1` meaning "whatever fits".
  Reshape fills in **row-major (C) order** — the last axis varies fastest.
* `np.concatenate([a, b], axis=k)` joins along an existing axis; `np.stack` creates a new axis.
* `np.hstack` / `np.column_stack` join side by side; `np.vstack` on top of each other.
* A batch of images with shape `(N, H, W)` becomes a design matrix `(N, H*W)` with
  `imgs.reshape(N, -1)`.

## Worked example
```python
x = np.arange(10)
x[: (10 // 4) * 4].reshape(-1, 4)     # [[0,1,2,3],[4,5,6,7]] — remainder 8, 9 dropped
np.hstack([np.ones((2, 1)), [[3, 4], [5, 6]]])   # [[1,3,4],[1,5,6]]
```

## Common mistakes
* `reshape(4, -1)` vs `reshape(-1, 4)` — rows vs columns of size 4.
* Using reshape to transpose (it doesn't reorder data; use `.T`).
* Stacking 1-D arrays with `hstack` and getting one long vector instead of columns.

## Why this matters
Mini-batching, adding the intercept column in linear regression (ML-09), flattening images
before a dense layer (DL/CV) and splitting attention heads (LM-10) are reshapes.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
