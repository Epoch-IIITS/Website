r"""Reference solution for MA-02 Exponentials and Logarithms.

The change-of-base and doubling formulas are direct translations. The log-likelihood never forms
the tiny product, so it cannot underflow, and invalid probabilities are rejected before taking
logs. Subtracting the maximum in log-sum-exp makes the largest exponent exactly 1, so the sum is
between 1 and n and its logarithm is always finite.
"""
import math


def log_base(x, base):
    return math.log(x) / math.log(base)


def doubling_time(rate):
    return math.log(2) / math.log(1 + rate)


def log_likelihood(probs):
    total = 0.0
    for p in probs:
        if not 0 < p <= 1:
            raise ValueError("probabilities must be in (0, 1]")
        total += math.log(p)
    return total


def logsumexp(values):
    if not values:
        raise ValueError("logsumexp of empty sequence")
    m = max(values)
    return m + math.log(sum(math.exp(v - m) for v in values))
