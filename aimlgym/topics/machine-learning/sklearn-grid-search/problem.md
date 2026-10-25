# ML-19 · Regularisation and Hyperparameter Search

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-18 Pipelines and ColumnTransformer

Read the lesson first: [article.md](article.md)

## Task

Write `tune_ridge(X, y, alphas, n_splits=5, seed=0)` returning
`{"best_alpha": float, "best_mse": float, "mse_by_alpha": list[float], "coef_norms": list[float], "model": fitted_best}`.

* Search `make_pipeline(StandardScaler(), Ridge())` with `GridSearchCV` over `{"ridge__alpha": alphas}`,
  `cv=KFold(n_splits, shuffle=True, random_state=seed)`, `scoring="neg_mean_squared_error"`.
* `best_mse` and `mse_by_alpha` are positive mean validation MSEs (grid order).
* `coef_norms[i]` is the Euclidean norm of the Ridge coefficients when the pipeline with `alphas[i]`
  is fitted on all of `X, y`.
* `model` is `search.best_estimator_`.
* Raise `ValueError` if `alphas` is empty or contains a value ≤ 0.

## Hints

<details><summary>Hint 1</summary>

Build the pipeline, then `GridSearchCV(pipe, {"ridge__alpha": list(alphas)}, cv=..., scoring=...)` and fit it.

</details>

<details><summary>Hint 2</summary>

`-search.cv_results_["mean_test_score"]` gives the MSE for every alpha in grid order.

</details>

<details><summary>Hint 3</summary>

For the norms, fit `make_pipeline(StandardScaler(), Ridge(alpha=a))` on all data and take `np.linalg.norm(p[-1].coef_)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_norms_shrink` | Fit a scaled Ridge(alpha=a) on all data for each alpha and take the coefficient norm. |
| `test_mse_matches_cross_val_score` | Use KFold(n_splits, shuffle=True, random_state=seed) and negate the scores. |
| `test_best_model_refit_on_all_data` | Return search.best_estimator_, which GridSearchCV refits on all data. |
| `test_invalid` | Alphas must be a non-empty list of positive numbers. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`GridSearchCV` cross-validates the scaled Ridge pipeline for each alpha and refits the winner on
all the data. Negating the scores turns them into MSEs. Refitting each alpha on the full data shows
the shrinkage directly: the coefficient norm can only fall as the penalty grows.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
