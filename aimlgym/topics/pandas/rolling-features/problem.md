# PD-16 · Rolling-Window Features

**Topic:** Pandas · **Difficulty:** advanced · **Allowed packages:** pandas, numpy

**Builds on:** PD-13 Weekly Resampling, NP-14 Moving Average with cumsum

Read the lesson first: [article.md](article.md)

## Task

Write `add_history_features(df, window=3)` for columns `store`, `date` (`YYYY-MM-DD`),
`sales`. Return a new DataFrame sorted by `store` then `date` (index 0..n−1, `date` converted to
datetime) with two new columns computed **within each store**:
* `lag1`: previous sales value (NaN for a store's first row),
* `past_mean`: mean of up to `window` previous sales values (NaN for the first row).
Raise `ValueError` if `window < 1`.

**Example**
```python
df = pd.DataFrame({"store": ["A", "B", "A", "A", "B", "A"],
                   "date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03", "2026-01-02", "2026-01-04"],
                   "sales": [10, 5, 20, 30, 7, 40]})
add_history_features(df, window=2)[["store", "sales", "lag1", "past_mean"]]
#   store  sales  lag1  past_mean
# 0     A     10   NaN        NaN
# 1     A     20  10.0       10.0
# 2     A     30  20.0       15.0
# 3     A     40  30.0       25.0
# 4     B      5   NaN        NaN
# 5     B      7   5.0        5.0
```

## Hints

<details><summary>Hint 1</summary>

`out = df.assign(date=pd.to_datetime(df['date'])).sort_values(['store', 'date']).reset_index(drop=True)`.

</details>

<details><summary>Hint 2</summary>

`g = out.groupby('store')['sales']`; `lag1 = g.shift(1)`.

</details>

<details><summary>Hint 3</summary>

`g.transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_past_mean` | Shift by one before rolling so the current sale is excluded. |
| `test_lag` | Compute the lag within each store (groupby('store')). |
| `test_order` | Sort by store, then date, and reset the index. |
| `test_no_leakage` | past_mean must never include the current row's value. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Sorting by store and date defines "previous". Within each store, shifting by one excludes the
current row, so both the lag and the rolling mean only use past information. `transform` keeps
the results aligned with the sorted rows.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
