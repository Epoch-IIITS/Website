r"""Reference solution for PD-08 Group-by Aggregation.

One `groupby().agg()` call computes all four statistics with explicit output names. `size`
counts all rows while `count` skips NaN, which is exactly the difference between n and n_valid.
"""
import numpy as np
import pandas as pd


def category_summary(df):
    return (df.groupby("category", sort=True)
              .agg(n=("value", "size"), n_valid=("value", "count"),
                   total=("value", "sum"), mean=("value", "mean"))
              .reset_index())
