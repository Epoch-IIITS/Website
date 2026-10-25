r"""Reference solution for PD-13 Weekly Resampling.

Parsing the dates and setting them as the index enables `resample`. Weekly buckets end on
Sunday; sum and count give 0 for empty weeks while mean gives NaN, which is the honest answer.
"""
import pandas as pd


def weekly_summary(df):
    if len(df) == 0:
        raise ValueError("empty frame")
    s = (df.assign(date=pd.to_datetime(df["date"]))
           .set_index("date")["amount"].sort_index())
    r = s.resample("W")
    out = pd.DataFrame({"total": r.sum(), "n": r.count(), "mean": r.mean()})
    out.index.name = "date"
    return out
