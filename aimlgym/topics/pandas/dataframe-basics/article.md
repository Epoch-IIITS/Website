# Series and DataFrames

## Learning outcomes

After this lesson you can:

- Create a DataFrame from a dict of columns
- Inspect shape, columns and dtypes
- Identify numeric columns

## Intuition
A **DataFrame** is a table: each column is a **Series** (a labelled 1-D array) with its own
dtype, and all columns share a row **index**. Think of a spreadsheet whose columns know their
types.

## Precise explanation
* `pd.DataFrame({"name": [...], "score": [...]})` — keys become column names; all lists must have
  the same length (else `ValueError`).
* `df.shape` → `(n_rows, n_cols)`; `df.columns` → column labels; `df.dtypes` → dtype per column.
* Numeric columns: `df.select_dtypes(include="number").columns`.
* `df.head()`, `df.info()`, `df.describe()` give quick summaries.
* Unlike a NumPy array, different columns can hold different types (strings, floats, booleans).

## Worked example
```python
df = pd.DataFrame({"name": ["ann", "bob"], "score": [91.5, 78.0], "year": [1, 2]})
df.shape                      # (2, 3)
list(df.select_dtypes("number").columns)   # ['score', 'year']
```

## Common mistakes
* Building a DataFrame row by row in a loop (slow); build lists or dicts first.
* Unequal column lengths.
* Assuming the index is 0..n−1 after filtering (see PD-04's `reset_index`).

## Why this matters
Almost every real dataset arrives as a table; inspecting shape and dtypes catches problems such
as numbers stored as strings before they break a model.

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
