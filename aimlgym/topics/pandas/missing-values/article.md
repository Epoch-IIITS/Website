# Finding and Handling Missing Values

## Learning outcomes

After this lesson you can:

- Detect missing values with isna and count them per column
- Drop incomplete rows only for the columns that matter
- Fill missing values with per-column defaults
- Explain how pandas reductions skip NaN, compared with a manual loop

## Intuition
Real data has holes: a sensor was off, a form field was left blank. pandas marks a missing value
as `NaN` ("not a number") or `None`. Before modelling you must find the holes and decide, column
by column, whether to drop those rows or fill them.

## Precise explanation
* `df.isna()` is a boolean DataFrame (`True` where missing); `df.isna().sum()` counts per column.
  `NaN != NaN`, so never test `x == np.nan`; use `isna` (or `math.isnan` for a single float).
* `df.dropna(subset=["age"])` drops rows missing `age`; without `subset` any missing cell drops
  the row, which can discard most of your data.
* `df.fillna({"city": "unknown", "age": 0})` fills each column with its own default.
* Reductions skip missing values by default: `s.mean()` averages only present values
  (`skipna=True`). A manual loop must do this explicitly.
* Operations return new objects; assign the result (`df = df.dropna(...)`).

## Worked example
```python
df = pd.DataFrame({"age": [20, None, 31], "city": ["A", "B", None]})
df.isna().sum()                 # age 1, city 1
df.dropna(subset=["age"])       # keeps rows 0 and 2
df["age"].mean()                # 25.5 — the None is skipped
```

## Common mistakes
* `dropna()` with no subset removing far more rows than intended.
* Filling with 0 when 0 is a meaningful value; consider the median or a separate
  "was missing" flag (PD-09).
* Forgetting `reset_index(drop=True)` and then being surprised by gaps in the index.

## Why this matters
Most ML models cannot accept NaN, and the way you fill gaps changes the results; leakage from
filling with statistics of the whole dataset is covered in ML-08.

## References

- [Working with missing data (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/missing_data.html) — pandas development team (`S086`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
