# Permutation Test with SciPy

## Learning outcomes

After this lesson you can:

- Run scipy.stats.permutation_test with a custom statistic
- Write a vectorised statistic that accepts an axis argument
- Make resampling results reproducible with a seed

## Intuition
If the group labels did not matter, shuffling them should not change the difference in means
much. A permutation test shuffles the labels many times and asks how often a shuffled difference
is at least as extreme as the real one. No normal distribution is assumed.

## Precise explanation
```python
from scipy import stats

def mean_diff(a, b, axis):
    return a.mean(axis=axis) - b.mean(axis=axis)

result = stats.permutation_test((x, y), mean_diff, permutation_type="independent",
                                n_resamples=9999, alternative="two-sided", random_state=0)
result.statistic, result.pvalue
```

* `data` is a tuple of samples; `permutation_type="independent"` reassigns values between groups.
* The statistic receives the samples as arrays (NumPy arrays, the subject of the next topic)
  and an `axis` keyword. `a.mean(axis=axis)` averages along that axis, which lets SciPy evaluate
  many shuffles in one call (`vectorized=True` is assumed when the function accepts `axis`).
* When `n_resamples` is at least the number of distinct relabellings, SciPy enumerates all of
  them and the p-value is **exact**; otherwise it samples randomly, so pass a seed as
  `random_state`.
* `alternative` works as in ST-17.

## Worked example
x = [1, 2, 3, 4, 5], y = [3, 4, 5, 6, 7.5]: the observed difference is −2.1. There are only
C(10, 5) = 252 ways to split ten values into two groups of five, so with `n_resamples=9999` SciPy
checks all of them; 32 of 252 splits give a difference at least 2.1 in size, p = 0.127.

## What the library does inside
It is the loop from ST-20 (the optional deep dive after this step) — shuffle,
recompute, count — written with arrays so that thousands of shuffles are computed at once, plus
exact enumeration for small samples.

## Common mistakes
* Writing a statistic without the `axis` argument, so it silently averages over the wrong axis.
* Leaving out `random_state` and getting a different p-value every run.
* Using `permutation_type="samples"` (paired data) for two independent groups.

## Why this matters
Resampling tests let you compare model metrics, A/B groups or feature effects without assuming
normal errors — and SciPy's version is fast enough to run inside an evaluation pipeline.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
