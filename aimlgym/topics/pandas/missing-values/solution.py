r"""Reference solution for PD-06 Finding and Handling Missing Values.

`isna().sum()` counts True values per column. `dropna(subset=...)` limits the check to the
columns that matter, and `fillna` with a dict applies a different default per column while
returning a new frame. The manual mean shows what `skipna=True` does inside pandas.
"""
import math

import pandas as pd


def missing_report(df):
    return {str(c): int(n) for c, n in df.isna().sum().items()}


def drop_incomplete(df, cols):
    return df.dropna(subset=list(cols)).reset_index(drop=True)


def fill_defaults(df, defaults):
    return df.fillna(defaults)


def mean_skipping_missing(values):
    kept = [v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    if not kept:
        return None
    return sum(kept) / len(kept)
