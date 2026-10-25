"""pandas steps added in the 2026-10 revision: Series, reading CSV, missing values and dates.
Each lesson solves the task once with plain Python and once with pandas."""

PROBLEMS = [
# ---------------------------------------------------------------- series-basics
{
"slug": "series-basics", "title": "Series: Labelled Columns",
"difficulty": "beginner", "prereqs": ["boolean-mask"], "packages": ["pandas", "numpy"],
"objectives": ["Create a Series from a dict and read values by label",
               "Explain index alignment in arithmetic between Series",
               "Filter with boolean masks and summarise with mean, nlargest and value_counts",
               "Compare each Series operation with the equivalent dict code"],
"tags": ["series", "index", "alignment", "value-counts"],
"sources": ["S084", "S008"], "entry": "make_series(data); add_aligned(a, b); above_mean(s); top_labels(s, k); count_values(items)",
"article": r'''
# Series: Labelled Columns

## Intuition
A NumPy array is a row of numbers addressed by position. A pandas **Series** is a NumPy array
plus a **label** for every value — like a dict that also supports vectorised arithmetic.
Labels make data self-describing: `prices["apple"]` instead of `prices[3]`.

## Precise explanation
```python
import pandas as pd
s = pd.Series({"apple": 1.2, "pear": 0.8, "fig": 2.5})
s["pear"]          # 0.8   — by label
s.index            # Index(['apple', 'pear', 'fig'], dtype=...)
s.values           # the underlying NumPy array
s[s > 1.0]         # boolean mask, as in NumPy: apple and fig
s.mean(), s.max()  # reductions
s.nlargest(2)      # the two largest values with their labels
pd.Series(["a", "b", "a"]).value_counts()   # counts of each value, largest first
```
* **Alignment**: `a + b` matches values **by label**, not position. A label present in only one
  Series gives `NaN` (missing). `a.add(b, fill_value=0)` treats a missing side as 0 instead.
* `.to_dict()` turns a Series back into a dict; `.index.tolist()` gives the labels.

| Task | dict version | Series version |
|---|---|---|
| add matching keys | `{k: a.get(k, 0) + b.get(k, 0) for k in a.keys() | b.keys()}` | `a.add(b, fill_value=0)` |
| keys with value above the mean | loop + `sum(d.values()) / len(d)` | `s[s > s.mean()]` |
| counts | `Counter(items)` | `pd.Series(items).value_counts()` |

## Worked example
```python
a = pd.Series({"x": 1, "y": 2}); b = pd.Series({"y": 10, "z": 5})
a + b                      # x NaN, y 12, z NaN
a.add(b, fill_value=0)     # x 1.0, y 12.0, z 5.0
```

## Common mistakes
* Expecting `a + b` to pair values by position.
* `s[0]` on a Series with string labels: use `s.iloc[0]` for positions and `s.loc[...]` or `s[...]`
  for labels.
* Forgetting that `value_counts` drops missing values unless `dropna=False`.

## Why this matters
Every DataFrame column is a Series ([[dataframe-basics]]), and label alignment is what makes
joins and group-by results line up correctly.
''',
"statement": r'''
Implement:

1. `make_series(data)` — a `float` Series from a dict of label → number.
2. `add_aligned(a, b)` — add two Series by label, treating a missing side as 0; return the
   result sorted by label.
3. `above_mean(s)` — list of labels whose value is strictly above the Series mean, in Series
   order.
4. `top_labels(s, k)` — list of the labels of the `k` largest values, largest first (use
   `nlargest`).
5. `count_values(items)` — a plain `dict` value → count built from `value_counts()`, with
   `int` counts.

**Examples**
```python
s = make_series({"apple": 1.2, "pear": 0.8, "fig": 2.5})
above_mean(s)                 # ['fig']
top_labels(s, 2)              # ['fig', 'apple']
count_values(["a", "b", "a"]) # {'a': 2, 'b': 1}
```
''',
"starter": r'''
import pandas as pd


def make_series(data):
    return pd.Series(data, dtype=float)


def add_aligned(a, b):
    # TODO: add with fill_value=0, then sort by label
    return a + b


def above_mean(s):
    # TODO
    return []


def top_labels(s, k):
    # TODO
    return []


def count_values(items):
    # TODO
    return {}
''',
"hints": [
    "`a.add(b, fill_value=0).sort_index()`.",
    "`s[s > s.mean()].index.tolist()`.",
    "`counts = pd.Series(items).value_counts()`; build `{k: int(v) for k, v in counts.items()}`.",
],
"solution": r'''
import pandas as pd


def make_series(data):
    return pd.Series(data, dtype=float)


def add_aligned(a, b):
    return a.add(b, fill_value=0).sort_index()


def above_mean(s):
    return s[s > s.mean()].index.tolist()


def top_labels(s, k):
    return s.nlargest(k).index.tolist()


def count_values(items):
    counts = pd.Series(items).value_counts()
    return {k: int(v) for k, v in counts.items()}
''',
"explanation": r'''
Each function is one Series operation: `add` with `fill_value` aligns by label without producing
NaN, a boolean mask selects labels above the mean, `nlargest` ranks by value and keeps labels,
and `value_counts` produces a Series of counts that is converted back to a plain dict.
''',
"tests": r'''
from collections import Counter

import pandas as pd


class TestSeries(unittest.TestCase):
    def setUp(self):
        self.s = S.make_series({"apple": 1.2, "pear": 0.8, "fig": 2.5})

    def test_make_series(self):
        self.assertIsInstance(self.s, pd.Series)
        self.assertEqual(self.s["pear"], 0.8)
        self.assertEqual(str(self.s.dtype), "float64")
        self.assertEqual(self.s.index.tolist(), ["apple", "pear", "fig"])

    def test_add_aligned(self):
        a = pd.Series({"y": 2.0, "x": 1.0})
        b = pd.Series({"y": 10.0, "z": 5.0})
        out = S.add_aligned(a, b)
        self.assertEqual(out.to_dict(), {"x": 1.0, "y": 12.0, "z": 5.0})
        self.assertEqual(out.index.tolist(), ["x", "y", "z"])

    def test_add_matches_dict_version(self):
        a = {"p": 1.0, "q": 4.0}
        b = {"q": 0.5, "r": -2.0}
        manual = {k: a.get(k, 0) + b.get(k, 0) for k in sorted(a.keys() | b.keys())}
        self.assertEqual(S.add_aligned(pd.Series(a), pd.Series(b)).to_dict(), manual)

    def test_above_mean(self):
        self.assertEqual(S.above_mean(self.s), ["fig"])
        self.assertEqual(S.above_mean(pd.Series({"a": 1.0, "b": 1.0})), [])

    def test_top_labels(self):
        self.assertEqual(S.top_labels(self.s, 2), ["fig", "apple"])
        self.assertEqual(S.top_labels(self.s, 1), ["fig"])

    def test_count_values(self):
        items = ["a", "b", "a", "c", "a", "b"]
        out = S.count_values(items)
        self.assertEqual(out, dict(Counter(items)))
        self.assertTrue(all(type(v) is int for v in out.values()))
''',
"feedback": [
    ("test_add_aligned", "Use `a.add(b, fill_value=0)` so labels in only one Series are not NaN, then `sort_index()`."),
    ("test_above_mean", "Select with `s[s > s.mean()]` and return its index as a list."),
    ("test_top_labels", "`s.nlargest(k).index.tolist()` keeps the largest-first order."),
    ("test_count_values", "Convert the counts to plain ints in a dict."),
],
},
# ---------------------------------------------------------------- read-csv-io
{
"slug": "read-csv-io", "title": "Reading and Writing CSV",
"difficulty": "beginner", "prereqs": ["dataframe-basics", "files-and-json"], "packages": ["pandas", "numpy"],
"objectives": ["Read CSV text with pd.read_csv and an in-memory io.StringIO buffer",
               "Check the dtypes pandas inferred", "Write a DataFrame back to CSV without its index",
               "Compare pandas parsing with the csv module"],
"tags": ["read-csv", "io", "dtypes", "csv"],
"sources": ["S085", "S055", "S008"], "entry": "parse_manual(text); parse_pandas(text); numeric_means(df); to_csv_text(df)",
"article": r'''
# Reading and Writing CSV

## Intuition
In [[files-and-json]] you read a CSV with `csv.DictReader` and converted every number yourself.
`pd.read_csv` does the reading, splitting, quoting **and** type conversion in one call, and
returns a DataFrame ready for analysis.

## Precise explanation
```python
import io
import pandas as pd
text = "name,score,passed\nada,91,True\nbob,78,False\n"
df = pd.read_csv(io.StringIO(text))     # a file path works the same way
df.dtypes      # name: string-like, score: int64, passed: bool
df.to_csv(index=False)                  # back to CSV text
```
* `io.StringIO(text)` wraps a string so it behaves like an open file; tests use it so no files
  are needed. `pd.read_csv("data.csv")` reads from disk.
* pandas **infers** dtypes: whole numbers → `int64`, decimals → `float64`, `True`/`False` →
  `bool`, text → `object` (pandas 2) or `str` (pandas 3). An empty field becomes `NaN`, which
  turns an integer column into `float64`.
* Useful options: `sep=";"`, `usecols=[...]`, `dtype={"zip": str}` (keep leading zeros),
  `na_values=["?"]`.
* `df.to_csv(index=False)` omits the row numbers, which are rarely wanted in a file.

## Worked example
`"a,b\n1,2.5\n3,\n"` → column `a` is `int64` `[1, 3]`; column `b` is `float64` `[2.5, NaN]`.

## Common mistakes
* Forgetting `index=False` and getting an extra unnamed column when reading the file back.
* Leading zeros lost: `"007"` is read as the integer 7 unless you pass `dtype=str`.
* Checking `df.dtypes == object` for text, which fails on pandas 3; use
  `pd.api.types.is_string_dtype`.

## Why this matters
Almost every dataset in practice starts as a CSV; knowing what `read_csv` infers prevents silent
type bugs before modelling.
''',
"statement": r'''
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
''',
"starter": r'''
import csv
import io

import pandas as pd


def _convert(value):
    # TODO: int, then float, else the original string
    return value


def parse_manual(text):
    # TODO
    return []


def parse_pandas(text):
    # TODO
    return pd.DataFrame()


def numeric_means(df):
    # TODO
    return {}


def to_csv_text(df):
    # TODO
    return df.to_csv()
''',
"hints": [
    "In `_convert`, use `try: return int(value)` / `except ValueError:` then the same with float.",
    "`[{k: _convert(v) for k, v in row.items()} for row in csv.DictReader(io.StringIO(text))]`.",
    "`num = df.select_dtypes(include=\"number\")`; `{c: float(num[c].mean()) for c in num.columns}`; `df.to_csv(index=False)`.",
],
"solution": r'''
import csv
import io

import pandas as pd


def _convert(value):
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        return value


def parse_manual(text):
    rows = csv.DictReader(io.StringIO(text))
    return [{k: _convert(v) for k, v in row.items()} for row in rows]


def parse_pandas(text):
    return pd.read_csv(io.StringIO(text))


def numeric_means(df):
    num = df.select_dtypes(include="number")
    return {str(c): float(num[c].mean()) for c in num.columns}


def to_csv_text(df):
    return df.to_csv(index=False)
''',
"explanation": r'''
The manual parser shows what `read_csv` automates: splitting with quote handling (delegated to
the csv module) and per-value type inference. pandas infers one dtype per column, so the numeric
selection keeps only number columns (booleans are a separate dtype). Writing with `index=False`
makes the text round-trip back to an identical DataFrame.
''',
"tests": r'''
import io

import pandas as pd

TEXT = "name,score,height,passed\nada,91,1.68,True\nbob,78,1.80,False\n\"lee, jo\",85,1.75,True\n"


class TestReadCsv(unittest.TestCase):
    def test_manual(self):
        rows = S.parse_manual(TEXT)
        self.assertEqual(rows[0], {"name": "ada", "score": 91, "height": 1.68, "passed": "True"})
        self.assertEqual(rows[2]["name"], "lee, jo")
        self.assertIs(type(rows[1]["score"]), int)

    def test_pandas_dtypes(self):
        df = S.parse_pandas(TEXT)
        self.assertEqual(df.shape, (3, 4))
        self.assertTrue(pd.api.types.is_integer_dtype(df["score"]))
        self.assertTrue(pd.api.types.is_float_dtype(df["height"]))
        self.assertTrue(pd.api.types.is_bool_dtype(df["passed"]))
        self.assertTrue(pd.api.types.is_string_dtype(df["name"]))

    def test_manual_matches_pandas(self):
        df = S.parse_pandas(TEXT)
        manual = S.parse_manual(TEXT)
        self.assertEqual([r["score"] for r in manual], df["score"].tolist())
        self.assertEqual([r["name"] for r in manual], df["name"].tolist())

    def test_missing_becomes_float(self):
        df = S.parse_pandas("a,b\n1,2.5\n3,\n")
        self.assertTrue(pd.api.types.is_integer_dtype(df["a"]))
        self.assertTrue(df["b"].isna().iloc[1])

    def test_numeric_means(self):
        means = S.numeric_means(S.parse_pandas(TEXT))
        self.assertEqual(sorted(means), ["height", "score"])
        self.assertAlmostEqual(means["score"], 254 / 3)
        self.assertAlmostEqual(means["height"], (1.68 + 1.80 + 1.75) / 3)

    def test_round_trip(self):
        df = S.parse_pandas(TEXT)
        text = S.to_csv_text(df)
        self.assertTrue(text.startswith("name,score,height,passed\n"))
        pd.testing.assert_frame_equal(pd.read_csv(io.StringIO(text)), df)
''',
"feedback": [
    ("test_manual", "Try `int`, then `float`, otherwise keep the string; use DictReader so quoted commas survive."),
    ("test_pandas_dtypes", "Use `pd.read_csv(io.StringIO(text))` with no extra options."),
    ("test_numeric_means", "Select numeric columns with `select_dtypes(include=\"number\")`; booleans are excluded."),
    ("test_round_trip", "Write with `index=False`."),
],
},
# ---------------------------------------------------------------- missing-values
{
"slug": "missing-values", "title": "Finding and Handling Missing Values",
"difficulty": "beginner", "prereqs": ["derived-columns"], "packages": ["pandas", "numpy"],
"objectives": ["Detect missing values with isna and count them per column",
               "Drop incomplete rows only for the columns that matter",
               "Fill missing values with per-column defaults",
               "Explain how pandas reductions skip NaN, compared with a manual loop"],
"tags": ["missing-values", "isna", "dropna", "fillna", "nan"],
"sources": ["S086", "S008"], "entry": "missing_report(df); drop_incomplete(df, cols); fill_defaults(df, defaults); mean_skipping_missing(values)",
"article": r'''
# Finding and Handling Missing Values

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
  "was missing" flag ([[fill-missing-group]]).
* Forgetting `reset_index(drop=True)` and then being surprised by gaps in the index.

## Why this matters
Most ML models cannot accept NaN, and the way you fill gaps changes the results; leakage from
filling with statistics of the whole dataset is covered in [[standard-scaler]].
''',
"statement": r'''
Implement:

1. `missing_report(df)` — dict column → number of missing values (`int`), for every column.
2. `drop_incomplete(df, cols)` — drop rows missing any of `cols`; reset the index.
3. `fill_defaults(df, defaults)` — fill missing values using the dict `defaults` (columns not in
   the dict are unchanged); do not modify `df`.
4. `mean_skipping_missing(values)` — plain-Python mean of a list that may contain `None` or
   `float("nan")`, skipping those; return `None` if nothing is left. (Use `math.isnan` for floats.)

**Example**
```python
df = pd.DataFrame({"age": [20, None, 31], "city": ["A", "B", None]})
missing_report(df)                # {'age': 1, 'city': 1}
mean_skipping_missing([20, None, 31, float("nan")])   # 25.5
```
''',
"starter": r'''
import math

import pandas as pd


def missing_report(df):
    # TODO
    return {}


def drop_incomplete(df, cols):
    # TODO
    return df


def fill_defaults(df, defaults):
    # TODO
    return df


def mean_skipping_missing(values):
    # TODO
    return None
''',
"hints": [
    "`{str(c): int(n) for c, n in df.isna().sum().items()}`.",
    "`df.dropna(subset=list(cols)).reset_index(drop=True)` and `df.fillna(defaults)`.",
    "Skip `v is None` and floats where `math.isnan(v)`; divide the sum by the count of kept values.",
],
"solution": r'''
import math

import pandas as pd


def missing_report(df):
    return {str(c): int(n) for c, n in df.isna().sum().items()}


def drop_incomplete(df, cols):
    return df.dropna(subset=list(cols)).reset_index(drop=True)


def fill_defaults(df, defaults):
    return df.fillna(defaults)


def mean_skipping_missing(values):
    kept = [v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    if not kept:
        return None
    return sum(kept) / len(kept)
''',
"explanation": r'''
`isna().sum()` counts True values per column. `dropna(subset=...)` limits the check to the
columns that matter, and `fillna` with a dict applies a different default per column while
returning a new frame. The manual mean shows what `skipna=True` does inside pandas.
''',
"tests": r'''
import numpy as np
import pandas as pd


def frame():
    return pd.DataFrame({"age": [20, None, 31, np.nan], "city": ["A", "B", None, "D"],
                         "score": [1.0, 2.0, 3.0, 4.0]})


class TestMissing(unittest.TestCase):
    def test_report(self):
        self.assertEqual(S.missing_report(frame()), {"age": 2, "city": 1, "score": 0})

    def test_drop_subset(self):
        out = S.drop_incomplete(frame(), ["age"])
        self.assertEqual(out["age"].tolist(), [20.0, 31.0])
        self.assertEqual(out.index.tolist(), [0, 1])

    def test_drop_two_columns(self):
        out = S.drop_incomplete(frame(), ["age", "city"])
        self.assertEqual(out["age"].tolist(), [20.0])

    def test_fill_defaults(self):
        df = frame()
        out = S.fill_defaults(df, {"age": 0, "city": "unknown"})
        self.assertEqual(out["age"].tolist(), [20.0, 0.0, 31.0, 0.0])
        self.assertEqual(out["city"].tolist(), ["A", "B", "unknown", "D"])
        self.assertEqual(int(df["age"].isna().sum()), 2)

    def test_manual_mean(self):
        self.assertEqual(S.mean_skipping_missing([20, None, 31, float("nan")]), 25.5)
        self.assertIsNone(S.mean_skipping_missing([None, float("nan")]))

    def test_manual_matches_pandas(self):
        values = [3.5, None, -1.0, float("nan"), 10.0]
        self.assertAlmostEqual(S.mean_skipping_missing(values), pd.Series(values, dtype=float).mean())
''',
"feedback": [
    ("test_report", "Count with `df.isna().sum()` and convert to a dict of ints."),
    ("test_drop_subset", "Pass `subset=` to dropna and reset the index."),
    ("test_fill_defaults", "`df.fillna(defaults)` returns a new frame; do not fill in place."),
    ("test_manual_mean", "Skip None and NaN values; return None when nothing is left."),
],
},
# ---------------------------------------------------------------- datetime-basics
{
"slug": "datetime-basics", "title": "Working with Dates",
"difficulty": "intermediate", "prereqs": ["string-cleaning"], "packages": ["pandas", "numpy"],
"objectives": ["Parse ISO date strings with pd.to_datetime and an explicit format",
               "Extract parts with the .dt accessor", "Subtract dates to get durations in days",
               "Compare pandas date arithmetic with the datetime module"],
"tags": ["datetime", "to-datetime", "dt-accessor", "timedelta"],
"sources": ["S087", "S008"], "entry": "days_between_manual(start, end); parse_dates(df, col); add_date_parts(df, col); add_duration(df, start, end); in_month(df, col, year, month)",
"article": r'''
# Working with Dates

## Intuition
`"2026-03-09"` is just text until you convert it to a date. Once converted, you can ask which
weekday it was, how many days separate two dates, or keep only March — and you can sort and
resample by time ([[resample-weekly]]).

## Precise explanation
**Standard library**: `datetime.date.fromisoformat("2026-03-09")` gives a `date`; subtracting two
dates gives a `timedelta` whose `.days` is the gap.

**pandas**
```python
dates = pd.to_datetime(df["date"], format="%Y-%m-%d")   # Series of datetime64
dates.dt.year, dates.dt.month, dates.dt.day_name()       # parts, element-wise
(end - start).dt.days                                    # durations in whole days
```
* Give `format=` when you know it: parsing is faster and an unexpected string raises an error
  instead of being guessed (`03/04` could be 3 April or 4 March).
* The `.dt` accessor works on datetime Series like `.str` works on text.
* `dt.dayofweek` is 0 for Monday … 6 for Sunday.
* Comparisons work directly: `dates >= "2026-03-01"`.

## Worked example
Start `2026-02-26`, end `2026-03-02`: 2026 is not a leap year, so February has 28 days and the gap
is 4 days. `pd.Timestamp("2026-03-02").day_name()` is `'Monday'`.

## Common mistakes
* Leaving dates as strings, so sorting `"2026-10-01"` vs `"2026-9-30"` is alphabetical.
* Ambiguous formats parsed without `format=`.
* Expecting `.dt.days` on a datetime column; it exists on durations (timedelta).

## Why this matters
Time-series features, train/test splits by time and resampling all start with correctly parsed
dates.
''',
"statement": r'''
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
''',
"starter": r'''
import datetime

import pandas as pd


def days_between_manual(start, end):
    # TODO
    return 0


def parse_dates(df, col):
    # TODO
    return df


def add_date_parts(df, col):
    # TODO
    return df


def add_duration(df, start, end):
    # TODO
    return df


def in_month(df, col, year, month):
    # TODO
    return df
''',
"hints": [
    "`(datetime.date.fromisoformat(end) - datetime.date.fromisoformat(start)).days`.",
    "`df.assign(**{col: pd.to_datetime(df[col], format=\"%Y-%m-%d\")})` returns a copy.",
    "`d = df[col].dt`; `df.assign(year=d.year, month=d.month, weekday=d.day_name())`; filter with `(d.year == year) & (d.month == month)`.",
],
"solution": r'''
import datetime

import pandas as pd


def days_between_manual(start, end):
    return (datetime.date.fromisoformat(end) - datetime.date.fromisoformat(start)).days


def parse_dates(df, col):
    return df.assign(**{col: pd.to_datetime(df[col], format="%Y-%m-%d")})


def add_date_parts(df, col):
    d = df[col].dt
    return df.assign(year=d.year, month=d.month, weekday=d.day_name())


def add_duration(df, start, end):
    s = pd.to_datetime(df[start], format="%Y-%m-%d")
    e = pd.to_datetime(df[end], format="%Y-%m-%d")
    return df.assign(days=(e - s).dt.days)


def in_month(df, col, year, month):
    d = df[col].dt
    return df[(d.year == year) & (d.month == month)].reset_index(drop=True)
''',
"explanation": r'''
Parsing with an explicit format converts text into datetime values once; afterwards the `.dt`
accessor extracts parts element-wise and subtraction produces timedeltas whose `.dt.days` gives
whole days. The manual version shows the same calculation for a single pair with the standard
library.
''',
"tests": r'''
import pandas as pd


def trips():
    return pd.DataFrame({"start": ["2026-02-26", "2024-02-28", "2026-03-09"],
                         "end": ["2026-03-02", "2024-03-01", "2026-03-09"]})


class TestDates(unittest.TestCase):
    def test_manual(self):
        self.assertEqual(S.days_between_manual("2026-02-26", "2026-03-02"), 4)
        self.assertEqual(S.days_between_manual("2024-02-28", "2024-03-01"), 2)

    def test_parse(self):
        df = trips()
        out = S.parse_dates(df, "start")
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(out["start"]))
        self.assertTrue(pd.api.types.is_string_dtype(df["start"]))

    def test_parse_rejects_bad_format(self):
        with self.assertRaises((ValueError, TypeError)):
            S.parse_dates(pd.DataFrame({"d": ["03/04/2026"]}), "d")

    def test_parts(self):
        out = S.add_date_parts(S.parse_dates(trips(), "end"), "end")
        self.assertEqual(out["year"].tolist(), [2026, 2024, 2026])
        self.assertEqual(out["month"].tolist(), [3, 3, 3])
        self.assertEqual(out["weekday"].tolist(), ["Monday", "Friday", "Monday"])

    def test_duration_matches_manual(self):
        df = trips()
        out = S.add_duration(df, "start", "end")
        manual = [S.days_between_manual(s, e) for s, e in zip(df["start"], df["end"])]
        self.assertEqual(out["days"].tolist(), manual)
        self.assertEqual(manual, [4, 2, 0])

    def test_in_month(self):
        df = S.parse_dates(trips(), "start")
        out = S.in_month(df, "start", 2026, 3)
        self.assertEqual(len(out), 1)
        self.assertEqual(out.index.tolist(), [0])
        self.assertEqual(len(S.in_month(df, "start", 2026, 2)), 1)
''',
"feedback": [
    ("test_manual", "Convert both strings with `datetime.date.fromisoformat` and take `.days` of the difference."),
    ("test_parse_rejects_bad_format", "Pass `format=\"%Y-%m-%d\"` so a different format raises instead of being guessed."),
    ("test_parts", "Use `.dt.year`, `.dt.month` and `.dt.day_name()`."),
    ("test_duration_matches_manual", "Parse both columns, subtract, and use `.dt.days`."),
    ("test_in_month", "Combine the year and month conditions with `&` and reset the index."),
],
},
]
