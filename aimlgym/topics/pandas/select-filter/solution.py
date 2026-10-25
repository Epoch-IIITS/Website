r"""Reference solution for PD-04 Select and Filter Rows.

One mask combines both conditions; `.loc` applies it together with the column list, and
`reset_index(drop=True)` discards the old labels.
"""
import pandas as pd


def filter_students(df, min_score, cities, cols):
    mask = (df["score"] >= min_score) & df["city"].isin(cities)
    return df.loc[mask, list(cols)].reset_index(drop=True)
