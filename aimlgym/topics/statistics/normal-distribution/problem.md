# ST-09 · The Normal Distribution

**Topic:** Statistics · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** ST-05 Standardize to z-scores, ST-08 Binomial Probabilities

Read the lesson first: [article.md](article.md)

## Task

Implement with `math` only:

1. `normal_pdf(x, mu=0.0, sigma=1.0)` and 2. `normal_cdf(x, mu=0.0, sigma=1.0)` from the formulas
   above; raise `ValueError` if `sigma <= 0`.
3. `prob_between(a, b, mu=0.0, sigma=1.0)` → $F(b) - F(a)$ (raise `ValueError` if `b < a`).
4. `empirical_rule()` → `{1: p1, 2: p2, 3: p3}`, the probabilities of lying within 1, 2, 3
   standard deviations of the mean.
5. `binomial_cdf_approx(k, n, p)` → normal approximation of $P(X \le k)$ for
   $X \sim \text{Bin}(n, p)$ with the continuity correction.

**Examples**
```python
normal_cdf(0)                    # 0.5
prob_between(160, 180, 170, 10)  # ≈ 0.6827
empirical_rule()[2]              # ≈ 0.9545
binomial_cdf_approx(55, 100, 0.5)  # ≈ 0.8643
```

## Hints

<details><summary>Hint 1</summary>

pdf: `math.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))`.

</details>

<details><summary>Hint 2</summary>

cdf: `0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))`.

</details>

<details><summary>Hint 3</summary>

The empirical rule is `prob_between(-k, k)` for k = 1, 2, 3.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_pdf` | Divide by `sigma * sqrt(2*pi)` and square `(x - mu)` inside the exponent. |
| `test_cdf` | Use `0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))`. |
| `test_empirical_rule` | Return a dict keyed by 1, 2 and 3 with `prob_between(-k, k)`. |
| `test_invalid_sigma` | Raise ValueError when sigma <= 0. |
| `test_binomial_approx_close_to_exact` | Use mean n*p, standard deviation sqrt(n*p*(1-p)) and evaluate at k + 0.5. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The density and cdf are direct translations of their formulas; the cdf relies on `math.erf`,
which the standard library computes accurately. Interval probabilities are differences of the
cdf, the empirical rule reuses that on the standard normal, and the binomial approximation plugs
the binomial mean and standard deviation into the normal cdf at $k + 0.5$.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
