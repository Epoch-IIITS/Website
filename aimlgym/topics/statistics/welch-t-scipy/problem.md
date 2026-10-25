# ST-17 · Welch's t-test with SciPy

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** numpy, scipy

**Builds on:** ST-15 Chi-Square Test with SciPy, ST-12 Sampling Distributions and Standard Error

Read the lesson first: [article.md](article.md)

## Task

Write `compare_means(x, y, alternative="two-sided", alpha=0.05)` returning
`{"mean_diff": float, "t": float, "df": float, "p_value": float, "reject": bool}` where
`mean_diff = mean(x) - mean(y)` and `reject` is `p_value < alpha`.

* Use `scipy.stats.ttest_ind` with `equal_var=False` and the given `alternative`.
* Raise `ValueError` if either sample has fewer than 2 values, both samples have zero variance,
  `alternative` is not one of `"two-sided"`, `"less"`, `"greater"`, or `alpha` is not in (0, 1).

**Examples**
```python
compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
# {'mean_diff': -2.0, 't': -2.0, 'df': 8.0, 'p_value': 0.0805..., 'reject': False}
compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="less")["reject"]   # True
```

## Hints

<details><summary>Hint 1</summary>

Check the sizes, the alternative and alpha; compute each sample's variance to reject the all-constant case.

</details>

<details><summary>Hint 2</summary>

`result = stats.ttest_ind(x, y, equal_var=False, alternative=alternative)`.

</details>

<details><summary>Hint 3</summary>

`result.df` holds the Welch degrees of freedom; convert everything with float().

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_symmetric_example` | Call ttest_ind with equal_var=False; read t, df and p from the result. |
| `test_one_sided_halves_p` | Pass alternative through to SciPy. |
| `test_welch_not_student` | equal_var=False gives Welch's test; the default pools variances. |
| `test_invalid_inputs` | Raise ValueError for tiny or constant samples, a bad alternative or alpha. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`ttest_ind(..., equal_var=False)` is Welch's test; the alternative is passed straight through.
SciPy would return `nan` when both samples are constant, so that case is rejected first. The mean
difference is reported because a p-value alone says nothing about how large the effect is.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
