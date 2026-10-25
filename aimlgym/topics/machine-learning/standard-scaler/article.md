# Fit/Transform and Data Leakage

## Learning outcomes

After this lesson you can:

- Write a fit/transform class
- Avoid data leakage by fitting only on training data
- Invert the transformation

## Intuition
Standardising needs a mean and a standard deviation. If you compute them on *all* data, the
test set has quietly influenced training — information has **leaked**. Learn the statistics on
the training set, then apply those same numbers to the test set.

## Precise explanation
The **estimator** pattern (used by scikit-learn):
* `fit(X)` learns parameters (here `mean_`, `scale_` per column) and returns `self`.
* `transform(X)` applies them: $(X - \mu)/\sigma$.
* `fit_transform(X)` = fit then transform.
* `inverse_transform(Z)` = $Z\sigma + \mu$.
* Calling `transform` before `fit` should raise an error.
Constant columns have $\sigma = 0$; use scale 1 so they map to 0 instead of NaN.

## Worked example
Train X = [[1], [3]] → mean 2, std 1. Test x = 5 → z = 3 (not 0!) — the test point is far from
the training data, and the scaler correctly reports it.

## Common mistakes
* `fit` on the test set (or refitting on each batch at prediction time).
* Returning a new array from `fit` instead of `self`.
* Using the sample std in one place and population std elsewhere.

## Why this matters
Leakage is one of the most common reasons ML results fail to reproduce; this pattern also
structures ML-13…ML-20 models.

## Library implementation

`sklearn.preprocessing.StandardScaler` has the same interface (`fit`, `transform`,
`fit_transform`, `inverse_transform`), uses the population standard deviation and leaves
constant columns unscaled (scale 1), exactly like your class.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
