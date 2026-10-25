r"""Reference solution for NP-03 Slicing a Sub-grid.

`crop` validates bounds (slicing would silently clip) and returns a copy so callers can modify it
safely. `every_other` uses steps. `border_sum` subtracts the interior from the total; for arrays
with fewer than three rows or columns the interior slice is empty and sums to 0.
"""
import numpy as np


def crop(a, top, left, h, w):
    if h < 1 or w < 1 or top < 0 or left < 0:
        raise ValueError("invalid crop parameters")
    if top + h > a.shape[0] or left + w > a.shape[1]:
        raise ValueError("crop does not fit")
    return a[top:top + h, left:left + w].copy()


def every_other(a):
    return a[::2, ::2]


def border_sum(a):
    return a.sum() - a[1:-1, 1:-1].sum()
