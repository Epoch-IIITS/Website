# Group-wise Imputation

## Learning outcomes

After this lesson you can:

- Detect missing values
- Impute with group means via transform
- Fall back to a global statistic

## Intuition
A missing height is better guessed from people of the same age group than from everyone. Filling
NaN with a **group** mean keeps more structure than a single global mean.

## Precise explanation
* `s.isna()` marks missing values; `s.isna().sum()` counts them.
* `df.groupby(g)[col].transform("mean")` returns a Series **aligned with the original rows**: each
  row gets its own group's mean (unlike `agg`, which returns one row per group).
* `s.fillna(other)` replaces NaN positions with the matching values of `other`.
* If a whole group is missing, its group mean is NaN; fall back to the global mean
  `s.mean()` (NaN skipped).

## Worked example
g = [a, a, b, b, c], v = [1, NaN, 10, 20, NaN]:
group means a 1, b 15, c NaN; global mean (1+10+20)/3 ≈ 10.33 →
filled [1, 1, 10, 20, 10.33].

## Common mistakes
* Using `agg` and trying to align by position.
* Computing means *after* filling (leaks filled values into statistics).
* In ML, computing imputation statistics on the full dataset instead of the training split
  (data leakage; see ML-08).

## Why this matters
Real data has holes; principled imputation (and recording which values were imputed) is a core
preprocessing step.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
