# PD-14 · Pivot Tables

**Topic:** Pandas · **Difficulty:** advanced · **Allowed packages:** pandas, numpy

**Builds on:** PD-08 Group-by Aggregation

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `sales_pivot(df)` → wide DataFrame from long columns `region, quarter, sales`: index =
  regions (sorted), columns = quarters (sorted), values = summed sales, missing = 0, integer
  dtype if `sales` is integer. Remove the columns-axis name (`rename_axis(columns=None)`).
* `to_long(wide)` → long DataFrame with columns `region, quarter, sales`, sorted by region then
  quarter, index 0..n−1 (zeros included).

**Example**
```python
df = pd.DataFrame({"region": ["N", "N", "S", "N"], "quarter": ["Q1", "Q2", "Q1", "Q1"],
                   "sales": [5, 3, 7, 2]})
sales_pivot(df)
#         Q1  Q2
# region
# N        7   3
# S        7   0
```

## Hints

<details><summary>Hint 1</summary>

`pd.pivot_table(df, index='region', columns='quarter', values='sales', aggfunc='sum', fill_value=0)`.

</details>

<details><summary>Hint 2</summary>

`.rename_axis(columns=None)` drops the 'quarter' label above the columns.

</details>

<details><summary>Hint 3</summary>

`wide.reset_index().melt(id_vars='region', var_name='quarter', value_name='sales')`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_values` | Use aggfunc='sum' so duplicate pairs are added, and fill_value=0. |
| `test_axes` | Sort index/columns and remove the columns name with rename_axis(columns=None). |
| `test_long` | Melt with id_vars='region', var_name='quarter', value_name='sales', then sort. |
| `test_int_dtype` | fill_value=0 keeps integer dtype; NaN would force floats. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`pivot_table` aggregates duplicate (region, quarter) pairs and fills empty cells. Sorting both
axes makes the output deterministic. `melt` reverses the reshape, keeping region as the id.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
