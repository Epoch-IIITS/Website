# NP-11 · Vectorized Pairwise Distances

**Topic:** NumPy · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** NP-07 Centering Columns with Broadcasting, NP-06 Matrix Products with @

Read the lesson first: [article.md](article.md)

## Task

Implement (no Python loops over points):
* `pairwise_sq_dists(A, B)` → `(m, n)` array of squared Euclidean distances, clipped at 0.
  Raise `ValueError` if the feature dimensions differ or inputs are not 2-D.
* `nearest(A, B)` → for each row of `A`, the index of the closest row of `B` (lowest index on ties).

**Examples**
```python
A = np.array([[0., 0.], [1., 1.]]); B = np.array([[1., 0.], [3., 4.]])
pairwise_sq_dists(A, B)   # [[ 1., 25.], [ 1., 13.]]
nearest(A, B)             # array([0, 0])
```

## Hints

<details><summary>Hint 1</summary>

Row norms: `(A ** 2).sum(axis=1)`, shaped `(m, 1)` and `(1, n)`.

</details>

<details><summary>Hint 2</summary>

`D = aa + bb - 2 * A @ B.T`, then `np.maximum(D, 0)`.

</details>

<details><summary>Hint 3</summary>

`D.argmin(axis=1)` returns the first index on ties.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_against_loops` | Check the sign of the −2·A@B.T term and the transpose. |
| `test_self_zero_diag_nonneg` | Clip with np.maximum(D, 0) to remove rounding negatives. |
| `test_nearest` | argmin along axis=1 gives the nearest B row for each A row. |
| `test_dim_mismatch` | Feature dimensions (columns) must match. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Expanding the squared distance turns the problem into two norm vectors and one matrix product,
combined by broadcasting into an m×n matrix. Clipping removes tiny negative rounding errors.
`argmin` along axis 1 picks the closest reference for each query.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Scientific Python Lectures](https://lectures.scientific-python.org/) — Scientific Python developers (`S006`)
