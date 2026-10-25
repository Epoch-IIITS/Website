# MA-12 · Trapezoidal Integration

**Topic:** Mathematics for AI/ML · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** MA-10 Numerical Derivative (Central Difference)

Read the lesson first: [article.md](article.md)

## Task

Write `trapezoid(f, a, b, n)` implementing the composite trapezoidal rule with `n` equal
sub-intervals. Raise `ValueError` if `n` is not a positive int. Allow `a > b` (negative area) and
`a == b` (returns 0.0).

**Examples**
```python
trapezoid(lambda x: x**2, 0, 1, 2)   # 0.375
trapezoid(lambda x: 3*x + 1, 0, 2, 1)  # 8.0  — exact for straight lines
trapezoid(lambda x: x**2, 1, 0, 2)   # -0.375 — reversed limits
```

## Hints

<details><summary>Hint 1</summary>

`h = (b - a) / n`; the points are `a + i * h` for i = 0..n.

</details>

<details><summary>Hint 2</summary>

Start with `0.5 * (f(a) + f(b))` then add interior points i = 1..n−1.

</details>

<details><summary>Hint 3</summary>

Multiply the total by `h` at the end.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_n2` | Endpoints get weight ½, interior points weight 1, then multiply by h. |
| `test_linear_exact` | With n = 1 the result is h·(f(a)+f(b))/2. |
| `test_error_quarters` | Make sure you include all n−1 interior points. |
| `test_bad_n` | n must be a positive int; reject floats and values < 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The endpoints are weighted by ½ and each interior point by 1, then everything is multiplied by
the strip width h. Points are computed as `a + i*h` to avoid accumulated rounding. A negative h
(for a > b) automatically gives a negative integral.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
