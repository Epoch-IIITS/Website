# Chi-Square Test with SciPy

## Learning outcomes

After this lesson you can:

- Run a goodness-of-fit test with scipy.stats.chisquare
- Interpret a p-value and compare it with a significance level
- Relate the p-value to the chi-square distribution's upper tail

## Intuition
A chi-square statistic says how far observed counts are from expected counts. On its own, 13.4
means little. The **p-value** turns it into a probability: if the hypothesised probabilities were
right, how often would random counts look at least this far off?

## Precise explanation
`scipy.stats.chisquare(f_obs, f_exp)` returns the statistic $\chi^2 = \sum (O_i - E_i)^2 / E_i$
and its p-value with $k - 1$ degrees of freedom:

```python
from scipy import stats
result = stats.chisquare([5, 8, 9, 8, 10, 20], f_exp=[10] * 6)
result.statistic   # 13.4
result.pvalue      # 0.0199
```

`f_exp` must be **counts** with the same total as `f_obs` (multiply probabilities by the total);
omitting it means "all categories equally likely". The p-value is the chi-square distribution's
upper tail, `stats.chi2(df).sf(statistic)`. With significance level α, reject the null hypothesis
when p < α. A p-value is **not** the probability that the null hypothesis is true.

## Worked example
For the die above, p ≈ 0.020. At α = 0.05 we reject fairness; at α = 0.01 we do not. The
evidence is the same; the decision depends on how strict the threshold is.

## What the library does inside
`chisquare` computes the same sum as your function in ST-16, which follows as an
optional deep dive, then calls the chi-square survival function instead of reading a table of
critical values. It also checks that observed and expected totals agree.

## Common mistakes
* Passing probabilities as `f_exp`: SciPy expects expected counts.
* Using proportions instead of counts for `f_obs`; the test needs the sample size.
* Rejecting when p > α, or reading 1 − p as the probability the hypothesis is false.
* Testing categories with expected counts below about 5, where the approximation is poor.

## Why this matters
Chi-square tests check whether class frequencies drifted between training and production data,
whether a random-number generator is uniform, and whether a feature's categories relate to labels.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
