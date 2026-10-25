# Sampling Distributions and Standard Error

## Learning outcomes

After this lesson you can:

- Simulate the sampling distribution of the mean with a seeded generator
- Compute the standard error s / √n and explain how it shrinks with n
- Build a normal-approximation 95% confidence interval
- Describe what the central limit theorem does and does not promise

## Intuition
Take a random sample of 30 students and compute their mean height. Take another sample and the
mean changes a little. The **sampling distribution** is the distribution of that mean over all
possible samples. It is narrower than the population — averages vary less than individuals — and
it gets narrower as the sample grows.

## Precise explanation
* If individual values have standard deviation $\sigma$, the mean of $n$ independent values has
  standard deviation $\sigma / \sqrt n$. Quadrupling $n$ halves it.
* We rarely know $\sigma$, so we estimate it with the sample standard deviation $s$ (dividing by
  $n-1$, ST-01): the **standard error** is $\mathrm{SE} = s / \sqrt n$.
* **Central limit theorem (CLT)**: for large $n$ the sampling distribution of the mean is
  approximately normal (ST-09), even when the data are not. It says nothing
  about small samples or heavy outliers, and it assumes independent draws.
* **Normal-approximation 95% interval**: $\bar x \pm z\,\mathrm{SE}$ with $z \approx 1.96$
  (`NormalDist().inv_cdf(0.975)`). "95%" describes the *procedure*: about 95% of intervals built
  this way contain the true mean.

**Simulating sampling with replacement** (reproducibly): with `rng = random.Random(seed)`, draw
an index `int(rng.random() * len(population))` for each of the $n$ values.

## Worked example
Population of die faces 1..6: $\sigma = \sqrt{35/12} \approx 1.708$. For $n = 25$, the means of many
samples have standard deviation about $1.708/5 \approx 0.342$, and their histogram is close to a
bell even though each face is uniform.

## Common mistakes
* Using $\sigma$ of the data as the uncertainty of the mean (forgetting $\sqrt n$).
* Dividing by $n$ instead of $n - 1$ when estimating $s$.
* Saying "there is a 95% probability the true mean is in *this* interval".

## Why this matters
Standard errors are the denominator of the t-statistic (ST-18), and the bootstrap
(ST-13) estimates the same sampling distribution by resampling your data.

## Library implementation

`statistics.stdev(sample) / math.sqrt(len(sample))` gives the same standard error, and
`random.Random(seed).choices(population, k=n)` draws with replacement in one call (its exact
sequence is not guaranteed across Python versions, which is why the graded version builds
indices from `random()`). `scipy.stats.sem` computes the standard error for arrays.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
- [statistics — Mathematical statistics functions](https://docs.python.org/3/library/statistics.html) — Python Software Foundation (`S003`)
- [random — Generate pseudo-random numbers](https://docs.python.org/3/library/random.html) — Python Software Foundation (`S004`)
