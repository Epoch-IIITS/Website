# ST-18 · Welch's t-statistic by Hand

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** ST-12 Sampling Distributions and Standard Error

Read the lesson first: [article.md](article.md)

## Task

Write `welch_t(x, y)` returning `(t, df)` as floats.

* Both samples need at least 2 values, else `ValueError`.
* If both sample variances are 0, raise `ValueError` (standard error is zero).

**Examples**
```python
welch_t([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])   # (-2.0, 8.0)
welch_t([10, 12, 14], [1, 2, 3, 4, 5, 6])   # (≈ 6.140, ≈ 3.839)
```

## Hints

<details><summary>Hint 1</summary>

Write `_mean_var(a)` returning the mean and sample variance.

</details>

<details><summary>Hint 2</summary>

`vx = sx2 / nx`, `vy = sy2 / ny`, `t = (mx - my) / math.sqrt(vx + vy)`.

</details>

<details><summary>Hint 3</summary>

`df = (vx + vy) ** 2 / (vx ** 2 / (nx - 1) + vy ** 2 / (ny - 1))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_symmetric_example` | Use sample variances (n − 1) divided by each sample size. |
| `test_unequal` | Do not pool variances; Welch keeps them separate. |
| `test_one_zero_variance_ok` | Only raise when *both* variances are zero. |
| `test_too_small` | Each sample needs n ≥ 2. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each group's squared standard error of the mean is its sample variance over its size. Their sum
is the variance of the difference in means; t divides the observed difference by its square
root. The Welch–Satterthwaite formula combines the two contributions into an effective df.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
