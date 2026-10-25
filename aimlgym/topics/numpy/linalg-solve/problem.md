# NP-12 · Solve Linear Systems Safely

**Topic:** NumPy · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** NP-06 Matrix Products with @, MA-08 Solve a 2x2 System (Cramer's Rule)

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `solve(A, b, max_cond=1e12)` → solution of square `A x = b`. Raise `ValueError` if `A` is not
  square, sizes mismatch, or `np.linalg.cond(A) > max_cond` (this also covers singular matrices,
  whose condition number is infinite or huge).
* `residual_norm(A, x, b)` → float `‖A x − b‖₂`.
* `fit_line(x, y)` → `(intercept, slope)` floats using `np.linalg.lstsq` on `[1, x]`.
  Raise `ValueError` for fewer than 2 points or mismatched lengths.

**Examples**
```python
solve(np.array([[3., 1.], [1., 2.]]), np.array([9., 8.]))   # array([2., 3.])
fit_line([0, 1, 2], [1, 3, 5])                               # (1.0, 2.0)
solve(np.array([[1., 2.], [2., 4.]]), np.array([1., 2.]))    # raises ValueError
```

## Hints

<details><summary>Hint 1</summary>

Check `A.ndim == 2 and A.shape[0] == A.shape[1] == len(b)`.

</details>

<details><summary>Hint 2</summary>

Compute `np.linalg.cond(A)` before calling `np.linalg.solve`.

</details>

<details><summary>Hint 3</summary>

`X = np.column_stack([np.ones(len(x)), x]); w, *_ = np.linalg.lstsq(X, y, rcond=None)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_singular` | Check np.linalg.cond(A) (inf or huge for singular matrices) before solving. |
| `test_fit_line` | Include a column of ones for the intercept; return (intercept, slope). |
| `test_fit_line_noisy` | Use np.linalg.lstsq(X, y, rcond=None). |
| `test_residual` | Residual is the 2-norm of A@x − b, as a Python float. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`solve` validates shapes and refuses ill-conditioned systems before factorising. The residual is
a direct norm. `fit_line` builds the design matrix with an intercept column and lets `lstsq`
minimise the squared residual.

## References

- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
