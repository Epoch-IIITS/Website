# ST-13 · Bootstrap Confidence Interval

**Topic:** Statistics · **Difficulty:** advanced · **Allowed packages:** standard library only

**Builds on:** ST-12 Sampling Distributions and Standard Error, ST-03 Percentiles by Linear Interpolation

Read the lesson first: [article.md](article.md)

## Task

Write `bootstrap_ci(data, n_boot=2000, alpha=0.05, seed=0, stat=None)` returning `(low, high)`.

* `stat` is a function of a list; default is the mean.
* `rng = random.Random(seed)`. For each of `n_boot` resamples, draw `len(data)` indices
  `int(rng.random() * n)` in order.
* Endpoints: percentiles `100*alpha/2` and `100*(1-alpha/2)` of the bootstrap statistics using
  the **linear-interpolation** definition from ST-03.
* Raise `ValueError` if `data` is empty, `n_boot < 1`, or `alpha` not in `(0, 1)`.

**Examples**
```python
lo, hi = bootstrap_ci([2, 4, 4, 5, 7, 9], seed=0)
lo < sum([2, 4, 4, 5, 7, 9]) / 6 < hi     # True
bootstrap_ci([5, 5, 5], seed=1)           # (5.0, 5.0) — no variability
```

## Hints

<details><summary>Hint 1</summary>

Default `stat = lambda xs: sum(xs) / len(xs)`.

</details>

<details><summary>Hint 2</summary>

Resample: `[data[int(rng.random() * n)] for _ in range(n)]`.

</details>

<details><summary>Hint 3</summary>

Reuse a linear-interpolation percentile helper on the list of bootstrap stats.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_exact_recipe` | Draw indices with int(rng.random()*n), n per resample, in order; sort the stats; use linear percentiles. |
| `test_constant` | Constant data gives identical bootstrap stats; both endpoints equal the value. |
| `test_wider_at_higher_confidence` | Lower alpha → percentiles further into the tails. |
| `test_custom_stat` | Apply the provided stat function to each resample. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each bootstrap replicate resamples n values with replacement using the documented index recipe
and records the statistic. Sorting the replicates and reading off the α/2 and 1−α/2 percentiles
gives the percentile interval.

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
