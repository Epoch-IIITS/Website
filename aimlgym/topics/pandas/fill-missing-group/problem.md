# PD-09 · Fill Missing Values by Group

**Topic:** Pandas · **Difficulty:** intermediate · **Allowed packages:** pandas, numpy

**Builds on:** PD-08 Group-by Aggregation

Read the lesson first: [article.md](article.md)

## Task

Write `impute_group_mean(df, group, col)` returning a **new** DataFrame where NaN in `col` are
replaced by the mean of `col` within the same `group`; if that group mean is NaN (all missing),
use the overall mean of `col`. Also add a boolean column `f"{col}_was_missing"`.
If the whole column is NaN, raise `ValueError`.

**Example**
```python
df = pd.DataFrame({"g": list("aabbc"), "v": [1, np.nan, 10, 20, np.nan]})
impute_group_mean(df, "g", "v")["v"].round(2).tolist()
# [1.0, 1.0, 10.0, 20.0, 10.33]
```

## Hints

<details><summary>Hint 1</summary>

`group_mean = df.groupby(group)[col].transform('mean')`.

</details>

<details><summary>Hint 2</summary>

`filled = df[col].fillna(group_mean).fillna(df[col].mean())`.

</details>

<details><summary>Hint 3</summary>

Use `df.assign(**{col: filled, f'{col}_was_missing': df[col].isna()})`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_values` | Use groupby().transform('mean') then fall back to the overall mean. |
| `test_group_mean_not_global` | Fill with the group's mean, not the global mean. |
| `test_indicator` | Compute the indicator from the original column before filling. |
| `test_input_unchanged` | Return df.assign(...) rather than modifying df. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`transform("mean")` broadcasts each group's mean back to its rows, so `fillna` can align it by
index. A second `fillna` with the global mean covers groups that have no observed values. The
indicator column records which values were imputed, computed from the original column.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
