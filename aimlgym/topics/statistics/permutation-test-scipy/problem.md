# ST-19 · Permutation Test with SciPy

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** scipy

**Builds on:** ST-17 Welch's t-test with SciPy

Read the lesson first: [article.md](article.md)

## Task

Write `permutation_mean_diff(x, y, alternative="two-sided", n_resamples=9999, seed=0)` returning
`{"statistic": float, "p_value": float}` for the difference in means `mean(x) - mean(y)`.

* Use `scipy.stats.permutation_test` with `permutation_type="independent"`, a statistic that
  accepts `axis`, and `random_state=seed`.
* Raise `ValueError` if either sample is empty or `alternative` is invalid.

**Examples**
```python
permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5])
# {'statistic': -2.1, 'p_value': 0.1269...}   (exact: all 252 splits are checked)
```

## Hints

<details><summary>Hint 1</summary>

Define `def mean_diff(a, b, axis): return a.mean(axis=axis) - b.mean(axis=axis)`.

</details>

<details><summary>Hint 2</summary>

Call `stats.permutation_test((x, y), mean_diff, permutation_type="independent", ...)`.

</details>

<details><summary>Hint 3</summary>

Pass `n_resamples`, `alternative` and `random_state=seed`; return floats.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_exact_small_sample` | Use permutation_type='independent' and a statistic of mean(x) - mean(y). |
| `test_one_sided` | Pass the alternative through to permutation_test. |
| `test_reproducible_with_seed` | Pass random_state=seed. |
| `test_invalid_inputs` | Raise ValueError for empty samples and unknown alternatives. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The statistic takes an `axis` so SciPy can evaluate many relabellings at once. For small samples
SciPy enumerates every split, giving an exact p-value; for larger ones the seed makes the random
resamples reproducible.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
