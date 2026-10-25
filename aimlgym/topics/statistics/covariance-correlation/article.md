# Covariance and Correlation

## Learning outcomes

After this lesson you can:

- Compute sample covariance
- Compute Pearson's r and interpret its range
- Recognise that correlation measures only linear association

## Intuition
Do two variables move together? If above-average $x$ tends to come with above-average $y$, the
products of their deviations are mostly positive — positive covariance. Correlation rescales
covariance to $[-1, 1]$ so it no longer depends on units.

## Precise explanation
$$\operatorname{cov}(x,y) = \frac{1}{n-1}\sum (x_i-\bar x)(y_i-\bar y)\quad(\text{sample}),$$
$$r = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum (x_i-\bar x)^2}\,\sqrt{\sum (y_i-\bar y)^2}}.$$
The $n$ vs $n-1$ factor cancels in $r$. $r = \pm 1$ means a perfect line; $r = 0$ means no
*linear* relationship — $y = x^2$ on symmetric $x$ has $r = 0$ despite perfect dependence.
$r$ is the cosine of the angle between the centred vectors (compare MA-04).

`statistics.covariance` and `statistics.correlation` (Python 3.10+) implement these.

## Worked example
x = [1, 2, 3, 4], y = [2, 4, 5, 8]: means 2.5 and 4.75; deviation products
(−1.5)(−2.75)+(−0.5)(−0.75)+(0.5)(0.25)+(1.5)(3.25) = 9.5; sample cov = 9.5/3 ≈ 3.167;
Σdx² = 5, Σdy² = 18.75, r = 9.5/√93.75 ≈ 0.981.

## Common mistakes
* Interpreting correlation as causation.
* Ignoring that one outlier can create or destroy a strong r.
* Dividing by zero when one variable is constant (r is undefined).

## Why this matters
Correlated features cause unstable linear-model coefficients (ridge regression helps, ML-20),
and correlation matrices are a standard first exploratory step.

## Library implementation

Python 3.10+ provides `statistics.covariance(x, y)` (sample, $n-1$) and
`statistics.correlation(x, y)` (Pearson). NumPy's `np.cov` and `np.corrcoef` return full
matrices for several variables at once.

## References

- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
