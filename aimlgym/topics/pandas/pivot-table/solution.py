r"""Reference solution for PD-14 Pivot Tables.

`pivot_table` aggregates duplicate (region, quarter) pairs and fills empty cells. Sorting both
axes makes the output deterministic. `melt` reverses the reshape, keeping region as the id.
"""
import pandas as pd


def sales_pivot(df):
    wide = pd.pivot_table(df, index="region", columns="quarter", values="sales",
                          aggfunc="sum", fill_value=0)
    return wide.sort_index().sort_index(axis=1).rename_axis(columns=None)


def to_long(wide):
    long = wide.reset_index().melt(id_vars="region", var_name="quarter", value_name="sales")
    return long.sort_values(["region", "quarter"]).reset_index(drop=True)
