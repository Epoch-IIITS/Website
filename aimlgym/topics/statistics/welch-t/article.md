# Comparing Two Means: Welch's t

## Learning outcomes

After this lesson you can:

- Compute the standard error of a mean difference
- Compute Welch's t and Welch–Satterthwaite df
- Explain why Welch is preferred when variances differ

## Intuition
Model A scores 0.82 on average across runs, model B 0.79. Is A really better, or is the gap just
noise? The t-statistic compares the difference in means to how much that difference would wobble
by chance (its standard error).

## Precise explanation
With sample means $\bar x, \bar y$, sample variances $s_x^2, s_y^2$ (n−1 denominators), sizes
$n_x, n_y$:
$$t = \frac{\bar x - \bar y}{\sqrt{s_x^2/n_x + s_y^2/n_y}}.$$
Welch's test does **not** assume equal variances. Its approximate degrees of freedom
(Welch–Satterthwaite):
$$\nu = \frac{\left(s_x^2/n_x + s_y^2/n_y\right)^2}{\dfrac{(s_x^2/n_x)^2}{n_x-1} + \dfrac{(s_y^2/n_y)^2}{n_y-1}}.$$
Large $|t|$ (compared with a t-distribution with ν df; roughly $|t| > 2$ for moderate ν at 5%)
suggests a real difference. ν is usually not an integer.

## Worked example
x = [1, 2, 3, 4, 5] (mean 3, s² 2.5), y = [3, 4, 5, 6, 7] (mean 5, s² 2.5):
SE = √(0.5 + 0.5) = 1, t = −2, ν = 1/(0.0625 + 0.0625) = 8.

## Common mistakes
* Using population variances.
* Pooling variances (Student's t) when spreads clearly differ.
* Reading "not significant" as "no difference".

## Why this matters
Comparing models across random seeds or cross-validation folds (ML-17) calls for exactly this
kind of test — with care about non-independence of folds.

## Library implementation

`scipy.stats.ttest_ind(x, y, equal_var=False)` performs Welch's test: its `statistic` is your
t, and recent SciPy versions also expose the Welch–Satterthwaite degrees of freedom as `.df`, plus
a p-value. The comparison runs only when SciPy is installed.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
