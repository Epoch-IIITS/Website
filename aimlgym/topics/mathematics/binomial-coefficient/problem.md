# MA-07 · Binomial Coefficient

**Topic:** Mathematics for AI/ML · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** MA-01 Summation and Product Notation, PY-19 Validated Factorial

Read the lesson first: [article.md](article.md)

## Task

Write `comb(n, k)` returning $\binom{n}{k}$ as an exact `int` without using `math.comb` or
`math.factorial`.

* Return `0` if `k > n`.
* Raise `ValueError` if `n < 0` or `k < 0`.

**Constraints:** 0 ≤ n ≤ 2000.

**Examples**
```python
comb(5, 2)    # 10
comb(5, 0)    # 1
comb(3, 5)    # 0  — cannot choose 5 from 3
comb(60, 30)  # 118264581564861424  — exact integer
```

## Hints

<details><summary>Hint 1</summary>

Handle negatives (raise) and `k > n` (return 0) first.

</details>

<details><summary>Hint 2</summary>

Replace `k` by `min(k, n - k)`.

</details>

<details><summary>Hint 3</summary>

Loop `for i in range(1, k + 1): r = r * (n - k + i) // i`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_large_exact` | Use integer `//` after multiplying, never `/`. |
| `test_k_greater` | Return 0 when k > n. |
| `test_edges` | C(n, 0) = C(n, n) = 1; check your loop for k = 0. |
| `test_pascal_rule` | If small values are right but some are off by rounding, divide after multiplying. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

After the edge cases, symmetry halves the work. Multiplying before the integer division keeps
the intermediate value an exact product of consecutive binomial coefficients, so `//` never
truncates. Python's arbitrary-precision ints keep large results exact.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
