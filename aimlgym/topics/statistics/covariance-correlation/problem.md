# ST-11 · Covariance and Pearson Correlation

**Topic:** Statistics · **Difficulty:** intermediate · **Allowed packages:** standard library only

**Builds on:** ST-05 Standardize to z-scores, MA-04 Dot Product

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `covariance(x, y, sample=True)` — raise `ValueError` if lengths differ, or there are fewer
  than 2 points (sample) / 1 point (population).
* `pearson(x, y)` — raise `ValueError` if lengths differ, `n < 2`, or either variable is constant.

**Examples**
```python
covariance([1, 2, 3, 4], [2, 4, 5, 8])   # 3.1666666666666665
pearson([1, 2, 3, 4], [2, 4, 5, 8])      # 0.9811...
pearson([1, 2, 3], [3, 2, 1])            # -1.0
```

## Hints

<details><summary>Hint 1</summary>

Compute both means, then `sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))`.

</details>

<details><summary>Hint 2</summary>

Covariance = `sxy / (n - 1)` (sample) or `/ n`.

</details>

<details><summary>Hint 3</summary>

r = `sxy / math.sqrt(sxx * syy)`; raise if `sxx` or `syy` is 0.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_cov` | Sample covariance divides the sum of deviation products by n − 1. |
| `test_nonlinear_zero` | r measures linear association only; y = x² on symmetric x gives 0. |
| `test_constant_raises` | A constant variable has zero spread — raise ValueError. |
| `test_scale_invariance` | Centre both variables before multiplying deviations. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A shared helper computes the centred cross- and self-sums once. Covariance divides the cross-sum
by n or n−1; Pearson's r normalises it by the geometric mean of the self-sums, so the denominator
choice cancels. Constant variables make the denominator zero and are rejected.

## References

- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
