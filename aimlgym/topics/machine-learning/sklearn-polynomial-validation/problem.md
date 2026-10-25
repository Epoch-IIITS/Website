# ML-14 · Polynomial Features and Validation Curves

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-12 k-Nearest Neighbours with scikit-learn, ML-10 Linear Regression by Gradient Descent

Read the lesson first: [article.md](article.md)

## Task

Write `degree_curve(x, y, degrees, n_splits=5, seed=0)` for one input feature `x` (a 1-D
sequence) returning `{"train_mse": list[float], "val_mse": list[float], "best_degree": int}`.

* Model: `make_pipeline(PolynomialFeatures(include_bias=False), LinearRegression())`.
* Use `validation_curve` with `param_name="polynomialfeatures__degree"`,
  `cv=KFold(n_splits, shuffle=True, random_state=seed)` and `scoring="neg_mean_squared_error"`.
* Each list holds the mean MSE over folds for each degree, in the order of `degrees`.
* `best_degree` has the smallest validation MSE (ties: the smaller degree).
* Raise `ValueError` if `degrees` is empty or `x` and `y` differ in length.

## Hints

<details><summary>Hint 1</summary>

Reshape the feature to a column: `X = np.asarray(x, dtype=float).reshape(-1, 1)`.

</details>

<details><summary>Hint 2</summary>

`train, val = validation_curve(model, X, y, param_name=..., param_range=degrees, cv=..., scoring=...)`.

</details>

<details><summary>Hint 3</summary>

MSE per degree is `-scores.mean(axis=1)`; pick the degree with the smallest validation MSE.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_quadratic_best_degree` | Pick the degree with the smallest mean validation MSE. |
| `test_underfit_line` | Negate the neg_mean_squared_error scores to get MSE. |
| `test_degree_one_matches_manual_cv` | Use KFold(n_splits, shuffle=True, random_state=seed) and include_bias=False. |
| `test_types_and_lengths` | Return plain floats in the order of degrees. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`validation_curve` refits the pipeline for every degree and fold; averaging across folds and
negating the scores gives mean squared errors. The minimum of the validation curve is the degree
that generalises best on this data.

## References

- [Underfitting vs. Overfitting (scikit-learn example)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html) — scikit-learn developers (`S090`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
