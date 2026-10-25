# Introducing scipy.stats

## Learning outcomes

After this lesson you can:

- Create frozen distribution objects with scipy.stats.norm and scipy.stats.binom
- Use pdf/pmf, cdf, ppf, mean and std on a distribution object
- Check library results against the formulas you implemented by hand

## Intuition
In ST-08 and ST-09 you wrote the probability formulas yourself. In
practice you reach for `scipy.stats`: one object per distribution that knows its density,
cumulative probability, quantiles, mean and spread, tested by thousands of users. Knowing the
formulas lets you check the library; knowing the library saves you from re-deriving them.

## Precise explanation
`scipy.stats` provides distribution families. Calling a family with its parameters returns a
**frozen** distribution:

```python
from scipy import stats
heights = stats.norm(loc=170, scale=10)   # normal, mean 170, standard deviation 10
coins = stats.binom(n=10, p=0.5)          # number of heads in 10 fair flips
```

| Method | Continuous (`norm`) | Discrete (`binom`) |
|---|---|---|
| density | `pdf(x)` — probability density | `pmf(k)` — P(X = k) |
| `cdf(x)` | P(X ≤ x) | P(X ≤ k) |
| `ppf(q)` | the x with cdf(x) = q (inverse cdf, the quantile) | smallest k with cdf(k) ≥ q |
| `sf(x)` | 1 − cdf(x), the upper tail, computed accurately | same |
| `mean()`, `std()` | μ, σ | np, √(np(1−p)) |

`loc` and `scale` are SciPy's general names for shift and stretch; for the normal they are μ and σ.
Results are NumPy floats; wrap them in `float()` when you need plain Python numbers.

## Worked example
```python
stats.norm(170, 10).cdf(180)     # 0.8413...: 84% of heights are below 180
stats.norm(170, 10).ppf(0.975)   # 189.6: 97.5% are below this
stats.binom(10, 0.5).pmf(5)      # 0.24609375 = C(10,5) / 2**10
stats.binom(10, 0.5).ppf(0.5)    # 5.0: the median number of heads
```

## What the library does inside
`norm.cdf` evaluates the same error-function formula as ST-09, using special
functions that stay accurate far in the tails; `binom.pmf` evaluates C(n, k)pᵏ(1−p)ⁿ⁻ᵏ from
ST-08 in log space so large n does not overflow. `ppf` inverts the cdf numerically.

## Common mistakes
* Passing the variance as `scale`: `scale` is the standard deviation.
* Calling `pdf` on a discrete distribution: discrete ones have `pmf`.
* Using `1 - cdf(x)` for tiny tail probabilities: `sf(x)` keeps precision.
* Forgetting that `ppf` of a discrete distribution returns a float (`5.0`), not an `int`.

## Why this matters
Every test in the next steps turns a statistic into a p-value through one of these objects, and
machine-learning code uses them to sample noise, set priors and compute confidence intervals.

## References

- [Statistical functions (scipy.stats)](https://docs.scipy.org/doc/scipy/reference/stats.html) — SciPy developers (`S101`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
