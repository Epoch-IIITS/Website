r"""Reference solution for PD-09 Fill Missing Values by Group.

`transform("mean")` broadcasts each group's mean back to its rows, so `fillna` can align it by
index. A second `fillna` with the global mean covers groups that have no observed values. The
indicator column records which values were imputed, computed from the original column.
"""
import numpy as np
import pandas as pd


def impute_group_mean(df, group, col):
    if df[col].isna().all():
        raise ValueError("column is entirely missing")
    group_mean = df.groupby(group)[col].transform("mean")
    filled = df[col].fillna(group_mean).fillna(df[col].mean())
    return df.assign(**{col: filled, f"{col}_was_missing": df[col].isna()})
