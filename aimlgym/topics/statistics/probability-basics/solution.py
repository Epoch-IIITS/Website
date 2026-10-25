r"""Reference solution for ST-06 Probability by Counting Outcomes.

Events are predicates, so intersections are built by combining predicates with `and`. Every
probability is an exact `Fraction`, which makes the independence test an exact equality, and the
union follows the inclusion–exclusion formula rather than counting directly.
"""
from fractions import Fraction


def two_dice():
    return [(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7)]


def probability(space, event):
    if not space:
        raise ValueError("empty sample space")
    return Fraction(sum(1 for o in space if event(o)), len(space))


def complement(space, event):
    return 1 - probability(space, event)


def union(space, a, b):
    both = probability(space, lambda o: a(o) and b(o))
    return probability(space, a) + probability(space, b) - both


def independent(space, a, b):
    both = probability(space, lambda o: a(o) and b(o))
    return both == probability(space, a) * probability(space, b)
