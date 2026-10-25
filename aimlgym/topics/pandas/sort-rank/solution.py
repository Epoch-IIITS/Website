r"""Reference solution for PD-07 Sort and Rank.

A two-key stable sort gives the display order; ranking on the score column with `method="min"`
assigns shared ranks to ties and skips the following rank. `assign` keeps the input untouched.
"""
import pandas as pd


def leaderboard(df, n=None):
    out = df.sort_values(["score", "name"], ascending=[False, True], kind="mergesort")
    out = out.assign(rank=out["score"].rank(method="min", ascending=False).astype(int))
    out = out.reset_index(drop=True)
    return out if n is None else out.head(n)
