# Welch's t-test with SciPy

## Learning outcomes

After this lesson you can:

- Compare two means with scipy.stats.ttest_ind(equal_var=False)
- Choose a two-sided or one-sided alternative
- Report the mean difference alongside the p-value

## Intuition
Two groups have different averages. Is the gap larger than the noise in each group would
produce? The t-statistic measures the gap in units of its standard error; the p-value asks how
often chance alone would give a t at least that extreme.

## Precise explanation
```python
from scipy import stats
result = stats.ttest_ind(x, y, equal_var=False)       # Welch's test
result.statistic, result.pvalue, result.df
```

`equal_var=False` selects **Welch's** test: each group keeps its own variance, and the degrees of
freedom come from the Welch–Satterthwaite formula (usually not an integer). The default,
`equal_var=True`, is Student's test, which pools the variances and can be badly wrong when the
spreads or sizes differ — so always ask for Welch unless you have a reason not to.

`alternative` states the question:

| `alternative` | Null hypothesis rejected when … |
|---|---|
| `"two-sided"` | the means differ in either direction |
| `"greater"` | mean(x) > mean(y) |
| `"less"` | mean(x) < mean(y) |

A one-sided p-value is half the two-sided one when the difference points the hypothesised way.

## Worked example
x = [1, 2, 3, 4, 5] and y = [3, 4, 5, 6, 7]: t = −2, df = 8, two-sided p ≈ 0.081. Not
significant at α = 0.05; with `alternative="less"`, p ≈ 0.040 and it is. Decide the alternative
**before** looking at the data — switching afterwards halves p dishonestly.

## What the library does inside
SciPy computes the same standard error, t and degrees of freedom as ST-18 (the optional
deep dive after this step), then reads the p-value from the t distribution's tails with `stats.t`.

## Common mistakes
* Leaving `equal_var=True` (Student's test) when group variances differ.
* Reporting only "p < 0.05" without the size of the difference.
* Picking the one-sided alternative after seeing which mean is larger.
* Using it on paired measurements (before/after on the same people): that is `ttest_rel`.

## Why this matters
Comparing two model variants across random seeds, or an A/B test of two page designs, ends with
exactly this test — and the mean difference tells you whether the effect is worth acting on.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
