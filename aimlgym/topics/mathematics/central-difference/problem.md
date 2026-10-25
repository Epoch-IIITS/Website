# MA-10 · Numerical Derivative (Central Difference)

**Topic:** Mathematics for AI/ML · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** MA-02 Exponentials and Logarithms

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `forward_diff(f, x, h=1e-6)` → $(f(x+h)-f(x))/h$
* `central_diff(f, x, h=1e-5)` → $(f(x+h)-f(x-h))/(2h)$

Both raise `ValueError` if `h <= 0`. `f` is any Python function of one float.

**Examples**
```python
central_diff(lambda x: x**3, 2.0)        # ≈ 12.0  (within 1e-6)
forward_diff(lambda x: x**3, 2.0, h=0.1) # 12.61   (first-order error)
central_diff(lambda x: x**3, 2.0, h=0.1) # 12.01   (second-order error)
```

## Hints

<details><summary>Hint 1</summary>

Validate `h > 0` first.

</details>

<details><summary>Hint 2</summary>

Forward: one extra evaluation at `x + h`.

</details>

<details><summary>Hint 3</summary>

Central: evaluate at `x + h` and `x - h` and divide by `2 * h`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_central_h01` | Divide by 2*h in the central difference. |
| `test_forward_h01` | Forward difference uses f(x+h) − f(x) over h. |
| `test_bad_h` | Raise ValueError when h <= 0. |
| `test_central_more_accurate` | Make sure central_diff evaluates at x−h, not at x. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Both functions translate their formulas directly. The central version evaluates symmetrically
around x, so the leading error term cancels and the estimate is far more accurate for the same h.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
