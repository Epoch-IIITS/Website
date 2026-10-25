# ST-08 · Binomial Probabilities

**Topic:** Statistics · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** ST-06 Probability by Counting Outcomes, MA-07 Binomial Coefficient

Read the lesson first: [article.md](article.md)

## Task

Implement (you may use `math.comb`):
* `binom_pmf(k, n, p)` → $P(X = k)$; returns `0.0` for `k < 0` or `k > n`.
* `binom_cdf(k, n, p)` → $P(X \le k)$ (0.0 if `k < 0`, 1.0 if `k >= n`).
* `prob_at_least(k, n, p)` → $P(X \ge k)$.

Raise `ValueError` if `n < 0` or `p` is outside `[0, 1]`.

**Examples**
```python
binom_pmf(2, 4, 0.5)      # 0.375
prob_at_least(3, 4, 0.5)  # 0.3125
binom_cdf(10, 10, 0.3)    # 1.0
```

## Hints

<details><summary>Hint 1</summary>

Write a `_check(n, p)` helper that raises ValueError.

</details>

<details><summary>Hint 2</summary>

pmf: `math.comb(n, k) * p**k * (1 - p)**(n - k)` for 0 ≤ k ≤ n.

</details>

<details><summary>Hint 3</summary>

cdf sums pmf for j = 0..min(k, n); at_least = 1 − cdf(k − 1).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_pmf` | Include the C(n, k) factor. |
| `test_at_least` | P(X ≥ k) = 1 − P(X ≤ k − 1), not 1 − P(X ≤ k). |
| `test_out_of_range_k` | Return 0.0 when k is outside 0..n. |
| `test_bad_p` | Validate 0 ≤ p ≤ 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The PMF is the formula directly. The CDF sums PMF terms (returning exact 0/1 at the extremes),
and the upper tail uses the complement rule with k − 1 because P(X ≥ k) excludes k − 1 and below.
`min`/`max` clamp tiny floating-point overshoots outside [0, 1].

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
