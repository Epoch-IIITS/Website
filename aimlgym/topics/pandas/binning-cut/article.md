# Binning Numbers into Categories

## Learning outcomes

After this lesson you can:

- Discretise numbers into labelled bins
- Control interval closure (right=False)
- Count observations per ordered category including empty ones

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
fairness reporting and histograms (ST-04).

## References

- [10 minutes to pandas (pandas 3.1.0 docs)](https://pandas.pydata.org/docs/user_guide/10min.html) — pandas via NumFOCUS (`S008`)
