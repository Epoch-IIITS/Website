r"""Reference solution for ST-07 Conditional Probability and Bayes' Rule.

Conditioning keeps only the outcomes where `b` holds and counts `a` among them, which equals
$P(A\cap B)/P(B)$. The posterior divides the true-positive mass by all positive mass. `update`
reuses the same formula with likelihoods chosen by each result, feeding each posterior forward as
the next prior.
"""
from fractions import Fraction


def conditional(space, a, b):
    given = [o for o in space if b(o)]
    if not given:
        raise ValueError("conditioning event has probability 0")
    return Fraction(sum(1 for o in given if a(o)), len(given))


def posterior(prior, sensitivity, false_positive_rate):
    evidence = sensitivity * prior + false_positive_rate * (1 - prior)
    return sensitivity * prior / evidence


def update(prior, sensitivity, false_positive_rate, results):
    p = prior
    for positive in results:
        if positive:
            like_d, like_not = sensitivity, false_positive_rate
        else:
            like_d, like_not = 1 - sensitivity, 1 - false_positive_rate
        p = like_d * p / (like_d * p + like_not * (1 - p))
    return p
