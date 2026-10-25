# PD-08 · Group-by Aggregation

**Topic:** Pandas · **Difficulty:** intermediate · **Allowed packages:** pandas, numpy

**Builds on:** PD-07 Sort and Rank, PY-18 Gradebook Aggregation

Read the lesson first: [article.md](article.md)

## Task

Write `category_summary(df)` for columns `category` and `value` (float, may contain NaN).
Return a DataFrame with columns `category, n, n_valid, total, mean`, one row per category sorted
by category, index 0..k−1, where `n` = rows, `n_valid` = non-missing values, `total` = sum
(NaN skipped), `mean` = mean of non-missing values.

**Example**
```python
category_summary(pd.DataFrame({"category": ["a", "b", "a", "b", "a"],
                               "value": [1, 2, 3, np.nan, 5]}))
#   category  n  n_valid  total  mean
# 0        a  3        3    9.0   3.0
# 1        b  2        1    2.0   2.0
```

## Hints

<details><summary>Hint 1</summary>

`df.groupby('category')` then `.agg(...)` with named aggregations.

</details>

<details><summary>Hint 2</summary>

`n=('value', 'size')`, `n_valid=('value', 'count')`.

</details>

<details><summary>Hint 3</summary>

`total=('value', 'sum')`, `mean=('value', 'mean')`, then `.reset_index()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_values` | n uses 'size' (all rows); n_valid uses 'count' (non-missing). |
| `test_columns` | Use named aggregation and reset_index() so category is a column. |
| `test_all_nan_group` | mean of all-NaN values is NaN; count is 0. |
| `test_sorted` | groupby sorts keys by default; keep sort=True. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One `groupby().agg()` call computes all four statistics with explicit output names. `size`
counts all rows while `count` skips NaN, which is exactly the difference between n and n_valid.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
