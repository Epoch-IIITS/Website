# The Normal Distribution

## Learning outcomes

After this lesson you can:

- Evaluate the normal density and cumulative probability with math.exp and math.erf
- Compute interval probabilities and the 68–95–99.7 rule
- Approximate a binomial probability with a continuity correction
- Compare a manual formula with statistics.NormalDist

## Intuition
Heights, measurement errors and averages of many small effects pile up in a symmetric bell
shape. The **normal distribution** $\mathcal N(\mu, \sigma^2)$ describes that bell: $\mu$ is its
centre and $\sigma$ its width. Because it is continuous, we ask for the probability of an
*interval*, which is the area under the curve.

## Precise explanation
**Density (pdf)**
$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).$$
**Cumulative probability (cdf)**, using the error function `math.erf`:
$$F(x) = P(X \le x) = \tfrac12\left[1 + \operatorname{erf}\!\left(\frac{x-\mu}{\sigma\sqrt2}\right)\right].$$
* $P(a \le X \le b) = F(b) - F(a)$. A single point has probability 0; $f(x)$ is a density, not a
  probability, and can exceed 1 when $\sigma$ is small.
* Standardising with $z = (x - \mu)/\sigma$ (ST-05) turns any normal into $\mathcal N(0, 1)$.
* **68–95–99.7 rule**: about 68.27%, 95.45% and 99.73% of the mass lies within 1, 2 and 3
  standard deviations of the mean.
* **Normal approximation to the binomial** (ST-08): for large $n$,
  $X \sim \text{Bin}(n, p)$ is close to $\mathcal N(np,\, np(1-p))$, and
  $P(X \le k) \approx F(k + 0.5)$ — the $+0.5$ **continuity correction** accounts for replacing
  bars at integers with a smooth curve.

## Worked example
$\mathcal N(170, 10^2)$: $P(X \le 180) = F(180) = \frac12[1 + \operatorname{erf}(1/\sqrt2)] \approx 0.8413$;
$P(160 \le X \le 180) \approx 0.8413 - 0.1587 = 0.6827$.

## Common mistakes
* Passing the variance where the standard deviation is expected.
* Treating $f(x)$ as $P(X = x)$.
* Forgetting the $\sqrt2$ inside the erf.

## Why this matters
Confidence intervals (ST-12), the t-test (ST-18), weight
initialisation and Gaussian noise for privacy all use the normal distribution.

## Library implementation

`statistics.NormalDist(mu, sigma)` provides `.pdf(x)`, `.cdf(x)` and `.inv_cdf(p)` (the
quantile function you will use for confidence intervals), plus arithmetic on independent normal
variables. `scipy.stats.norm` offers the same functions vectorised over arrays. The tests compare
your functions with `NormalDist`, and with SciPy if it is installed.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [math — Mathematical functions](https://docs.python.org/3/library/math.html) — Python Software Foundation (`S050`)
