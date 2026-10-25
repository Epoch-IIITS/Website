r"""Reference solution for PD-05 Derived Columns.

All three features are vectorised column expressions. `where(b != 0)` converts the undefined
ratios (inf and NaN from division by zero) into NaN. `assign` returns a new frame, so the input is
unchanged.
"""
import numpy as np
import pandas as pd


def add_features(df):
    total = df["a"] + df["b"]
    ratio = (df["a"] / df["b"]).where(df["b"] != 0)
    return df.assign(total=total, ratio=ratio, passed=total >= 50)
