# PD-13 · Weekly Resampling

**Topic:** Pandas · **Difficulty:** advanced · **Allowed packages:** pandas, numpy

**Builds on:** PD-12 Working with Dates, PD-08 Group-by Aggregation

Read the lesson first: [article.md](article.md)

## Task

Write `weekly_summary(df)` for columns `date` (strings `YYYY-MM-DD`) and `amount` (numbers).
Return a DataFrame indexed by week-end Sunday (`resample("W")`) with columns:
* `total` (sum, 0 for empty weeks), `n` (count, 0 for empty weeks), `mean` (NaN for empty weeks).

The index name should be `date`. Raise `ValueError` for an empty frame.

**Example**
```python
df = pd.DataFrame({"date": ["2026-01-05", "2026-01-11", "2026-01-12", "2026-01-26"],
                   "amount": [10, 5, 7, 1]})
weekly_summary(df)
#             total  n  mean
# date
# 2026-01-11     15  2   7.5
# 2026-01-18      7  1   7.0
# 2026-01-25      0  0   NaN
# 2026-02-01      1  1   1.0
```

## Hints

<details><summary>Hint 1</summary>

`s = df.assign(date=pd.to_datetime(df['date'])).set_index('date')['amount'].sort_index()`.

</details>

<details><summary>Hint 2</summary>

`r = s.resample('W')`.

</details>

<details><summary>Hint 3</summary>

`pd.DataFrame({'total': r.sum(), 'n': r.count(), 'mean': r.mean()})`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_index` | Use resample('W') (weeks end Sunday) and name the index 'date'. |
| `test_counts` | Use count() so empty weeks show 0. |
| `test_mean_nan_empty` | Mean of an empty week is NaN — don't fill it. |
| `test_unsorted_input` | Convert to datetime and sort the index. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Parsing the dates and setting them as the index enables `resample`. Weekly buckets end on
Sunday; sum and count give 0 for empty weeks while mean gives NaN, which is the honest answer.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
