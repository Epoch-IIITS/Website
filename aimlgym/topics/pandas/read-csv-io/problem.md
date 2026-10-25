# PD-03 · Reading and Writing CSV

**Topic:** Pandas · **Difficulty:** beginner · **Allowed packages:** pandas, numpy

**Builds on:** PD-02 Build and Describe a DataFrame, PY-23 Files, CSV and JSON

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `parse_manual(text)` — use `csv.DictReader(io.StringIO(text))`; return a list of dicts where
   every value that looks like an integer is an `int`, a decimal number a `float`, and anything
   else stays a string (try `int`, then `float`, else keep the text).
2. `parse_pandas(text)` — `pd.read_csv(io.StringIO(text))`.
3. `numeric_means(df)` — dict column → mean (as `float`) for numeric columns only
   (`df.select_dtypes(include="number")`); `bool` columns are not included.
4. `to_csv_text(df)` — CSV text without the index.

**Example**
```python
text = "name,score,height\nada,91,1.68\nbob,78,1.80\n"
parse_manual(text)[0]          # {'name': 'ada', 'score': 91, 'height': 1.68}
numeric_means(parse_pandas(text))   # {'score': 84.5, 'height': 1.74}
```

## Hints

<details><summary>Hint 1</summary>

In `_convert`, use `try: return int(value)` / `except ValueError:` then the same with float.

</details>

<details><summary>Hint 2</summary>

`[{k: _convert(v) for k, v in row.items()} for row in csv.DictReader(io.StringIO(text))]`.

</details>

<details><summary>Hint 3</summary>

`num = df.select_dtypes(include="number")`; `{c: float(num[c].mean()) for c in num.columns}`; `df.to_csv(index=False)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_manual` | Try `int`, then `float`, otherwise keep the string; use DictReader so quoted commas survive. |
| `test_pandas_dtypes` | Use `pd.read_csv(io.StringIO(text))` with no extra options. |
| `test_numeric_means` | Select numeric columns with `select_dtypes(include="number")`; booleans are excluded. |
| `test_round_trip` | Write with `index=False`. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The manual parser shows what `read_csv` automates: splitting with quote handling (delegated to
the csv module) and per-value type inference. pandas infers one dtype per column, so the numeric
selection keeps only number columns (booleans are a separate dtype). Writing with `index=False`
makes the text round-trip back to an identical DataFrame.

## References

- [IO tools (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/io.html) — pandas development team (`S085`)
- [csv — CSV file reading and writing](https://docs.python.org/3/library/csv.html) — Python Software Foundation (`S055`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
