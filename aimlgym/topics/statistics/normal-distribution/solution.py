r"""Reference solution for ST-09 The Normal Distribution.

The density and cdf are direct translations of their formulas; the cdf relies on `math.erf`,
which the standard library computes accurately. Interval probabilities are differences of the
cdf, the empirical rule reuses that on the standard normal, and the binomial approximation plugs
the binomial mean and standard deviation into the normal cdf at $k + 0.5$.
"""
import math


def _check(sigma):
    if sigma <= 0:
        raise ValueError("sigma must be positive")


def normal_pdf(x, mu=0.0, sigma=1.0):
    _check(sigma)
    return math.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))


def normal_cdf(x, mu=0.0, sigma=1.0):
    _check(sigma)
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))


def prob_between(a, b, mu=0.0, sigma=1.0):
    if b < a:
        raise ValueError("need a <= b")
    return normal_cdf(b, mu, sigma) - normal_cdf(a, mu, sigma)


def empirical_rule():
    return {k: prob_between(-k, k) for k in (1, 2, 3)}


def binomial_cdf_approx(k, n, p):
    mu = n * p
    sigma = math.sqrt(n * p * (1 - p))
    return normal_cdf(k + 0.5, mu, sigma)
