# ML-03 · Regression Metrics

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** ML-01 Features, Labels and Baseline Models

Read the lesson first: [article.md](article.md)

## Task

Write `regression_report(y_true, y_pred)` returning a dict of floats
`{"mse", "rmse", "mae", "r2"}`. Raise `ValueError` for empty or mismatched inputs, and for
constant `y_true` (R² undefined).

**Example**
```python
regression_report([3, 5, 7], [2, 5, 9])
# {'mse': 1.6667, 'rmse': 1.2910, 'mae': 1.0, 'r2': 0.375}  (rounded here)
```

## Hints

<details><summary>Hint 1</summary>

`e = y_true - y_pred` with float arrays.

</details>

<details><summary>Hint 2</summary>

`mse = np.mean(e ** 2)`, `mae = np.mean(np.abs(e))`.

</details>

<details><summary>Hint 3</summary>

`ss_tot = np.sum((y_true - y_true.mean()) ** 2)`; raise if it is 0.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Use the mean of squared and absolute residuals; R² = 1 − SS_res/SS_tot. |
| `test_negative_r2` | Don't clip R² at 0 — worse-than-mean models have negative R². |
| `test_constant_target` | Raise ValueError when y_true has zero variance. |
| `test_types` | Return plain Python floats. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All four metrics come from the residual vector. R² divides the residual sum of squares by the
total sum of squares around the mean, so it measures improvement over the constant-mean model.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
