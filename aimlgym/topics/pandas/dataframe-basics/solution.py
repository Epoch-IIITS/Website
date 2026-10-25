r"""Reference solution for PD-02 Build and Describe a DataFrame.

Validation gives a clear message before pandas does. `describe_df` reads the shape and column
labels, and `select_dtypes` filters numeric columns (ints and floats, but not booleans or strings).
"""
import pandas as pd


def make_df(data):
    if not data:
        raise ValueError("data must not be empty")
    if len({len(v) for v in data.values()}) != 1:
        raise ValueError("all columns must have the same length")
    return pd.DataFrame(data)


def describe_df(df):
    return {
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": [str(c) for c in df.columns],
        "numeric": [str(c) for c in df.select_dtypes(include="number").columns],
    }
