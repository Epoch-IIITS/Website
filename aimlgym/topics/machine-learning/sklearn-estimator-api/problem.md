# ML-02 · The scikit-learn Estimator API

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-01 Features, Labels and Baseline Models

Read the lesson first: [article.md](article.md)

## Task

Write `evaluate_regressor(model, X_train, y_train, X_test, y_test)` that fits a **clone** of
`model` on the training data and returns
`{"model": fitted_clone, "predictions": list[float], "mse": float, "mae": float, "r2": float}`
computed on the test data with `sklearn.metrics`.

* The `model` passed in must stay unfitted (use `sklearn.base.clone`).
* Raise `ValueError` if `X_train` and `y_train` (or `X_test` and `y_test`) have different numbers
  of rows.

**Example**
```python
from sklearn.linear_model import LinearRegression
r = evaluate_regressor(LinearRegression(), [[1], [2], [3], [4]], [3, 5, 7, 9], [[5], [6]], [11, 14])
r["predictions"], r["mse"], r["mae"]     # ([11.0, 13.0], 0.5, 0.5)
```

## Hints

<details><summary>Hint 1</summary>

Check `len(X_train) == len(y_train)` and the same for the test arrays.

</details>

<details><summary>Hint 2</summary>

`fitted = clone(model).fit(X_train, y_train)`; `pred = fitted.predict(X_test)`.

</details>

<details><summary>Hint 3</summary>

Metrics take `(y_true, y_pred)`; convert predictions with `[float(v) for v in pred]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_linear_example` | Fit on the training data, predict the test rows, and pass (y_true, y_pred) to the metrics. |
| `test_original_model_not_fitted` | Fit `clone(model)`, not `model` itself. |
| `test_metrics_match_formulas` | Use mean_squared_error, mean_absolute_error and r2_score on the test set. |
| `test_plain_floats_and_validation` | Convert results to float and check that X and y lengths match. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`clone` copies the settings but not the learned state, so fitting it leaves the caller's model
untouched. Any regressor works because the function relies only on `fit` and `predict`, and the
three metrics come from `sklearn.metrics` with the true values first.

## References

- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
