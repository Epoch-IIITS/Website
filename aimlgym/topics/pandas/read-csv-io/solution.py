r"""Reference solution for PD-03 Reading and Writing CSV.

The manual parser shows what `read_csv` automates: splitting with quote handling (delegated to
the csv module) and per-value type inference. pandas infers one dtype per column, so the numeric
selection keeps only number columns (booleans are a separate dtype). Writing with `index=False`
makes the text round-trip back to an identical DataFrame.
"""
import csv
import io

import pandas as pd


def _convert(value):
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def parse_manual(text):
    rows = csv.DictReader(io.StringIO(text))
    return [{k: _convert(v) for k, v in row.items()} for row in rows]


def parse_pandas(text):
    return pd.read_csv(io.StringIO(text))


def numeric_means(df):
    num = df.select_dtypes(include="number")
    return {str(c): float(num[c].mean()) for c in num.columns}


def to_csv_text(df):
    return df.to_csv(index=False)
