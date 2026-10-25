# MA-08 · Solve a 2x2 System (Cramer's Rule)

**Topic:** Mathematics for AI/ML · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** MA-06 Matrix Multiplication

Read the lesson first: [article.md](article.md)

## Task

Write `solve_2x2(A, b, tol=1e-12)` where `A = [[a, b], [c, d]]` and `b = [e, f]`.

* Return the solution `(x, y)` as floats.
* Raise `ValueError("singular")` if `abs(det) < tol`.
* Raise `ValueError` if `A` is not 2×2 or `b` does not have length 2.

**Examples**
```python
solve_2x2([[2, 1], [1, -1]], [5, 1])   # (2.0, 1.0)
solve_2x2([[1, 2], [2, 4]], [3, 6])    # raises ValueError — parallel lines (det = 0)
```

## Hints

<details><summary>Hint 1</summary>

Unpack: `(a, b_), (c, d) = A` and `e, f = b` after checking shapes.

</details>

<details><summary>Hint 2</summary>

`det = a * d - b_ * c`; raise if `abs(det) < tol`.

</details>

<details><summary>Hint 3</summary>

`x = (e * d - b_ * f) / det`, `y = (a * f - e * c) / det`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Check the determinant ad − bc and which numerator belongs to x vs y. |
| `test_near_singular_tolerance` | Compare abs(det) < tol, not det == 0. |
| `test_residual` | Substitute your answer back into both equations to debug. |
| `test_bad_shape` | Validate that A is 2×2 and b has two entries. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The function validates shapes, computes the determinant, and treats tiny determinants as
singular using a tolerance. Cramer's rule then gives each unknown as a ratio of determinants.
The variable is named `b12` to avoid clashing with the right-hand-side vector `b`.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
