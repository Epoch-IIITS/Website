# Leakage-free Rolling Features

## Learning outcomes

After this lesson you can:

- Compute per-entity rolling statistics
- Avoid target leakage with shift
- Combine groupby, sort and transform

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
training split (ML-08).

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
