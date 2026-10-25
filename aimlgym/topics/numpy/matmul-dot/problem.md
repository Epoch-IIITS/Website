# NP-06 · Matrix Products with @

**Topic:** NumPy · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** NP-05 Aggregations Along Axes, MA-06 Matrix Multiplication

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `matmul_loops(A, B)` — nested-list product with three loops (as in MA-06);
   raise `ValueError` if inner dimensions differ. Return a list of lists.
2. `matmul(A, B)` — `np.asarray` both and return `A @ B`; raise `ValueError` with a message
   containing both shapes if the inner dimensions differ (check before multiplying; both
   inputs are 2-D).
3. `batch_scores(X, w, b)` — scores `X @ w + b` for a 2-D `X`, 1-D `w` and a number `b`.
4. `gram(X)` — `X @ X.T`.

**Examples**
```python
matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])   # array([[19, 22], [43, 50]])
batch_scores([[1, 2], [3, 4], [5, 6]], [0.5, -1.0], 0.1)   # array([-1.4, -2.4, -3.4])
```

## Hints

<details><summary>Hint 1</summary>

Loops: for each i (rows of A) and j (columns of B), sum `A[i][k] * B[k][j]` over k.

</details>

<details><summary>Hint 2</summary>

`if A.shape[1] != B.shape[0]: raise ValueError(f"cannot multiply {A.shape} by {B.shape}")`.

</details>

<details><summary>Hint 3</summary>

`np.asarray(X, dtype=float) @ np.asarray(w, dtype=float) + b`; `X @ X.T` for the Gram matrix.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_loops_match_numpy` | Entry (i, j) is the sum over k of A[i][k] * B[k][j]. |
| `test_not_elementwise` | Use `@` (matrix product), not `*` (element-wise). |
| `test_shape_error` | Check `A.shape[1] != B.shape[0]` and include both shapes in the message. |
| `test_batch_scores` | Compute `X @ w + b` with float arrays. |
| `test_gram` | The Gram matrix is `X @ X.T`, shape (rows, rows). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The loop version spells out $C_{ij} = \sum_k A_{ik}B_{kj}$; `@` performs the same computation in
compiled code. Checking `A.shape[1] == B.shape[0]` first produces a clear message. Scoring a batch
is one matrix–vector product plus a broadcast scalar, and the Gram matrix collects every pairwise
dot product of the rows.

## References

- [numpy.matmul (NumPy v2.5 Manual)](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html) — NumPy Developers (`S082`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
