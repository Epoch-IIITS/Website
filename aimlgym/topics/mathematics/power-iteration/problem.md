# MA-16 · Dominant Eigenvalue by Power Iteration

**Topic:** Mathematics for AI/ML · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** MA-05 Vector Norm and Unit Vector, MA-06 Matrix Multiplication

Read the lesson first: [article.md](article.md)

## Task

Write `power_iteration(A, num_iters=1000, tol=1e-10)` for a square matrix `A` (list of rows) in
pure Python.

* Start from the all-ones vector.
* Each iteration: `w = A b`; if `‖w‖ == 0` raise `ValueError`; `b = w / ‖w‖`;
  `lam = b · (A b)`. Stop when `|lam - previous_lam| < tol`.
* Sign convention: flip `b` so its entry with largest absolute value is positive.
* Return `(lam, b)` with `b` a list of floats of unit length. Tests check `lam` to 1e-8 and
  `b` to 1e-4 (the vector converges more slowly than the eigenvalue).
* Raise `ValueError` if `A` is not square.

**Examples**
```python
power_iteration([[2, 1], [1, 2]])   # (3.0, [0.7071..., 0.7071...])
power_iteration([[4, 0], [0, -1]])  # (4.0, [1.0, 0.0])
```

## Hints

<details><summary>Hint 1</summary>

Write helpers `matvec(A, v)` and `dot(u, v)`.

</details>

<details><summary>Hint 2</summary>

Normalise: `nrm = math.sqrt(dot(w, w)); b = [x / nrm for x in w]`.

</details>

<details><summary>Hint 3</summary>

Track `prev` and compare `abs(lam - prev) < tol`; fix the sign at the end.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_eigen_equation` | Check A·v ≈ λ·v; normalise b every iteration and use the Rayleigh quotient. |
| `test_sign_convention` | Flip b so its largest-magnitude entry is positive. |
| `test_zero_matrix` | Raise ValueError when A·b has zero norm. |
| `test_diagonal_negative` | λ is the dominant eigenvalue by absolute value; here it is 4. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Repeated multiplication amplifies the dominant eigen-direction; normalising each step keeps the
numbers bounded. The Rayleigh quotient of the unit vector estimates the eigenvalue and provides
the stopping test. Finally the sign is fixed (largest-magnitude entry positive) so the
eigenvector is reported reproducibly.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
