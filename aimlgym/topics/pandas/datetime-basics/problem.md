# PD-12 · Working with Dates

**Topic:** Pandas · **Difficulty:** intermediate · **Allowed packages:** pandas, numpy

**Builds on:** PD-11 Cleaning Text Columns

Read the lesson first: [article.md](article.md)

## Task

Implement:

1. `days_between_manual(start, end)` — days from `start` to `end` (ISO strings) using
   `datetime.date.fromisoformat`.
2. `parse_dates(df, col)` — return a copy with `col` converted by
   `pd.to_datetime(..., format="%Y-%m-%d")`.
3. `add_date_parts(df, col)` — add columns `year`, `month` and `weekday` (the day name, e.g.
   `"Monday"`) for an already-parsed column.
4. `add_duration(df, start, end)` — add a column `days` = whole days from `start` to `end`
   (both string columns; parse them first).
5. `in_month(df, col, year, month)` — rows of a parsed frame whose date is in that month, with a
   reset index.

## Hints

<details><summary>Hint 1</summary>

`(datetime.date.fromisoformat(end) - datetime.date.fromisoformat(start)).days`.

</details>

<details><summary>Hint 2</summary>

`df.assign(**{col: pd.to_datetime(df[col], format="%Y-%m-%d")})` returns a copy.

</details>

<details><summary>Hint 3</summary>

`d = df[col].dt`; `df.assign(year=d.year, month=d.month, weekday=d.day_name())`; filter with `(d.year == year) & (d.month == month)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_manual` | Convert both strings with `datetime.date.fromisoformat` and take `.days` of the difference. |
| `test_parse_rejects_bad_format` | Pass `format="%Y-%m-%d"` so a different format raises instead of being guessed. |
| `test_parts` | Use `.dt.year`, `.dt.month` and `.dt.day_name()`. |
| `test_duration_matches_manual` | Parse both columns, subtract, and use `.dt.days`. |
| `test_in_month` | Combine the year and month conditions with `&` and reset the index. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Parsing with an explicit format converts text into datetime values once; afterwards the `.dt`
accessor extracts parts element-wise and subtraction produces timedeltas whose `.dt.days` gives
whole days. The manual version shows the same calculation for a single pair with the standard
library.

## References

- [Time series / date functionality (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/timeseries.html) — pandas development team (`S087`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
