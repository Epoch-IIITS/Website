# PD-02 · Build and Describe a DataFrame

**Topic:** Pandas · **Difficulty:** beginner · **Allowed packages:** pandas, numpy

**Builds on:** PD-01 Series: Labelled Columns

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `make_df(data)` → DataFrame from a dict of equal-length lists; raise `ValueError` if `data` is
  empty or lengths differ.
* `describe_df(df)` → dict
  `{"n_rows": int, "n_cols": int, "columns": list[str], "numeric": list[str]}`
  (columns in table order).

**Example**
```python
df = make_df({"name": ["ann", "bob"], "score": [91.5, 78.0], "year": [1, 2]})
describe_df(df)
# {'n_rows': 2, 'n_cols': 3, 'columns': ['name', 'score', 'year'], 'numeric': ['score', 'year']}
```

## Hints

<details><summary>Hint 1</summary>

Check `len(set(len(v) for v in data.values())) == 1`.

</details>

<details><summary>Hint 2</summary>

`pd.DataFrame(data)` builds the table.

</details>

<details><summary>Hint 3</summary>

`list(df.select_dtypes(include='number').columns)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_describe` | Return plain lists/ints; use select_dtypes(include='number'). |
| `test_unequal` | Check every column list has the same length. |
| `test_bool_not_numeric` | Booleans are not selected by include='number'. |
| `test_make` | Return pd.DataFrame(data). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Validation gives a clear message before pandas does. `describe_df` reads the shape and column
labels, and `select_dtypes` filters numeric columns (ints and floats, but not booleans or strings).

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
