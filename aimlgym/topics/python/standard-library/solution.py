r"""Reference solution for PY-15 Importing the Standard Library.

Each function delegates the core work to a standard-library tool: `math.hypot` and `math.ceil`
for numerics, `Counter` for counting (with an explicit alphabetical tie-break, which
`most_common` does not provide), a seeded `random.Random` for reproducible rolls, `heapq` for a
partial sort and `itertools.combinations` for pairs.
"""
import math
import random
from collections import Counter
import heapq
import itertools


def hypotenuse(a, b):
    return math.hypot(a, b)


def pages_needed(items, per_page):
    return math.ceil(items / per_page)


def most_common_letter(text):
    counts = Counter(ch for ch in text.lower() if ch.isalpha())
    if not counts:
        return None
    best = max(counts.values())
    return min(ch for ch, c in counts.items() if c == best)


def dice_rolls(seed, n):
    rng = random.Random(seed)
    return [int(rng.random() * 6) + 1 for _ in range(n)]


def smallest_k(nums, k):
    return heapq.nsmallest(k, nums)


def all_pairs(items):
    return list(itertools.combinations(items, 2))
