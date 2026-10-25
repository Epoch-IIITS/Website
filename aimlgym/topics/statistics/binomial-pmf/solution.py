r"""Reference solution for ST-08 Binomial Probabilities.

The PMF is the formula directly. The CDF sums PMF terms (returning exact 0/1 at the extremes),
and the upper tail uses the complement rule with k − 1 because P(X ≥ k) excludes k − 1 and below.
`min`/`max` clamp tiny floating-point overshoots outside [0, 1].
"""
import math


def _check(n, p):
    if n < 0:
        raise ValueError("n must be >= 0")
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0, 1]")


def binom_pmf(k, n, p):
    _check(n, p)
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def binom_cdf(k, n, p):
    _check(n, p)
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return min(1.0, sum(binom_pmf(j, n, p) for j in range(k + 1)))


def prob_at_least(k, n, p):
    _check(n, p)
    return max(0.0, 1.0 - binom_cdf(k - 1, n, p))
