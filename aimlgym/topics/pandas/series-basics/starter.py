import pandas as pd


def make_series(data):
    return pd.Series(data, dtype=float)


def add_aligned(a, b):
    # TODO: add with fill_value=0, then sort by label
    return a + b


def above_mean(s):
    # TODO
    return []


def top_labels(s, k):
    # TODO
    return []


def count_values(items):
    # TODO
    return {}
