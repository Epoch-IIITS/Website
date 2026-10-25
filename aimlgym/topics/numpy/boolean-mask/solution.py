r"""Reference solution for NP-04 Boolean Masks.

Comparisons produce masks; `&` combines them element-wise and boolean indexing extracts the
selected elements. Summing a mask counts Trues. `np.where` constructs a fresh array, leaving the
input untouched.
"""
import numpy as np


def in_range(a, lo, hi):
    a = np.asarray(a)
    return a[(a >= lo) & (a <= hi)]


def count_above(a, t):
    return int((np.asarray(a) > t).sum())


def cap(a, t):
    a = np.asarray(a)
    return np.where(a > t, t, a)
