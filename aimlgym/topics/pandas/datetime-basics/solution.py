r"""Reference solution for PD-12 Working with Dates.

Parsing with an explicit format converts text into datetime values once; afterwards the `.dt`
accessor extracts parts element-wise and subtraction produces timedeltas whose `.dt.days` gives
whole days. The manual version shows the same calculation for a single pair with the standard
library.
"""
import datetime

import pandas as pd


def days_between_manual(start, end):
    return (datetime.date.fromisoformat(end) - datetime.date.fromisoformat(start)).days


def parse_dates(df, col):
    return df.assign(**{col: pd.to_datetime(df[col], format="%Y-%m-%d")})


def add_date_parts(df, col):
    d = df[col].dt
    return df.assign(year=d.year, month=d.month, weekday=d.day_name())


def add_duration(df, start, end):
    s = pd.to_datetime(df[start], format="%Y-%m-%d")
    e = pd.to_datetime(df[end], format="%Y-%m-%d")
    return df.assign(days=(e - s).dt.days)


def in_month(df, col, year, month):
    d = df[col].dt
    return df[(d.year == year) & (d.month == month)].reset_index(drop=True)
