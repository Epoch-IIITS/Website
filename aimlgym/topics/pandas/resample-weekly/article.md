# Resampling Time Series

## Learning outcomes

After this lesson you can:

- Parse dates and set a DatetimeIndex
- Resample to weekly frequency
- Understand week anchoring and empty periods

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

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
