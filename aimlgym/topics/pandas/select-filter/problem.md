# PD-04 · Select and Filter Rows

**Topic:** Pandas · **Difficulty:** beginner · **Allowed packages:** pandas, numpy

**Builds on:** PD-03 Reading and Writing CSV

Read the lesson first: [article.md](article.md)

## Task

Write `filter_students(df, min_score, cities, cols)` returning a **new** DataFrame with rows
where `score >= min_score` **and** `city` is in `cities`, only the columns `cols` (in that order),
and a fresh 0..k−1 index. Raise `KeyError` (pandas' natural error is fine) for missing columns.

**Example**
```python
df = pd.DataFrame({"name": ["ann", "bob", "cy", "dee"], "city": ["Pune", "Delhi", "Pune", "Chennai"],
                   "score": [72, 90, 55, 61]})
filter_students(df, 60, ["Pune", "Chennai"], ["name", "score"])
#   name  score
# 0  ann     72
# 1  dee     61
```

## Hints

<details><summary>Hint 1</summary>

`mask = (df['score'] >= min_score) & df['city'].isin(cities)`.

</details>

<details><summary>Hint 2</summary>

`df.loc[mask, cols]`.

</details>

<details><summary>Hint 3</summary>

Finish with `.reset_index(drop=True)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Combine masks with & and use isin for the city list. |
| `test_inclusive` | Use >= for min_score. |
| `test_index_reset` | Call reset_index(drop=True). |
| `test_column_order` | Select columns in the order given by cols. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One mask combines both conditions; `.loc` applies it together with the column list, and
`reset_index(drop=True)` discards the old labels.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
