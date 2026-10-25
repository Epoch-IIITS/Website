r"""Reference solution for PD-15 Binning with pd.cut.

`pd.cut` maps each age to its left-closed interval and attaches labels; negative ages fall
outside every bin and become NaN. Counting over the categorical keeps the bin order and reports
empty categories as 0.
"""
import numpy as np
import pandas as pd

EDGES = [0, 13, 20, 65, np.inf]
LABELS = ["child", "teen", "adult", "senior"]


def age_groups(ages):
    return pd.cut(pd.Series(ages, dtype=float), bins=EDGES, labels=LABELS, right=False)


def group_counts(ages):
    counts = age_groups(ages).value_counts(sort=False)
    return {str(k): int(counts.get(k, 0)) for k in LABELS}
