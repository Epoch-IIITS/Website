# Derived Columns

## Learning outcomes

After this lesson you can:

- Create columns from vectorised arithmetic
- Handle division by zero as NaN
- Return a new DataFrame with assign

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

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
