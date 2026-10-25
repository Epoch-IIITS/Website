r"""Reference solution for PD-16 Rolling-Window Features.

Sorting by store and date defines "previous". Within each store, shifting by one excludes the
current row, so both the lag and the rolling mean only use past information. `transform` keeps
the results aligned with the sorted rows.
"""
import pandas as pd


def add_history_features(df, window=3):
    if window < 1:
        raise ValueError("window must be >= 1")
    out = (df.assign(date=pd.to_datetime(df["date"]))
             .sort_values(["store", "date"], kind="mergesort")
             .reset_index(drop=True))
    g = out.groupby("store")["sales"]
    lag1 = g.shift(1)
    past_mean = g.transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    return out.assign(lag1=lag1, past_mean=past_mean)
