import csv
import io

import pandas as pd


def _convert(value):
    # TODO: int, then float, else the original string
    return value


def parse_manual(text):
    # TODO
    return []


def parse_pandas(text):
    # TODO
    return pd.DataFrame()


def numeric_means(df):
    # TODO
    return {}


def to_csv_text(df):
    # TODO
    return df.to_csv()
