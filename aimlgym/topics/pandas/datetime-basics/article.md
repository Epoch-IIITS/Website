# Working with Dates

## Learning outcomes

After this lesson you can:

- Parse ISO date strings with pd.to_datetime and an explicit format
- Extract parts with the .dt accessor
- Subtract dates to get durations in days
- Compare pandas date arithmetic with the datetime module

## Intuition
`"2026-03-09"` is just text until you convert it to a date. Once converted, you can ask which
weekday it was, how many days separate two dates, or keep only March — and you can sort and
resample by time (PD-13).

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

## References

- [Time series / date functionality (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/timeseries.html) — pandas development team (`S087`)
- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
