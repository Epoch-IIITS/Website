# MA-09 · Inverse of a 2x2 Matrix

**Topic:** Mathematics for AI/ML · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** MA-08 Solve a 2x2 System (Cramer's Rule)

Read the lesson first: [article.md](article.md)

## Task

Write `inverse_2x2(A, tol=1e-12)` returning the inverse of a 2×2 matrix as a list of rows of
floats. Raise `ValueError` if `|det A| < tol` or if `A` is not 2×2.

**Examples**
```python
inverse_2x2([[4, 7], [2, 6]])   # [[0.6, -0.7], [-0.2, 0.4]]
inverse_2x2([[2, 4], [1, 2]])   # raises ValueError — det = 0
```

## Hints

<details><summary>Hint 1</summary>

Unpack `(a, b), (c, d) = A` and compute `det = a*d - b*c`.

</details>

<details><summary>Hint 2</summary>

Raise ValueError if `abs(det) < tol`.

</details>

<details><summary>Hint 3</summary>

Return `[[d/det, -b/det], [-c/det, a/det]]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Swap the diagonal entries and negate the off-diagonal ones. |
| `test_product_is_identity` | Divide every entry by the determinant. |
| `test_singular` | Raise ValueError when |det| < tol. |
| `test_bad_shape` | Check A has exactly two rows of length two. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The adjugate formula is applied directly after shape and singularity checks. Dividing each entry
by the determinant produces floats.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
