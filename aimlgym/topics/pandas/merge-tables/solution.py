r"""Reference solution for PD-10 Merging Tables.

A left join keeps every order; `validate` guards against duplicate customers, and missing
matches are labelled "unknown". The spend table groups the merged rows by name and sorts with a
deterministic tie-break.
"""
import pandas as pd


def orders_with_customers(orders, customers):
    merged = pd.merge(orders, customers, on="customer_id", how="left", validate="many_to_one")
    return merged.assign(name=merged["name"].fillna("unknown")).reset_index(drop=True)


def spend_per_customer(orders, customers):
    m = orders_with_customers(orders, customers)
    out = m.groupby("name", as_index=False).agg(total=("amount", "sum"))
    return out.sort_values(["total", "name"], ascending=[False, True]).reset_index(drop=True)
