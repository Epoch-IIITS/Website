# PD-06 · Finding and Handling Missing Values

**Topic:** Pandas · **Difficulty:** beginner · **Allowed packages:** pandas, numpy

**Builds on:** PD-05 Derived Columns

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `missing_report(df)` — dict column → number of missing values (`int`), for every column.
2. `drop_incomplete(df, cols)` — drop rows missing any of `cols`; reset the index.
3. `fill_defaults(df, defaults)` — fill missing values using the dict `defaults` (columns not in
   the dict are unchanged); do not modify `df`.
4. `mean_skipping_missing(values)` — plain-Python mean of a list that may contain `None` or
   `float("nan")`, skipping those; return `None` if nothing is left. (Use `math.isnan` for floats.)

**Example**
```python
df = pd.DataFrame({"age": [20, None, 31], "city": ["A", "B", None]})
missing_report(df)                # {'age': 1, 'city': 1}
mean_skipping_missing([20, None, 31, float("nan")])   # 25.5
```

## Hints

<details><summary>Hint 1</summary>

`{str(c): int(n) for c, n in df.isna().sum().items()}`.

</details>

<details><summary>Hint 2</summary>

`df.dropna(subset=list(cols)).reset_index(drop=True)` and `df.fillna(defaults)`.

</details>

<details><summary>Hint 3</summary>

Skip `v is None` and floats where `math.isnan(v)`; divide the sum by the count of kept values.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_report` | Count with `df.isna().sum()` and convert to a dict of ints. |
| `test_drop_subset` | Pass `subset=` to dropna and reset the index. |
| `test_fill_defaults` | `df.fillna(defaults)` returns a new frame; do not fill in place. |
| `test_manual_mean` | Skip None and NaN values; return None when nothing is left. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`isna().sum()` counts True values per column. `dropna(subset=...)` limits the check to the
columns that matter, and `fillna` with a dict applies a different default per column while
returning a new frame. The manual mean shows what `skipna=True` does inside pandas.

## References

- [Working with missing data (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/missing_data.html) — pandas development team (`S086`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
