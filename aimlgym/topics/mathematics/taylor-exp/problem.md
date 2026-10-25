# MA-15 · Taylor Series for exp(x)

**Topic:** Mathematics for AI/ML · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** MA-11 Derivative Rules and the Chain Rule, MA-07 Binomial Coefficient

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `exp_taylor(x, n_terms)` — sum of the first `n_terms` terms ($k = 0..n_\text{terms}-1$).
  `n_terms = 0` returns `0.0`. Raise `ValueError` if `n_terms < 0`.
* `terms_needed(x, tol)` — the smallest `n` such that the magnitude of term $t_n$ (the first
  term *not* included) is `< tol`. Raise `ValueError` if `tol <= 0`.

Compute terms recursively (`t = t * x / k`), not with `math.factorial`.

**Examples**
```python
exp_taylor(1.0, 5)     # 2.708333333...
exp_taylor(0.0, 3)     # 1.0
terms_needed(1.0, 1e-3)  # 7   — t_7 = 1/5040 ≈ 1.98e-4 is the first term below 1e-3
```

## Hints

<details><summary>Hint 1</summary>

Start `term = 1.0`, `total = 0.0`; for k in range(n_terms): add term, then update.

</details>

<details><summary>Hint 2</summary>

Update rule: `term *= x / (k + 1)`.

</details>

<details><summary>Hint 3</summary>

For terms_needed: start n = 0, t = 1.0, and loop while `abs(t) >= tol`: n += 1; t *= x / n.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_five_terms` | Five terms means k = 0..4, starting with the constant 1. |
| `test_terms_needed` | n counts included terms; stop when the next term t_n is below tol. |
| `test_large_terms_no_overflow` | Build terms recursively; math.factorial(500) * float overflows. |
| `test_x_zero` | With x = 0 only the first term (1) is non-zero. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Both functions keep the current term and multiply it by x/k to get the next one, which is exact
algebra and avoids huge factorials. `terms_needed` advances until the first omitted term is below
the tolerance and reports how many terms were included.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
