# Selecting and Filtering

## Learning outcomes

After this lesson you can:

- Filter rows with boolean masks and isin
- Select columns with .loc
- Reset the index after filtering

## Intuition
Filtering a DataFrame is NumPy masking with labels: build a True/False Series per row, keep the
Trues, and pick the columns you want.

## Precise explanation
* `df["score"] >= 60` → boolean Series aligned with the index.
* Combine with `&`, `|`, `~` and parentheses (as in NP-04).
* `df["city"].isin(["Pune", "Chennai"])` tests membership.
* `df.loc[mask, ["name", "score"]]` selects rows by mask and columns by label in one step.
  Avoid chained indexing like `df[mask]["score"] = 0` — under Copy-on-Write (pandas 3) it never
  modifies `df`.
* After filtering, the index keeps the original labels (e.g. 0, 3, 4). `reset_index(drop=True)`
  renumbers 0..k−1.

## Worked example
```python
df.loc[(df.score >= 60) & df.city.isin(["Pune"]), ["name"]].reset_index(drop=True)
```

## Common mistakes
* `and` instead of `&`.
* Forgetting parentheses around comparisons.
* Expecting `df[df.score > 60].loc[0]` to work when row 0 was filtered out.

## Why this matters
Selecting cohorts, removing invalid rows and building train/test subsets are filtering.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
