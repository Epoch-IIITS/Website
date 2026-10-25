# Pandas

**You will be able to:** Load, inspect, clean, filter, group, merge, reshape and window tabular data, comparing each operation with its plain-Python equivalent.

**Topic prerequisites:** NumPy

pandas adds labelled rows and columns on top of NumPy. You start with a single labelled column
(`Series`), then build and read tables, select and derive columns, handle missing values, sort,
group, merge, clean text, work with dates, resample, pivot, bin and compute rolling features.
Group-by and merge lessons first solve the task with dictionaries so the library's behaviour is
not magic.

**Packages:** `pandas` and `numpy`. Packs are validated on pandas 2.2 (the executor image) and
pandas 3.x; code avoids chained assignment so it behaves the same under Copy-on-Write.

**Project ideas:** ungraded briefs between steps suggest things to build with what you have learned so far.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | PD-01 | [Series: Labelled Columns](series-basics/problem.md) | beginner | NP-04 |
| 2 | PD-02 | [Build and Describe a DataFrame](dataframe-basics/problem.md) | beginner | PD-01 |
| 3 | PD-03 | [Reading and Writing CSV](read-csv-io/problem.md) | beginner | PD-02, PY-23 |
| 4 | PD-04 | [Select and Filter Rows](select-filter/problem.md) | beginner | PD-03 |
| 5 | PD-05 | [Derived Columns](derived-columns/problem.md) | beginner | PD-04 |
| 6 | PD-06 | [Finding and Handling Missing Values](missing-values/problem.md) | beginner | PD-05 |
| 7 | PD-07 | [Sort and Rank](sort-rank/problem.md) | intermediate | PD-06 |
| 8 | PD-08 | [Group-by Aggregation](groupby-agg/problem.md) | intermediate | PD-07, PY-18 |
| 9 | PD-09 | [Fill Missing Values by Group](fill-missing-group/problem.md) | intermediate | PD-08 |
| 10 | PD-10 | [Merging Tables](merge-tables/problem.md) | intermediate | PD-08 |
| 11 | PD-P1 | [Project idea: Exploratory Analysis of a Public Dataset](public-dataset-eda/project.md) | ungraded | PD-03, PD-04, PD-06, PD-08, PD-10 |
| 12 | PD-11 | [Cleaning Text Columns](string-cleaning/problem.md) | intermediate | PD-06 |
| 13 | PD-12 | [Working with Dates](datetime-basics/problem.md) | intermediate | PD-11 |
| 14 | PD-13 | [Weekly Resampling](resample-weekly/problem.md) | advanced | PD-12, PD-08 |
| 15 | PD-14 | [Pivot Tables](pivot-table/problem.md) | advanced | PD-08 |
| 16 | PD-15 | [Binning with pd.cut](binning-cut/problem.md) | advanced | PD-08, ST-04 |
| 17 | PD-16 | [Rolling-Window Features](rolling-features/problem.md) | advanced | PD-13, NP-14 |
| 18 | PD-P2 | [Project idea: Personal Finance Dashboard Data](personal-finance-data/project.md) | ungraded | PD-11, PD-12, PD-13, PD-14, PD-15, PD-16 |
