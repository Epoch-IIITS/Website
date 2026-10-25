# Matrix Products with @

## Learning outcomes

After this lesson you can:

- Multiply matrices and matrix–vector pairs with the @ operator
- Predict result shapes and catch mismatches before multiplying
- Score a whole batch of examples with one product
- Verify @ against the triple loop from Mathematics

## Intuition
MA-06 computed each entry of $AB$ as a dot product of a row of $A$ with a column of
$B$ using three nested loops. NumPy's `@` operator does the same in one expression and is the
most important operation in machine learning: a linear model scores a whole batch of examples
with a single `X @ w`.

## Precise explanation
For $A$ of shape $(m, n)$ and $B$ of shape $(n, p)$, $C = AB$ has shape $(m, p)$ and
$C_{ij} = \sum_{k} A_{ik} B_{kj}$. The inner dimensions must match.

| Expression | Shapes | Result |
|---|---|---|
| `A @ B` | (m, n) @ (n, p) | (m, p) |
| `A @ v` | (m, n) @ (n,) | (m,) — each row dotted with v |
| `v @ w` | (n,) @ (n,) | scalar — the dot product |
| `X @ X.T` | (m, n) @ (n, m) | (m, m) — all pairwise dot products (the Gram matrix) |

* `A * B` is **element-wise**, not matrix multiplication.
* `np.dot` gives the same results for 1-D and 2-D arrays; `@` is the modern, clearer spelling.
* `.T` transposes a 2-D array.
* **Linear model on a batch**: rows of `X` are examples, `w` holds one weight per feature, and
  `X @ w + b` gives one score per example.

## Worked example
```python
A = np.array([[1, 2], [3, 4]]); B = np.array([[5, 6], [7, 8]])
A @ B        # [[19, 22], [43, 50]]
A * B        # [[ 5, 12], [21, 32]]  — different!
X = np.array([[1., 2.], [3., 4.], [5., 6.]]); w = np.array([0.5, -1.0])
X @ w + 0.1  # [-1.4, -2.4, -3.4]
```

## Common mistakes
* Using `*` when you meant `@`.
* Multiplying `(3, 2) @ (3, 2)`; you probably needed a transpose.
* Confusing a 1-D vector `(n,)` with a column `(n, 1)`; `X @ w` with `w` of shape `(n, 1)` returns
  shape `(m, 1)`, not `(m,)`.

## Why this matters
Dense layers (DL-04), attention (LM-07) and least squares are all
matrix products.

## Library implementation

`@` calls `np.matmul`; `np.dot` and `np.einsum("ik,kj->ij", A, B)` are equivalent spellings for
2-D arrays. NumPy hands large products to an optimised BLAS library, which is why `@` is far
faster than the triple loop. The tests check all three spellings agree with your function.

## References

- [numpy.matmul (NumPy v2.5 Manual)](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) — NumPy Developers (`S082`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
