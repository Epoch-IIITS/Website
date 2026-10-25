r"""Reference solution for PD-01 Series: Labelled Columns.

Each function is one Series operation: `add` with `fill_value` aligns by label without producing
NaN, a boolean mask selects labels above the mean, `nlargest` ranks by value and keeps labels,
and `value_counts` produces a Series of counts that is converted back to a plain dict.
"""
import pandas as pd


def make_series(data):
    return pd.Series(data, dtype=float)


def add_aligned(a, b):
    return a.add(b, fill_value=0).sort_index()


def above_mean(s):
    return s[s > s.mean()].index.tolist()


def top_labels(s, k):
    return s.nlargest(k).index.tolist()


def count_values(items):
    counts = pd.Series(items).value_counts()
    return {k: int(v) for k, v in counts.items()}
