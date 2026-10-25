# Measuring Regression Error

## Learning outcomes

After this lesson you can:

- Compute MSE, RMSE, MAE and R²
- Interpret R² relative to a mean baseline
- Handle degenerate targets

## Intuition
How wrong are the predictions? Average the errors — but squared errors punish big misses more
than absolute errors. R² compares the model with the simplest possible model: always predicting
the mean.

## Precise explanation
With residuals $e_i = y_i - \hat y_i$:
* $\text{MSE} = \frac1n\sum e_i^2$, $\text{RMSE} = \sqrt{\text{MSE}}$ (same units as y).
* $\text{MAE} = \frac1n\sum |e_i|$ — less sensitive to outliers.
* $R^2 = 1 - \frac{\sum e_i^2}{\sum (y_i - \bar y)^2}$. $R^2 = 1$ is perfect, 0 equals the mean
  baseline, negative is *worse* than the baseline. Undefined when all $y_i$ are equal.

## Worked example
y = [3, 5, 7], ŷ = [2, 5, 9]: e = [1, 0, −2]; MSE 5/3 ≈ 1.667, RMSE 1.291, MAE 1;
Σ(y−ȳ)² = 8, R² = 1 − 5/8 = 0.375.

## Common mistakes
* Averaging signed errors (positive and negative cancel).
* Swapping arguments in R² (it is not symmetric).
* Reporting R² on training data only.

## Why this matters
These metrics evaluate ML-09/07/12 and are the losses many models minimise.

## Library implementation

`sklearn.metrics` provides `mean_squared_error`, `root_mean_squared_error`,
`mean_absolute_error` and `r2_score` with the same definitions. Comparison runs when scikit-learn
is installed.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
