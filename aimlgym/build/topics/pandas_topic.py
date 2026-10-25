"""Problem definitions for the pandas topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- dataframe-basics
{
"slug": "dataframe-basics", "title": "Build and Describe a DataFrame",
"difficulty": "beginner", "prereqs": ["series-basics"], "packages": ["pandas", "numpy"],
"objectives": ["Create a DataFrame from a dict of columns", "Inspect shape, columns and dtypes",
               "Identify numeric columns"],
"tags": ["dataframe", "dtypes", "inspection"],
"sources": ["S008"], "entry": "make_df(data); describe_df(df)",
"article": r'''
# Series and DataFrames

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
* Assuming the index is 0..n−1 after filtering (see [[select-filter]]'s `reset_index`).

## Why this matters
Almost every real dataset arrives as a table; inspecting shape and dtypes catches problems such
as numbers stored as strings before they break a model.
''',
"statement": r'''
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
''',
"starter": r'''
import pandas as pd


def make_df(data):
    # TODO
    pass


def describe_df(df):
    # TODO
    return {}
''',
"hints": [
    "Check `len(set(len(v) for v in data.values())) == 1`.",
    "`pd.DataFrame(data)` builds the table.",
    "`list(df.select_dtypes(include='number').columns)`.",
],
"solution": r'''
import pandas as pd


def make_df(data):
    if not data:
        raise ValueError("data must not be empty")
    if len({len(v) for v in data.values()}) != 1:
        raise ValueError("all columns must have the same length")
    return pd.DataFrame(data)


def describe_df(df):
    return {
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": [str(c) for c in df.columns],
        "numeric": [str(c) for c in df.select_dtypes(include="number").columns],
    }
''',
"explanation": r'''
Validation gives a clear message before pandas does. `describe_df` reads the shape and column
labels, and `select_dtypes` filters numeric columns (ints and floats, but not booleans or strings).
''',
"tests": r'''
import pandas as pd

D = {"name": ["ann", "bob"], "score": [91.5, 78.0], "year": [1, 2]}

class TestBasics(unittest.TestCase):
    def test_make(self):
        df = S.make_df(D)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df["score"].tolist(), [91.5, 78.0])

    def test_describe(self):
        self.assertEqual(S.describe_df(S.make_df(D)),
                         {"n_rows": 2, "n_cols": 3, "columns": ["name", "score", "year"],
                          "numeric": ["score", "year"]})

    def test_unequal(self):
        with self.assertRaises(ValueError):
            S.make_df({"a": [1, 2], "b": [1]})

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.make_df({})

    def test_no_numeric(self):
        self.assertEqual(S.describe_df(S.make_df({"x": ["a", "b"]}))["numeric"], [])

    def test_bool_not_numeric(self):
        d = S.describe_df(S.make_df({"flag": [True, False], "v": [1, 2]}))
        self.assertEqual(d["numeric"], ["v"])
''',
"feedback": [
    ("test_describe", "Return plain lists/ints; use select_dtypes(include='number')."),
    ("test_unequal", "Check every column list has the same length."),
    ("test_bool_not_numeric", "Booleans are not selected by include='number'."),
    ("test_make", "Return pd.DataFrame(data)."),
],
},
# ---------------------------------------------------------------- select-filter
{
"slug": "select-filter", "title": "Select and Filter Rows",
"difficulty": "beginner", "prereqs": ["read-csv-io"], "packages": ["pandas", "numpy"],
"objectives": ["Filter rows with boolean masks and isin", "Select columns with .loc",
               "Reset the index after filtering"],
"tags": ["filtering", "loc", "isin", "boolean-indexing"],
"sources": ["S008"], "entry": "filter_students(df, min_score, cities, cols)",
"article": r'''
# Selecting and Filtering

## Intuition
Filtering a DataFrame is NumPy masking with labels: build a True/False Series per row, keep the
Trues, and pick the columns you want.

## Precise explanation
* `df["score"] >= 60` → boolean Series aligned with the index.
* Combine with `&`, `|`, `~` and parentheses (as in [[boolean-mask]]).
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
''',
"statement": r'''
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
''',
"starter": r'''
import pandas as pd


def filter_students(df, min_score, cities, cols):
    # TODO
    pass
''',
"hints": [
    "`mask = (df['score'] >= min_score) & df['city'].isin(cities)`.",
    "`df.loc[mask, cols]`.",
    "Finish with `.reset_index(drop=True)`.",
],
"solution": r'''
import pandas as pd


def filter_students(df, min_score, cities, cols):
    mask = (df["score"] >= min_score) & df["city"].isin(cities)
    return df.loc[mask, list(cols)].reset_index(drop=True)
''',
"explanation": r'''
One mask combines both conditions; `.loc` applies it together with the column list, and
`reset_index(drop=True)` discards the old labels.
''',
"tests": r'''
import pandas as pd

DF = pd.DataFrame({"name": ["ann", "bob", "cy", "dee"], "city": ["Pune", "Delhi", "Pune", "Chennai"],
                   "score": [72, 90, 55, 61]})

class TestFilter(unittest.TestCase):
    def test_example(self):
        out = S.filter_students(DF, 60, ["Pune", "Chennai"], ["name", "score"])
        pd.testing.assert_frame_equal(out, pd.DataFrame({"name": ["ann", "dee"], "score": [72, 61]}),
                                      check_dtype=False)

    def test_inclusive(self):
        self.assertEqual(S.filter_students(DF, 61, ["Chennai"], ["name"])["name"].tolist(), ["dee"])

    def test_none(self):
        out = S.filter_students(DF, 100, ["Pune"], ["name"])
        self.assertEqual(len(out), 0)
        self.assertEqual(list(out.columns), ["name"])

    def test_index_reset(self):
        out = S.filter_students(DF, 0, ["Pune"], ["name"])
        self.assertEqual(list(out.index), [0, 1])

    def test_column_order(self):
        out = S.filter_students(DF, 0, ["Delhi"], ["score", "name"])
        self.assertEqual(list(out.columns), ["score", "name"])

    def test_input_unchanged(self):
        before = DF.copy()
        S.filter_students(DF, 60, ["Pune"], ["name"])
        pd.testing.assert_frame_equal(DF, before)

    def test_missing_col(self):
        with self.assertRaises(KeyError):
            S.filter_students(DF, 0, ["Pune"], ["age"])
''',
"feedback": [
    ("test_example", "Combine masks with & and use isin for the city list."),
    ("test_inclusive", "Use >= for min_score."),
    ("test_index_reset", "Call reset_index(drop=True)."),
    ("test_column_order", "Select columns in the order given by cols."),
],
},
# ---------------------------------------------------------------- derived-columns
{
"slug": "derived-columns", "title": "Derived Columns",
"difficulty": "beginner", "prereqs": ["select-filter"], "packages": ["pandas", "numpy"],
"objectives": ["Create columns from vectorised arithmetic", "Handle division by zero as NaN",
               "Return a new DataFrame with assign"],
"tags": ["feature-engineering", "assign", "missing-values"],
"sources": ["S008"], "entry": "add_features(df)",
"article": r'''
# Derived Columns

## Intuition
Feature engineering often means combining existing columns: totals, ratios, flags. In pandas
these are whole-column operations — no loops.

## Precise explanation
* Arithmetic between Series is element-wise and aligned by index: `df["a"] + df["b"]`.
* `df.assign(new=expr, ...)` returns a **new** DataFrame, leaving the original untouched —
  preferable to mutating inputs inside functions.
* Division by zero in pandas floats gives `inf` (or NaN for 0/0). To mark "undefined" ratios as
  missing, replace with NaN: `(df.a / df.b).where(df.b != 0)` (`where` keeps values where the
  condition is True and puts NaN elsewhere).
* Comparisons produce boolean columns: `df["total"] >= 50`.

## Worked example
a = [30, 10, 0], b = [20, 0, 0] → total [50, 10, 0]; ratio [1.5, NaN, NaN]; passed
[True, False, False].

## Common mistakes
* Mutating the caller's DataFrame (`df["x"] = ...` inside the function).
* Leaving `inf` in features — many models crash or behave badly.
* Using `apply(lambda row: ...)` row by row (slow and unnecessary).

## Why this matters
Derived features are where domain knowledge enters a model; safe handling of undefined values
avoids silent NaN/inf propagation.
''',
"statement": r'''
Write `add_features(df)` for a DataFrame with numeric columns `a` and `b`. Return a **new**
DataFrame with extra columns:
* `total = a + b`
* `ratio = a / b`, NaN where `b == 0`
* `passed = total >= 50` (boolean)

The input must not be modified.

**Example**
```python
add_features(pd.DataFrame({"a": [30, 10, 0], "b": [20, 0, 0]}))
#     a   b  total  ratio  passed
# 0  30  20     50    1.5    True
# 1  10   0     10    NaN   False
# 2   0   0      0    NaN   False
```
''',
"starter": r'''
import numpy as np
import pandas as pd


def add_features(df):
    # TODO: return df.assign(...)
    pass
''',
"hints": [
    "`total = df['a'] + df['b']`.",
    "`ratio = (df['a'] / df['b']).where(df['b'] != 0)`.",
    "Use `df.assign(total=..., ratio=..., passed=...)`; compute passed from total.",
],
"solution": r'''
import numpy as np
import pandas as pd


def add_features(df):
    total = df["a"] + df["b"]
    ratio = (df["a"] / df["b"]).where(df["b"] != 0)
    return df.assign(total=total, ratio=ratio, passed=total >= 50)
''',
"explanation": r'''
All three features are vectorised column expressions. `where(b != 0)` converts the undefined
ratios (inf and NaN from division by zero) into NaN. `assign` returns a new frame, so the input is
unchanged.
''',
"tests": r'''
import numpy as np
import pandas as pd

DF = pd.DataFrame({"a": [30, 10, 0], "b": [20, 0, 0]})

class TestFeatures(unittest.TestCase):
    def test_total(self):
        self.assertEqual(S.add_features(DF)["total"].tolist(), [50, 10, 0])

    def test_ratio_nan(self):
        r = S.add_features(DF)["ratio"]
        self.assertAlmostEqual(r.iloc[0], 1.5)
        self.assertTrue(np.isnan(r.iloc[1]) and np.isnan(r.iloc[2]))

    def test_no_inf(self):
        self.assertFalse(np.isinf(S.add_features(DF)["ratio"].to_numpy(dtype=float)).any())

    def test_passed(self):
        self.assertEqual(S.add_features(DF)["passed"].tolist(), [True, False, False])

    def test_columns(self):
        self.assertEqual(list(S.add_features(DF).columns), ["a", "b", "total", "ratio", "passed"])

    def test_not_mutated(self):
        d = DF.copy()
        S.add_features(d)
        self.assertEqual(list(d.columns), ["a", "b"])

    def test_negative_b(self):
        out = S.add_features(pd.DataFrame({"a": [6], "b": [-3]}))
        self.assertAlmostEqual(out["ratio"].iloc[0], -2.0)
''',
"feedback": [
    ("test_ratio_nan", "Mask the ratio where b == 0 using .where(df['b'] != 0)."),
    ("test_no_inf", "Division by zero gives inf — replace it with NaN."),
    ("test_not_mutated", "Use df.assign (returns a new frame) instead of df['x'] = ..."),
    ("test_passed", "passed is total >= 50 (inclusive)."),
],
},
# ---------------------------------------------------------------- sort-rank
{
"slug": "sort-rank", "title": "Sort and Rank",
"difficulty": "intermediate", "prereqs": ["missing-values"], "packages": ["pandas", "numpy"],
"objectives": ["Sort by several columns with different directions", "Rank with ties (method='min')",
               "Take the top-n rows"],
"tags": ["sorting", "ranking", "ties"],
"sources": ["S008"], "entry": "leaderboard(df, n=None)",
"article": r'''
# Sorting and Ranking

## Intuition
A leaderboard sorts by score (highest first) and assigns ranks. When two people tie, they share
a rank and the next rank is skipped (1, 2, 2, 4) — "competition ranking".

## Precise explanation
* `df.sort_values(["score", "name"], ascending=[False, True])` sorts by score descending and
  breaks ties by name ascending. Use `kind="mergesort"` (stable) when order of equal keys matters.
* `df["score"].rank(method="min", ascending=False)` gives competition ranks: tied values get the
  smallest rank of their group. Other methods: `"dense"` (1, 2, 2, 3), `"average"` (1, 2.5, 2.5, 4),
  `"first"` (by appearance).
* Ranks are floats; convert with `.astype(int)` when there are no NaNs.
* `df.head(n)` keeps the first n rows after sorting.

## Worked example
scores ann 90, bob 85, cy 90, dee 70 → sorted ann 90, cy 90, bob 85, dee 70 → ranks 1, 1, 3, 4.

## Common mistakes
* `ascending=False` for both keys, reversing the alphabetical tie-break.
* Using `method="dense"` when competition ranking is required (or vice versa).
* Ranking before filtering, then wondering why ranks have gaps.

## Why this matters
Ranking metrics (precision@k), feature importance tables ([[top-k-attributions]]) and leaderboards all require
correct, deterministic tie handling.
''',
"statement": r'''
Write `leaderboard(df, n=None)` for columns `name` and `score`. Return a new DataFrame:
* sorted by `score` descending, then `name` ascending,
* with an `int` column `rank` using competition ranking (`method="min"`) on score,
* index reset to 0..k−1, keeping only the first `n` rows if `n` is given (ties beyond row n are
  cut).

**Example**
```python
leaderboard(pd.DataFrame({"name": ["bob", "ann", "dee", "cy"], "score": [85, 90, 70, 90]}))
#   name  score  rank
# 0  ann     90     1
# 1   cy     90     1
# 2  bob     85     3
# 3  dee     70     4
```
''',
"starter": r'''
import pandas as pd


def leaderboard(df, n=None):
    # TODO
    pass
''',
"hints": [
    "`out = df.sort_values(['score', 'name'], ascending=[False, True])`.",
    "`out['rank'] = out['score'].rank(method='min', ascending=False).astype(int)` on the copy.",
    "`reset_index(drop=True)` and `head(n)` if n is not None.",
],
"solution": r'''
import pandas as pd


def leaderboard(df, n=None):
    out = df.sort_values(["score", "name"], ascending=[False, True], kind="mergesort")
    out = out.assign(rank=out["score"].rank(method="min", ascending=False).astype(int))
    out = out.reset_index(drop=True)
    return out if n is None else out.head(n)
''',
"explanation": r'''
A two-key stable sort gives the display order; ranking on the score column with `method="min"`
assigns shared ranks to ties and skips the following rank. `assign` keeps the input untouched.
''',
"tests": r'''
import pandas as pd

DF = pd.DataFrame({"name": ["bob", "ann", "dee", "cy"], "score": [85, 90, 70, 90]})

class TestLeaderboard(unittest.TestCase):
    def test_order(self):
        self.assertEqual(S.leaderboard(DF)["name"].tolist(), ["ann", "cy", "bob", "dee"])

    def test_ranks(self):
        self.assertEqual(S.leaderboard(DF)["rank"].tolist(), [1, 1, 3, 4])

    def test_rank_int(self):
        self.assertTrue(pd.api.types.is_integer_dtype(S.leaderboard(DF)["rank"]))

    def test_top_n(self):
        out = S.leaderboard(DF, n=2)
        self.assertEqual(out["name"].tolist(), ["ann", "cy"])

    def test_index(self):
        self.assertEqual(list(S.leaderboard(DF).index), [0, 1, 2, 3])

    def test_all_tied(self):
        out = S.leaderboard(pd.DataFrame({"name": ["z", "y"], "score": [5, 5]}))
        self.assertEqual(out["name"].tolist(), ["y", "z"])
        self.assertEqual(out["rank"].tolist(), [1, 1])

    def test_input_unchanged(self):
        before = DF.copy()
        S.leaderboard(DF)
        pd.testing.assert_frame_equal(DF, before)
''',
"feedback": [
    ("test_order", "ascending=[False, True]: score descending, name ascending."),
    ("test_ranks", "Use rank(method='min', ascending=False)."),
    ("test_rank_int", "Convert ranks to int with .astype(int)."),
    ("test_input_unchanged", "Don't add the rank column to the original DataFrame."),
],
},
# ---------------------------------------------------------------- groupby-agg
{
"slug": "groupby-agg", "title": "Group-by Aggregation",
"difficulty": "intermediate", "prereqs": ["sort-rank", "gradebook-aggregate"], "packages": ["pandas", "numpy"],
"objectives": ["Apply split–apply–combine", "Use named aggregations",
               "Return a tidy, sorted summary table"],
"tags": ["groupby", "aggregation", "split-apply-combine"],
"sources": ["S008"], "entry": "category_summary(df)",
"article": r'''
# Group-by: Split, Apply, Combine

## Intuition
"Average sale per category" means: **split** the rows by category, **apply** an aggregate to each
group, **combine** the results into a table — the pandas version of [[gradebook-aggregate]]'s manual grouping.

## Precise explanation
```python
df.groupby("category").agg(
    n=("value", "size"),
    total=("value", "sum"),
    mean=("value", "mean"),
).reset_index()
```
* **Named aggregation** `new_col=(source_col, func)` produces clear column names.
* `"size"` counts rows (including NaN values); `"count"` counts non-missing values.
* `groupby` sorts group keys by default (`sort=True`).
* `reset_index()` turns the group keys from the index back into a column.

```mermaid
flowchart LR
  T[table] --> S1[split by category]
  S1 --> A["apply: size/sum/mean"]
  A --> C[combine into summary]
```

## Worked example
category [a, b, a, b, a], value [1, 2, 3, NaN, 5] →
a: n 3, total 9, mean 3; b: n 2, count 1, total 2, mean 2.

## Common mistakes
* Confusing `size` and `count` with missing values.
* Forgetting `reset_index`, leaving keys in the index.
* Aggregating string columns with `mean`.

## Why this matters
Per-class accuracy, per-client data sizes in federated learning ([[weighted-fedavg]]) and per-user features
are group-bys.
''',
"statement": r'''
Write `category_summary(df)` for columns `category` and `value` (float, may contain NaN).
Return a DataFrame with columns `category, n, n_valid, total, mean`, one row per category sorted
by category, index 0..k−1, where `n` = rows, `n_valid` = non-missing values, `total` = sum
(NaN skipped), `mean` = mean of non-missing values.

**Example**
```python
category_summary(pd.DataFrame({"category": ["a", "b", "a", "b", "a"],
                               "value": [1, 2, 3, np.nan, 5]}))
#   category  n  n_valid  total  mean
# 0        a  3        3    9.0   3.0
# 1        b  2        1    2.0   2.0
```
''',
"starter": r'''
import numpy as np
import pandas as pd


def category_summary(df):
    # TODO
    pass
''',
"hints": [
    "`df.groupby('category')` then `.agg(...)` with named aggregations.",
    "`n=('value', 'size')`, `n_valid=('value', 'count')`.",
    "`total=('value', 'sum')`, `mean=('value', 'mean')`, then `.reset_index()`.",
],
"solution": r'''
import numpy as np
import pandas as pd


def category_summary(df):
    return (df.groupby("category", sort=True)
              .agg(n=("value", "size"), n_valid=("value", "count"),
                   total=("value", "sum"), mean=("value", "mean"))
              .reset_index())
''',
"explanation": r'''
One `groupby().agg()` call computes all four statistics with explicit output names. `size`
counts all rows while `count` skips NaN, which is exactly the difference between n and n_valid.
''',
"tests": r'''
import numpy as np
import pandas as pd

DF = pd.DataFrame({"category": ["a", "b", "a", "b", "a"], "value": [1, 2, 3, np.nan, 5]})

class TestGroupby(unittest.TestCase):
    def test_columns(self):
        self.assertEqual(list(S.category_summary(DF).columns), ["category", "n", "n_valid", "total", "mean"])

    def test_values(self):
        exp = pd.DataFrame({"category": ["a", "b"], "n": [3, 2], "n_valid": [3, 1],
                            "total": [9.0, 2.0], "mean": [3.0, 2.0]})
        pd.testing.assert_frame_equal(S.category_summary(DF), exp, check_dtype=False)

    def test_sorted(self):
        d = pd.DataFrame({"category": ["z", "m", "a"], "value": [1.0, 2.0, 3.0]})
        self.assertEqual(S.category_summary(d)["category"].tolist(), ["a", "m", "z"])

    def test_all_nan_group(self):
        d = pd.DataFrame({"category": ["x", "x"], "value": [np.nan, np.nan]})
        out = S.category_summary(d)
        self.assertEqual(out["n"].iloc[0], 2)
        self.assertEqual(out["n_valid"].iloc[0], 0)
        self.assertTrue(np.isnan(out["mean"].iloc[0]))

    def test_index(self):
        self.assertEqual(list(S.category_summary(DF).index), [0, 1])

    def test_single_group(self):
        out = S.category_summary(pd.DataFrame({"category": ["q"] * 4, "value": [1.0, 2, 3, 4]}))
        self.assertAlmostEqual(out["mean"].iloc[0], 2.5)
''',
"feedback": [
    ("test_values", "n uses 'size' (all rows); n_valid uses 'count' (non-missing)."),
    ("test_columns", "Use named aggregation and reset_index() so category is a column."),
    ("test_all_nan_group", "mean of all-NaN values is NaN; count is 0."),
    ("test_sorted", "groupby sorts keys by default; keep sort=True."),
],
},
# ---------------------------------------------------------------- fill-missing-group
{
"slug": "fill-missing-group", "title": "Fill Missing Values by Group",
"difficulty": "intermediate", "prereqs": ["groupby-agg"], "packages": ["pandas", "numpy"],
"objectives": ["Detect missing values", "Impute with group means via transform",
               "Fall back to a global statistic"],
"tags": ["missing-values", "imputation", "transform", "groupby"],
"sources": ["S008"], "entry": "impute_group_mean(df, group, col)",
"article": r'''
# Group-wise Imputation

## Intuition
A missing height is better guessed from people of the same age group than from everyone. Filling
NaN with a **group** mean keeps more structure than a single global mean.

## Precise explanation
* `s.isna()` marks missing values; `s.isna().sum()` counts them.
* `df.groupby(g)[col].transform("mean")` returns a Series **aligned with the original rows**: each
  row gets its own group's mean (unlike `agg`, which returns one row per group).
* `s.fillna(other)` replaces NaN positions with the matching values of `other`.
* If a whole group is missing, its group mean is NaN; fall back to the global mean
  `s.mean()` (NaN skipped).

## Worked example
g = [a, a, b, b, c], v = [1, NaN, 10, 20, NaN]:
group means a 1, b 15, c NaN; global mean (1+10+20)/3 ≈ 10.33 →
filled [1, 1, 10, 20, 10.33].

## Common mistakes
* Using `agg` and trying to align by position.
* Computing means *after* filling (leaks filled values into statistics).
* In ML, computing imputation statistics on the full dataset instead of the training split
  (data leakage; see [[standard-scaler]]).

## Why this matters
Real data has holes; principled imputation (and recording which values were imputed) is a core
preprocessing step.
''',
"statement": r'''
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
''',
"starter": r'''
import numpy as np
import pandas as pd


def impute_group_mean(df, group, col):
    # TODO
    pass
''',
"hints": [
    "`group_mean = df.groupby(group)[col].transform('mean')`.",
    "`filled = df[col].fillna(group_mean).fillna(df[col].mean())`.",
    "Use `df.assign(**{col: filled, f'{col}_was_missing': df[col].isna()})`.",
],
"solution": r'''
import numpy as np
import pandas as pd


def impute_group_mean(df, group, col):
    if df[col].isna().all():
        raise ValueError("column is entirely missing")
    group_mean = df.groupby(group)[col].transform("mean")
    filled = df[col].fillna(group_mean).fillna(df[col].mean())
    return df.assign(**{col: filled, f"{col}_was_missing": df[col].isna()})
''',
"explanation": r'''
`transform("mean")` broadcasts each group's mean back to its rows, so `fillna` can align it by
index. A second `fillna` with the global mean covers groups that have no observed values. The
indicator column records which values were imputed, computed from the original column.
''',
"tests": r'''
import numpy as np
import pandas as pd

DF = pd.DataFrame({"g": list("aabbc"), "v": [1, np.nan, 10, 20, np.nan]})

class TestImpute(unittest.TestCase):
    def test_values(self):
        out = S.impute_group_mean(DF, "g", "v")["v"].tolist()
        np.testing.assert_allclose(out, [1, 1, 10, 20, 31 / 3])

    def test_indicator(self):
        self.assertEqual(S.impute_group_mean(DF, "g", "v")["v_was_missing"].tolist(),
                         [False, True, False, False, True])

    def test_no_nan_left(self):
        self.assertFalse(S.impute_group_mean(DF, "g", "v")["v"].isna().any())

    def test_input_unchanged(self):
        d = DF.copy()
        S.impute_group_mean(d, "g", "v")
        self.assertTrue(np.isnan(d["v"].iloc[1]))

    def test_group_mean_not_global(self):
        d = pd.DataFrame({"g": ["x", "x", "y", "y"], "v": [100, np.nan, 0, np.nan]})
        self.assertEqual(S.impute_group_mean(d, "g", "v")["v"].tolist(), [100, 100, 0, 0])

    def test_all_missing(self):
        with self.assertRaises(ValueError):
            S.impute_group_mean(pd.DataFrame({"g": ["a"], "v": [np.nan]}), "g", "v")

    def test_nothing_missing(self):
        d = pd.DataFrame({"g": ["a", "b"], "v": [1.0, 2.0]})
        pd.testing.assert_series_equal(S.impute_group_mean(d, "g", "v")["v"], d["v"])
''',
"feedback": [
    ("test_values", "Use groupby().transform('mean') then fall back to the overall mean."),
    ("test_group_mean_not_global", "Fill with the group's mean, not the global mean."),
    ("test_indicator", "Compute the indicator from the original column before filling."),
    ("test_input_unchanged", "Return df.assign(...) rather than modifying df."),
],
},
# ---------------------------------------------------------------- merge-tables
{
"slug": "merge-tables", "title": "Merging Tables",
"difficulty": "intermediate", "prereqs": ["groupby-agg"], "packages": ["pandas", "numpy"],
"objectives": ["Join tables on a key with merge", "Choose inner vs left joins",
               "Validate join cardinality"],
"tags": ["merge", "join", "relational-data"],
"sources": ["S008"], "entry": "orders_with_customers(orders, customers); spend_per_customer(orders, customers)",
"article": r'''
# Merging Tables

## Intuition
Orders list a `customer_id`; customer details live in another table. A **join** looks up each
order's customer and attaches their columns — like VLOOKUP, but for whole tables.

## Precise explanation
`pd.merge(left, right, on="customer_id", how=...)`:
* `how="inner"` keeps keys present in both tables.
* `how="left"` keeps every left row; missing matches get NaN.
* `how="outer"` keeps keys from either side.
* `validate="many_to_one"` raises `MergeError` if the right table has duplicate keys — which
  would silently duplicate left rows.
* `indicator=True` adds a `_merge` column ("both", "left_only", "right_only") for debugging.

```mermaid
erDiagram
  CUSTOMERS ||--o{ ORDERS : places
  CUSTOMERS { int customer_id string name }
  ORDERS { int order_id int customer_id float amount }
```

## Worked example
orders (1, c1, 50), (2, c2, 20), (3, c9, 5); customers c1 Ann, c2 Bob →
left join: Ann, Bob, NaN→"unknown".

## Common mistakes
* Inner join silently dropping orders with unknown customers.
* Duplicate keys in a lookup table multiplying rows.
* Merging on columns with different dtypes (int vs string ids) → no matches.

## Why this matters
Features usually live in several tables (users, events, labels); correct joins prevent both lost
rows and duplicated labels.
''',
"statement": r'''
Implement:
* `orders_with_customers(orders, customers)` → left join of `orders` (`order_id, customer_id,
  amount`) with `customers` (`customer_id, name`) on `customer_id`, `validate="many_to_one"`,
  missing names filled with `"unknown"`, rows in original order with index 0..n−1.
  Duplicate customer ids must raise (pandas raises `pd.errors.MergeError`).
* `spend_per_customer(orders, customers)` → DataFrame `name, total` (sum of amounts per name,
  including `"unknown"`), sorted by `total` descending then `name` ascending.

**Example**
```python
orders = pd.DataFrame({"order_id": [1, 2, 3, 4], "customer_id": [1, 2, 9, 1], "amount": [50, 20, 5, 10]})
customers = pd.DataFrame({"customer_id": [1, 2], "name": ["Ann", "Bob"]})
orders_with_customers(orders, customers)["name"].tolist()   # ['Ann', 'Bob', 'unknown', 'Ann']
spend_per_customer(orders, customers)  # Ann 60, Bob 20, unknown 5
```
''',
"starter": r'''
import pandas as pd


def orders_with_customers(orders, customers):
    # TODO
    pass


def spend_per_customer(orders, customers):
    # TODO
    pass
''',
"hints": [
    "`pd.merge(orders, customers, on='customer_id', how='left', validate='many_to_one')`.",
    "`merged.assign(name=merged['name'].fillna('unknown'))`.",
    "Group by name, sum amount, then sort_values(['total', 'name'], ascending=[False, True]).",
],
"solution": r'''
import pandas as pd


def orders_with_customers(orders, customers):
    merged = pd.merge(orders, customers, on="customer_id", how="left", validate="many_to_one")
    return merged.assign(name=merged["name"].fillna("unknown")).reset_index(drop=True)


def spend_per_customer(orders, customers):
    m = orders_with_customers(orders, customers)
    out = m.groupby("name", as_index=False).agg(total=("amount", "sum"))
    return out.sort_values(["total", "name"], ascending=[False, True]).reset_index(drop=True)
''',
"explanation": r'''
A left join keeps every order; `validate` guards against duplicate customers, and missing
matches are labelled "unknown". The spend table groups the merged rows by name and sorts with a
deterministic tie-break.
''',
"tests": r'''
import pandas as pd

O = pd.DataFrame({"order_id": [1, 2, 3, 4], "customer_id": [1, 2, 9, 1], "amount": [50, 20, 5, 10]})
C = pd.DataFrame({"customer_id": [1, 2], "name": ["Ann", "Bob"]})

class TestMerge(unittest.TestCase):
    def test_names(self):
        self.assertEqual(S.orders_with_customers(O, C)["name"].tolist(), ["Ann", "Bob", "unknown", "Ann"])

    def test_row_count_kept(self):
        self.assertEqual(len(S.orders_with_customers(O, C)), 4)

    def test_order_ids(self):
        self.assertEqual(S.orders_with_customers(O, C)["order_id"].tolist(), [1, 2, 3, 4])

    def test_duplicate_customer(self):
        bad = pd.DataFrame({"customer_id": [1, 1], "name": ["Ann", "Ann2"]})
        with self.assertRaises(pd.errors.MergeError):
            S.orders_with_customers(O, bad)

    def test_spend(self):
        out = S.spend_per_customer(O, C)
        self.assertEqual(out["name"].tolist(), ["Ann", "Bob", "unknown"])
        self.assertEqual(out["total"].tolist(), [60, 20, 5])

    def test_spend_tie(self):
        o = pd.DataFrame({"order_id": [1, 2], "customer_id": [2, 1], "amount": [7, 7]})
        self.assertEqual(S.spend_per_customer(o, C)["name"].tolist(), ["Ann", "Bob"])

    def test_columns(self):
        self.assertEqual(list(S.spend_per_customer(O, C).columns), ["name", "total"])
''',
"feedback": [
    ("test_row_count_kept", "Use how='left' so orders without a customer are kept."),
    ("test_duplicate_customer", "Pass validate='many_to_one' to merge."),
    ("test_names", "Fill missing names with 'unknown' after the merge."),
    ("test_spend_tie", "Sort by total descending, then name ascending."),
],
},
# ---------------------------------------------------------------- string-cleaning
{
"slug": "string-cleaning", "title": "Cleaning Text Columns",
"difficulty": "intermediate", "prereqs": ["missing-values"], "packages": ["pandas", "numpy"],
"objectives": ["Use the .str accessor", "Normalise whitespace and case with regex",
               "Extract parts of strings and keep missing values missing"],
"tags": ["strings", "regex", "data-cleaning", "str-accessor"],
"sources": ["S008"], "entry": "clean_contacts(df)",
"article": r'''
# Cleaning Text Columns

## Intuition
Typed-in data is messy: "  Ann   LEE ", "ann lee", "+91 98-765 43210". Before you can join or
count, normalise it. The `.str` accessor applies string methods to a whole column at once.

## Precise explanation
* `s.str.strip()`, `s.str.lower()`, `s.str.title()`.
* Regex replace: `s.str.replace(r"\s+", " ", regex=True)` collapses runs of whitespace;
  `s.str.replace(r"\D", "", regex=True)` removes every non-digit.
* `s.str.split("@").str[1]` takes the part after "@" (NaN if absent).
* `s.str.contains("@", na=False)` for validity checks.
* Missing values stay missing through `.str` methods (they return NaN/NA rather than raising).

## Worked example
"  Ann   LEE " → strip → "Ann   LEE" → collapse → "Ann LEE" → title → "Ann Lee".
"+91 98-765 43210" → digits "919876543210".

## Common mistakes
* Calling Python string methods on the Series itself (`s.lower()` → AttributeError).
* Forgetting `regex=True` for patterns.
* Converting NaN to the string "nan" with `astype(str)`.

## Why this matters
Text normalisation precedes deduplication, joining on names, and NLP tokenisation ([[tokenize-normalize]]).
''',
"statement": r'''
Write `clean_contacts(df)` for columns `name`, `phone`, `email` (strings, may be missing).
Return a new DataFrame with:
* `name`: stripped, internal whitespace collapsed to one space, title case;
* `phone`: digits only;
* `email`: stripped and lower-cased;
* `domain`: the part after `@` in the cleaned email (missing if there is no `@`).
Missing inputs must remain missing (check with `pd.isna`).

**Example**
```python
clean_contacts(pd.DataFrame({"name": ["  ann   LEE "], "phone": ["+91 98-765 43210"],
                             "email": [" Ann.Lee@Example.COM "]})).iloc[0].tolist()
# ['Ann Lee', '919876543210', 'ann.lee@example.com', 'example.com']
```
''',
"starter": r'''
import pandas as pd


def clean_contacts(df):
    # TODO
    pass
''',
"hints": [
    "`df['name'].str.strip().str.replace(r'\\s+', ' ', regex=True).str.title()`.",
    "`df['phone'].str.replace(r'\\D', '', regex=True)`.",
    "`email.str.split('@').str[1]` — NaN when there is no '@'.",
],
"solution": r'''
import pandas as pd


def clean_contacts(df):
    name = df["name"].str.strip().str.replace(r"\s+", " ", regex=True).str.title()
    phone = df["phone"].str.replace(r"\D", "", regex=True)
    email = df["email"].str.strip().str.lower()
    parts = email.str.split("@")
    domain = parts.str[1].where(parts.str.len() > 1)
    return df.assign(name=name, phone=phone, email=email, domain=domain)
''',
"explanation": r'''
Each column is cleaned with a chain of vectorised `.str` operations. The domain is the second
element after splitting on '@'; `.where(len > 1)` keeps it missing when there was no '@'. Missing
inputs propagate as missing through every `.str` call.
''',
"tests": r'''
import numpy as np
import pandas as pd

DF = pd.DataFrame({"name": ["  ann   LEE ", "BOB", None],
                   "phone": ["+91 98-765 43210", "(044) 1234", None],
                   "email": [" Ann.Lee@Example.COM ", "bob-at-mail", None]})

class TestClean(unittest.TestCase):
    def test_row0(self):
        self.assertEqual(S.clean_contacts(DF).iloc[0][["name", "phone", "email", "domain"]].tolist(),
                         ["Ann Lee", "919876543210", "ann.lee@example.com", "example.com"])

    def test_title(self):
        self.assertEqual(S.clean_contacts(DF)["name"].iloc[1], "Bob")

    def test_phone_digits(self):
        self.assertEqual(S.clean_contacts(DF)["phone"].iloc[1], "0441234")

    def test_no_at_domain_missing(self):
        self.assertTrue(pd.isna(S.clean_contacts(DF)["domain"].iloc[1]))

    def test_missing_stays_missing(self):
        row = S.clean_contacts(DF).iloc[2]
        self.assertTrue(all(pd.isna(row[c]) for c in ["name", "phone", "email", "domain"]))

    def test_not_string_nan(self):
        self.assertNotIn("nan", S.clean_contacts(DF)["name"].dropna().str.lower().tolist())

    def test_input_unchanged(self):
        d = DF.copy()
        S.clean_contacts(d)
        self.assertEqual(d["name"].iloc[0], "  ann   LEE ")
''',
"feedback": [
    ("test_row0", "Collapse whitespace with str.replace(r'\\s+', ' ', regex=True) after strip."),
    ("test_phone_digits", r"Remove all non-digits with the regex \D."),
    ("test_no_at_domain_missing", "If there is no '@', domain must be missing, not the whole email."),
    ("test_missing_stays_missing", "Don't use astype(str); .str methods keep NaN as NaN."),
],
},
# ---------------------------------------------------------------- pivot-table
{
"slug": "pivot-table", "title": "Pivot Tables",
"difficulty": "advanced", "prereqs": ["groupby-agg"], "packages": ["pandas", "numpy"],
"objectives": ["Reshape long data to wide with pivot_table", "Fill missing cells",
               "Melt wide data back to long"],
"tags": ["pivot", "melt", "reshaping", "tidy-data"],
"sources": ["S008"], "entry": "sales_pivot(df); to_long(wide)",
"article": r'''
# Long vs Wide: Pivot and Melt

## Intuition
"Long" data has one row per observation (region, quarter, sales). "Wide" data has one row per
region and one column per quarter — easier for humans to read. Pivoting converts long → wide;
melting converts back.

## Precise explanation
```python
wide = pd.pivot_table(df, index="region", columns="quarter", values="sales",
                      aggfunc="sum", fill_value=0)
```
* Duplicate (region, quarter) pairs are combined by `aggfunc` (`pivot` without aggregation would
  raise on duplicates).
* `fill_value=0` fills combinations with no rows.
* `wide.columns.name` holds "quarter"; `rename_axis(columns=None)` removes it.
* `wide.reset_index().melt(id_vars="region", var_name="quarter", value_name="sales")` goes back
  to long form.

| region | quarter | sales |      | region | Q1 | Q2 |
|---|---|---|---|---|---|---|
| N | Q1 | 5 | → | N | 5 | 3 |
| N | Q2 | 3 |   | S | 7 | 0 |
| S | Q1 | 7 |   |   |   |   |

## Worked example
Above: the S/Q2 cell has no data → filled with 0.

## Common mistakes
* Using `pivot` with duplicate keys.
* Forgetting fill_value and getting NaN.
* Melting without `id_vars`, which melts the identifier too.

## Why this matters
Confusion matrices, user × item matrices for recommenders, and reporting tables are pivots.
''',
"statement": r'''
Implement:
* `sales_pivot(df)` → wide DataFrame from long columns `region, quarter, sales`: index =
  regions (sorted), columns = quarters (sorted), values = summed sales, missing = 0, integer
  dtype if `sales` is integer. Remove the columns-axis name (`rename_axis(columns=None)`).
* `to_long(wide)` → long DataFrame with columns `region, quarter, sales`, sorted by region then
  quarter, index 0..n−1 (zeros included).

**Example**
```python
df = pd.DataFrame({"region": ["N", "N", "S", "N"], "quarter": ["Q1", "Q2", "Q1", "Q1"],
                   "sales": [5, 3, 7, 2]})
sales_pivot(df)
#         Q1  Q2
# region
# N        7   3
# S        7   0
```
''',
"starter": r'''
import pandas as pd


def sales_pivot(df):
    # TODO
    pass


def to_long(wide):
    # TODO
    pass
''',
"hints": [
    "`pd.pivot_table(df, index='region', columns='quarter', values='sales', aggfunc='sum', fill_value=0)`.",
    "`.rename_axis(columns=None)` drops the 'quarter' label above the columns.",
    "`wide.reset_index().melt(id_vars='region', var_name='quarter', value_name='sales')`.",
],
"solution": r'''
import pandas as pd


def sales_pivot(df):
    wide = pd.pivot_table(df, index="region", columns="quarter", values="sales",
                          aggfunc="sum", fill_value=0)
    return wide.sort_index().sort_index(axis=1).rename_axis(columns=None)


def to_long(wide):
    long = wide.reset_index().melt(id_vars="region", var_name="quarter", value_name="sales")
    return long.sort_values(["region", "quarter"]).reset_index(drop=True)
''',
"explanation": r'''
`pivot_table` aggregates duplicate (region, quarter) pairs and fills empty cells. Sorting both
axes makes the output deterministic. `melt` reverses the reshape, keeping region as the id.
''',
"tests": r'''
import pandas as pd

DF = pd.DataFrame({"region": ["N", "N", "S", "N"], "quarter": ["Q1", "Q2", "Q1", "Q1"],
                   "sales": [5, 3, 7, 2]})

class TestPivot(unittest.TestCase):
    def test_values(self):
        w = S.sales_pivot(DF)
        self.assertEqual(w.loc["N", "Q1"], 7)
        self.assertEqual(w.loc["S", "Q2"], 0)

    def test_axes(self):
        w = S.sales_pivot(DF)
        self.assertEqual(list(w.index), ["N", "S"])
        self.assertEqual(list(w.columns), ["Q1", "Q2"])
        self.assertIsNone(w.columns.name)

    def test_int_dtype(self):
        self.assertTrue(pd.api.types.is_integer_dtype(S.sales_pivot(DF)["Q2"]))

    def test_sorted_columns(self):
        d = pd.DataFrame({"region": ["A", "A"], "quarter": ["Q4", "Q1"], "sales": [1, 2]})
        self.assertEqual(list(S.sales_pivot(d).columns), ["Q1", "Q4"])

    def test_long(self):
        long = S.to_long(S.sales_pivot(DF))
        self.assertEqual(list(long.columns), ["region", "quarter", "sales"])
        self.assertEqual(long.values.tolist(), [["N", "Q1", 7], ["N", "Q2", 3], ["S", "Q1", 7], ["S", "Q2", 0]])

    def test_total_preserved(self):
        self.assertEqual(int(S.to_long(S.sales_pivot(DF))["sales"].sum()), int(DF["sales"].sum()))
''',
"feedback": [
    ("test_values", "Use aggfunc='sum' so duplicate pairs are added, and fill_value=0."),
    ("test_axes", "Sort index/columns and remove the columns name with rename_axis(columns=None)."),
    ("test_long", "Melt with id_vars='region', var_name='quarter', value_name='sales', then sort."),
    ("test_int_dtype", "fill_value=0 keeps integer dtype; NaN would force floats."),
],
},
# ---------------------------------------------------------------- resample-weekly
{
"slug": "resample-weekly", "title": "Weekly Resampling",
"difficulty": "advanced", "prereqs": ["datetime-basics", "groupby-agg"], "packages": ["pandas", "numpy"],
"objectives": ["Parse dates and set a DatetimeIndex", "Resample to weekly frequency",
               "Understand week anchoring and empty periods"],
"tags": ["time-series", "resample", "datetime"],
"sources": ["S008"], "entry": "weekly_summary(df)",
"article": r'''
# Resampling Time Series

## Intuition
Daily data is noisy; weekly totals show the trend. Resampling is a group-by on time buckets.

## Precise explanation
* `pd.to_datetime(col)` parses dates; `df.set_index("date")` gives a `DatetimeIndex`.
* `s.resample("W").sum()` groups into weeks. `"W"` is an alias for `"W-SUN"`: each bucket ends on
  a Sunday and is **labelled by that Sunday**. Monday-anchored weeks would be `"W-MON"`.
* Periods with no observations still appear: `sum()` gives 0, `count()` gives 0, `mean()` gives NaN.
* Unsorted dates are fine for resample, but sort anyway for readability.

## Worked example
Dates Mon 2026-01-05 … Sun 2026-01-11 belong to the week labelled 2026-01-11; Mon 2026-01-12
starts the next week (labelled 2026-01-18).

## Common mistakes
* Strings instead of datetimes (resample raises a `TypeError`).
* Assuming weeks start Monday with `"W"`.
* Dropping empty weeks and creating gaps in a model's input.

## Why this matters
Forecasting, monitoring model metrics over time and building lag features all start from
correctly bucketed time series.
''',
"statement": r'''
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
''',
"starter": r'''
import pandas as pd


def weekly_summary(df):
    # TODO
    pass
''',
"hints": [
    "`s = df.assign(date=pd.to_datetime(df['date'])).set_index('date')['amount'].sort_index()`.",
    "`r = s.resample('W')`.",
    "`pd.DataFrame({'total': r.sum(), 'n': r.count(), 'mean': r.mean()})`.",
],
"solution": r'''
import pandas as pd


def weekly_summary(df):
    if len(df) == 0:
        raise ValueError("empty frame")
    s = (df.assign(date=pd.to_datetime(df["date"]))
           .set_index("date")["amount"].sort_index())
    r = s.resample("W")
    out = pd.DataFrame({"total": r.sum(), "n": r.count(), "mean": r.mean()})
    out.index.name = "date"
    return out
''',
"explanation": r'''
Parsing the dates and setting them as the index enables `resample`. Weekly buckets end on
Sunday; sum and count give 0 for empty weeks while mean gives NaN, which is the honest answer.
''',
"tests": r'''
import numpy as np
import pandas as pd

DF = pd.DataFrame({"date": ["2026-01-05", "2026-01-11", "2026-01-12", "2026-01-26"],
                   "amount": [10, 5, 7, 1]})

class TestResample(unittest.TestCase):
    def test_index(self):
        idx = S.weekly_summary(DF).index
        self.assertEqual([d.strftime("%Y-%m-%d") for d in idx],
                         ["2026-01-11", "2026-01-18", "2026-01-25", "2026-02-01"])
        self.assertEqual(idx.name, "date")

    def test_totals(self):
        self.assertEqual(S.weekly_summary(DF)["total"].tolist(), [15, 7, 0, 1])

    def test_counts(self):
        self.assertEqual(S.weekly_summary(DF)["n"].tolist(), [2, 1, 0, 1])

    def test_mean_nan_empty(self):
        m = S.weekly_summary(DF)["mean"]
        self.assertAlmostEqual(m.iloc[0], 7.5)
        self.assertTrue(np.isnan(m.iloc[2]))

    def test_unsorted_input(self):
        out = S.weekly_summary(DF.iloc[::-1].reset_index(drop=True))
        self.assertEqual(out["total"].tolist(), [15, 7, 0, 1])

    def test_sunday_belongs_to_its_week(self):
        out = S.weekly_summary(pd.DataFrame({"date": ["2026-01-11"], "amount": [3]}))
        self.assertEqual(out.index[0].strftime("%Y-%m-%d"), "2026-01-11")

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.weekly_summary(pd.DataFrame({"date": [], "amount": []}))
''',
"feedback": [
    ("test_index", "Use resample('W') (weeks end Sunday) and name the index 'date'."),
    ("test_counts", "Use count() so empty weeks show 0."),
    ("test_mean_nan_empty", "Mean of an empty week is NaN — don't fill it."),
    ("test_unsorted_input", "Convert to datetime and sort the index."),
],
},
# ---------------------------------------------------------------- binning-cut
{
"slug": "binning-cut", "title": "Binning with pd.cut",
"difficulty": "advanced", "prereqs": ["groupby-agg", "histogram-bins"], "packages": ["pandas", "numpy"],
"objectives": ["Discretise numbers into labelled bins", "Control interval closure (right=False)",
               "Count observations per ordered category including empty ones"],
"tags": ["binning", "categorical", "pd.cut", "discretisation"],
"sources": ["S008"], "entry": "age_groups(ages); group_counts(ages)",
"article": r'''
# Binning Numbers into Categories

## Intuition
Ages 0–120 are easier to report as "child / teen / adult / senior". Binning converts a
continuous variable into ordered categories.

## Precise explanation
```python
pd.cut(ages, bins=[0, 13, 20, 65, np.inf], labels=["child", "teen", "adult", "senior"], right=False)
```
* `bins` are edges; `right=False` makes intervals **left-closed** `[0, 13)`, `[13, 20)`, … so
  13 is a teen. The default `right=True` gives `(0, 13]`.
* Values outside all bins become NaN.
* The result is an **ordered Categorical**; `value_counts(sort=False)` lists categories in bin
  order and includes empty categories with count 0.
* `pd.qcut` makes equal-frequency bins from quantiles instead of fixed edges.

## Worked example
ages [5, 13, 19, 20, 70, -1] → [child, teen, teen, adult, senior, NaN].

## Common mistakes
* Off-by-one at bin edges from the wrong `right` setting.
* Forgetting `np.inf` as the last edge, so large values become NaN.
* Sorting counts by frequency when the category order is meaningful.

## Why this matters
Binned features help simple models capture non-linear effects and are used in calibration,
fairness reporting and histograms ([[histogram-bins]]).
''',
"statement": r'''
Implement with edges `[0, 13, 20, 65, inf)` and labels `child, teen, adult, senior`
(left-closed intervals):
* `age_groups(ages)` → categorical Series of labels (NaN for negative ages).
* `group_counts(ages)` → `dict` mapping every label (in bin order) to its count (ints, zeros
  included), ignoring NaN.

**Examples**
```python
age_groups([5, 13, 19, 20, 70, -1]).tolist()   # ['child', 'teen', 'teen', 'adult', 'senior', nan]
group_counts([5, 13, 19, 20, 70, -1])          # {'child': 1, 'teen': 2, 'adult': 1, 'senior': 1}
group_counts([30])                             # {'child': 0, 'teen': 0, 'adult': 1, 'senior': 0}
```
''',
"starter": r'''
import numpy as np
import pandas as pd

EDGES = [0, 13, 20, 65, np.inf]
LABELS = ["child", "teen", "adult", "senior"]


def age_groups(ages):
    # TODO
    pass


def group_counts(ages):
    # TODO
    return {}
''',
"hints": [
    "`pd.cut(pd.Series(ages), bins=EDGES, labels=LABELS, right=False)`.",
    "`value_counts(sort=False)` keeps category order and includes zeros.",
    "Convert to a dict with int values: `{k: int(v) for k, v in counts.items()}`.",
],
"solution": r'''
import numpy as np
import pandas as pd

EDGES = [0, 13, 20, 65, np.inf]
LABELS = ["child", "teen", "adult", "senior"]


def age_groups(ages):
    return pd.cut(pd.Series(ages, dtype=float), bins=EDGES, labels=LABELS, right=False)


def group_counts(ages):
    counts = age_groups(ages).value_counts(sort=False)
    return {str(k): int(counts.get(k, 0)) for k in LABELS}
''',
"explanation": r'''
`pd.cut` maps each age to its left-closed interval and attaches labels; negative ages fall
outside every bin and become NaN. Counting over the categorical keeps the bin order and reports
empty categories as 0.
''',
"tests": r'''
import numpy as np
import pandas as pd

class TestBinning(unittest.TestCase):
    def test_groups(self):
        out = S.age_groups([5, 13, 19, 20, 70, -1]).tolist()
        self.assertEqual(out[:5], ["child", "teen", "teen", "adult", "senior"])
        self.assertTrue(pd.isna(out[5]))

    def test_edges_left_closed(self):
        self.assertEqual(S.age_groups([0, 13, 20, 65]).tolist(), ["child", "teen", "adult", "senior"])

    def test_counts(self):
        self.assertEqual(S.group_counts([5, 13, 19, 20, 70, -1]),
                         {"child": 1, "teen": 2, "adult": 1, "senior": 1})

    def test_counts_zeros_and_order(self):
        c = S.group_counts([30])
        self.assertEqual(list(c), ["child", "teen", "adult", "senior"])
        self.assertEqual(c, {"child": 0, "teen": 0, "adult": 1, "senior": 0})

    def test_ordered_categorical(self):
        s = S.age_groups([1, 90])
        self.assertTrue(isinstance(s.dtype, pd.CategoricalDtype) and s.cat.ordered)

    def test_large(self):
        self.assertEqual(S.age_groups([1000]).tolist(), ["senior"])
''',
"feedback": [
    ("test_edges_left_closed", "Use right=False so 13 is a teen and 65 a senior."),
    ("test_large", "The last edge must be np.inf."),
    ("test_counts_zeros_and_order", "Use value_counts(sort=False) and include every label."),
    ("test_groups", "Negative ages fall outside the bins and become NaN."),
],
},
# ---------------------------------------------------------------- rolling-features
{
"slug": "rolling-features", "title": "Rolling-Window Features",
"difficulty": "advanced", "prereqs": ["resample-weekly", "moving-average"], "packages": ["pandas", "numpy"],
"objectives": ["Compute per-entity rolling statistics", "Avoid target leakage with shift",
               "Combine groupby, sort and transform"],
"tags": ["rolling", "lag-features", "leakage", "groupby-transform"],
"sources": ["S008"], "entry": "add_history_features(df, window=3)",
"article": r'''
# Leakage-free Rolling Features

## Intuition
To predict today's sales for a store, yesterday's and last week's sales are useful features —
but today's sales must not be inside its own feature. A rolling mean that includes the current
row "peeks at the answer" (**target leakage**) and makes offline accuracy look better than it
will be in production.

## Precise explanation
For each entity (store) separately, sorted by time:
* **lag-1**: `s.shift(1)` — previous value (NaN for the first row).
* **past rolling mean**: `s.shift(1).rolling(window, min_periods=1).mean()` — mean of up to
  `window` *previous* values.
* Group-wise: `df.groupby("store")["sales"].transform(lambda s: s.shift(1).rolling(w, min_periods=1).mean())`.
  `transform` returns a result aligned to the original rows.
Sort by `[store, date]` first, otherwise "previous" is meaningless.

## Worked example
store A sales by day: 10, 20, 30, 40; window 2 →
lag1: NaN, 10, 20, 30; past mean: NaN, 10, 15, 25.

## Common mistakes
* `rolling(...).mean()` without `shift(1)` → leakage.
* Rolling over the whole frame, mixing stores.
* Forgetting to sort by date within each store.

## Why this matters
Time-aware features and leakage awareness are central to forecasting, fraud detection and any
model trained on historical logs; the same thinking applies to fitting scalers only on the
training split ([[standard-scaler]]).
''',
"statement": r'''
Write `add_history_features(df, window=3)` for columns `store`, `date` (`YYYY-MM-DD`),
`sales`. Return a new DataFrame sorted by `store` then `date` (index 0..n−1, `date` converted to
datetime) with two new columns computed **within each store**:
* `lag1`: previous sales value (NaN for a store's first row),
* `past_mean`: mean of up to `window` previous sales values (NaN for the first row).
Raise `ValueError` if `window < 1`.

**Example**
```python
df = pd.DataFrame({"store": ["A", "B", "A", "A", "B", "A"],
                   "date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03", "2026-01-02", "2026-01-04"],
                   "sales": [10, 5, 20, 30, 7, 40]})
add_history_features(df, window=2)[["store", "sales", "lag1", "past_mean"]]
#   store  sales  lag1  past_mean
# 0     A     10   NaN        NaN
# 1     A     20  10.0       10.0
# 2     A     30  20.0       15.0
# 3     A     40  30.0       25.0
# 4     B      5   NaN        NaN
# 5     B      7   5.0        5.0
```
''',
"starter": r'''
import pandas as pd


def add_history_features(df, window=3):
    # TODO
    pass
''',
"hints": [
    "`out = df.assign(date=pd.to_datetime(df['date'])).sort_values(['store', 'date']).reset_index(drop=True)`.",
    "`g = out.groupby('store')['sales']`; `lag1 = g.shift(1)`.",
    "`g.transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())`.",
],
"solution": r'''
import pandas as pd


def add_history_features(df, window=3):
    if window < 1:
        raise ValueError("window must be >= 1")
    out = (df.assign(date=pd.to_datetime(df["date"]))
             .sort_values(["store", "date"], kind="mergesort")
             .reset_index(drop=True))
    g = out.groupby("store")["sales"]
    lag1 = g.shift(1)
    past_mean = g.transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    return out.assign(lag1=lag1, past_mean=past_mean)
''',
"explanation": r'''
Sorting by store and date defines "previous". Within each store, shifting by one excludes the
current row, so both the lag and the rolling mean only use past information. `transform` keeps
the results aligned with the sorted rows.
''',
"tests": r'''
import numpy as np
import pandas as pd

DF = pd.DataFrame({"store": ["A", "B", "A", "A", "B", "A"],
                   "date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03", "2026-01-02", "2026-01-04"],
                   "sales": [10, 5, 20, 30, 7, 40]})

def nan_list(s):
    return [None if pd.isna(v) else float(v) for v in s]

class TestRolling(unittest.TestCase):
    def test_order(self):
        out = S.add_history_features(DF, 2)
        self.assertEqual(out["store"].tolist(), ["A"] * 4 + ["B"] * 2)
        self.assertEqual(out["sales"].tolist(), [10, 20, 30, 40, 5, 7])

    def test_lag(self):
        self.assertEqual(nan_list(S.add_history_features(DF, 2)["lag1"]), [None, 10, 20, 30, None, 5])

    def test_past_mean(self):
        self.assertEqual(nan_list(S.add_history_features(DF, 2)["past_mean"]), [None, 10, 15, 25, None, 5])

    def test_window3(self):
        self.assertAlmostEqual(S.add_history_features(DF, 3)["past_mean"].iloc[3], 20.0)

    def test_no_leakage(self):
        out = S.add_history_features(DF, 1)
        self.assertTrue((out["past_mean"].dropna() != out["sales"][out["past_mean"].notna()]).all())

    def test_datetime(self):
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(S.add_history_features(DF)["date"]))

    def test_bad_window(self):
        with self.assertRaises(ValueError):
            S.add_history_features(DF, 0)
''',
"feedback": [
    ("test_past_mean", "Shift by one before rolling so the current sale is excluded."),
    ("test_lag", "Compute the lag within each store (groupby('store'))."),
    ("test_order", "Sort by store, then date, and reset the index."),
    ("test_no_leakage", "past_mean must never include the current row's value."),
],
},
]
