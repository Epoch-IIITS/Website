# Mean and Variance

## Learning outcomes

After this lesson you can:

- Compute mean and variance
- Distinguish population (N) and sample (N−1) variance
- Relate variance and standard deviation

## Intuition
The mean tells you where the data is centred; the variance tells you how spread out it is
around that centre. Variance is the average squared distance from the mean.

## Precise explanation
For data $x_1,\dots,x_n$ with mean $\bar x = \frac1n\sum x_i$:
* **Population variance** (the data *is* the whole population):
  $\sigma^2 = \frac{1}{n}\sum (x_i-\bar x)^2$.
* **Sample variance** (the data is a sample used to estimate a larger population):
  $s^2 = \frac{1}{n-1}\sum (x_i-\bar x)^2$. Dividing by $n-1$ (Bessel's correction) makes the
  estimate unbiased, because deviations from the *sample* mean are slightly too small on average.
* Standard deviation = square root of variance, in the original units.

Python's `statistics.pvariance` uses $n$, `statistics.variance` uses $n-1$; NumPy's `np.var`
defaults to $n$ (`ddof=0`) — a frequent source of mismatched results.

The two-pass method (compute the mean, then sum squared deviations) is numerically safer than
the textbook shortcut $\overline{x^2} - \bar x^2$, which can lose precision or even go negative.

## Worked example
Data 2, 4, 4, 4, 5, 5, 7, 9: mean 5; squared deviations 9,1,1,1,0,0,4,16 sum 32.
Population variance 32/8 = 4 (sd 2). Sample variance 32/7 ≈ 4.571.

## Common mistakes
* Mixing $n$ and $n-1$ between libraries.
* Computing sample variance of a single value (division by zero — it is undefined).
* Forgetting to square deviations (they sum to zero).

## Why this matters
Variance drives feature standardisation (ML-08), batch normalisation (DL-23), confidence
intervals and the bias–variance trade-off.

## Library implementation

The `statistics` module provides `fmean`, `pvariance` (divide by $n$) and `variance` (divide by
$n-1$), plus `pstdev`/`stdev`. They use exact arithmetic internally where possible, so tiny
differences from your loop are rounding only.

## References

- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
