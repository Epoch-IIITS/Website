# MA-02 · Exponentials and Logarithms

**Topic:** Mathematics for AI/ML · **Difficulty:** beginner · **Allowed packages:** standard library only

**Builds on:** MA-01 Summation and Product Notation

Read the lesson first: [article.md](article.md)

## Task

Implement with the `math` module:

1. `log_base(x, base)` — $\log_{base} x$ via the change-of-base rule (use `math.log(x)` only).
2. `doubling_time(rate)` — $\ln 2 / \ln(1 + rate)$.
3. `log_likelihood(probs)` — $\sum \ln p_i$; raise `ValueError` if any $p \le 0$ or $p > 1$.
   It must work for 1000 probabilities of `1e-5` (where the plain product underflows).
4. `logsumexp(values)` — the stable form $m + \ln\sum e^{v_i - m}$; raise `ValueError` for an
   empty list.

**Examples**
```python
log_base(8, 2)                 # 3.0 (within rounding)
doubling_time(0.07)            # ≈ 10.24
log_likelihood([0.5, 0.25])    # ln(0.125) ≈ -2.0794
logsumexp([1000, 1000])        # ≈ 1000.6931
```

## Hints

<details><summary>Hint 1</summary>

`math.log(x) / math.log(base)`; `math.log(2) / math.log(1 + rate)`.

</details>

<details><summary>Hint 2</summary>

Loop over the probabilities, check `0 < p <= 1`, and add `math.log(p)`.

</details>

<details><summary>Hint 3</summary>

`m = max(values)`, then `m + math.log(sum(math.exp(v - m) for v in values))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_log_base` | Divide `math.log(x)` by `math.log(base)`. |
| `test_log_likelihood_no_underflow` | Add logs one by one instead of taking the log of the product. |
| `test_log_likelihood_validates` | Raise ValueError for any p that is not in (0, 1]. |
| `test_logsumexp_large_and_negative` | Subtract the maximum before exponentiating and add it back after the log. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The change-of-base and doubling formulas are direct translations. The log-likelihood never forms
the tiny product, so it cannot underflow, and invalid probabilities are rejected before taking
logs. Subtracting the maximum in log-sum-exp makes the largest exponent exactly 1, so the sum is
between 1 and n and its logarithm is always finite.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
