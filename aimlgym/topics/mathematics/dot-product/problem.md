# MA-04 · Dot Product

**Topic:** Mathematics for AI/ML · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** MA-01 Summation and Product Notation

Read the lesson first: [article.md](article.md)

## Task

Write `dot(u, v)` returning the dot product of two equal-length lists of numbers.

* Raise `ValueError` if the lengths differ.
* The dot product of two empty vectors is `0`.
* Do not use NumPy.

**Examples**
```python
dot([1, 2, 3], [4, -5, 6])   # 12
dot([1, 0], [0, 1])          # 0   — perpendicular
dot([1, 2], [1, 2, 3])       # raises ValueError
```

## Hints

<details><summary>Hint 1</summary>

Compare `len(u)` and `len(v)` first.

</details>

<details><summary>Hint 2</summary>

`zip(u, v)` pairs up corresponding elements.

</details>

<details><summary>Hint 3</summary>

Accumulate `total += a * b` starting from 0.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_mismatch` | zip stops at the shorter list — check lengths explicitly. |
| `test_empty` | Start the accumulator at 0, not at u[0]*v[0]. |
| `test_floats` | Floats are compared with tolerance 1e-12; return a number. |
| `test_example` | Multiply corresponding elements and add them up. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Length validation protects against `zip` silently truncating. The accumulator starts at 0 (the
additive identity), so empty vectors correctly give 0, and each pair contributes its product.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
