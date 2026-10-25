# Long vs Wide: Pivot and Melt

## Learning outcomes

After this lesson you can:

- Reshape long data to wide with pivot_table
- Fill missing cells
- Melt wide data back to long

## Intuition
"Long" data has one row per observation (region, quarter, sales). "Wide" data has one row per
region and one column per quarter — easier for humans to read. Pivoting converts long → wide;
melting converts back.

## Precise explanation
```python
wide = pd.pivot_table(df, index="region", columns="quarter", values="sales",
                      aggfunc="sum", fill_value=0)
```
* Duplicate (region, quarter) pairs are combined by `aggfunc` (`pivot` without aggregation would
  raise on duplicates).
* `fill_value=0` fills combinations with no rows.
* `wide.columns.name` holds "quarter"; `rename_axis(columns=None)` removes it.
* `wide.reset_index().melt(id_vars="region", var_name="quarter", value_name="sales")` goes back
  to long form.

| region | quarter | sales |      | region | Q1 | Q2 |
|---|---|---|---|---|---|---|
| N | Q1 | 5 | → | N | 5 | 3 |
| N | Q2 | 3 |   | S | 7 | 0 |
| S | Q1 | 7 |   |   |   |   |

## Worked example
Above: the S/Q2 cell has no data → filled with 0.

## Common mistakes
* Using `pivot` with duplicate keys.
* Forgetting fill_value and getting NaN.
* Melting without `id_vars`, which melts the identifier too.

## Why this matters
Confusion matrices, user × item matrices for recommenders, and reporting tables are pivots.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
