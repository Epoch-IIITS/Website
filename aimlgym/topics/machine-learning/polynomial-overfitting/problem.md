# ML-15 · Polynomial Features and Overfitting by Hand

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** ML-09 Least-Squares Line, ML-05 Seeded Train/Test Split

Read the lesson first: [article.md](article.md)

## Task

Implement (`x` and `y` are 1-D arrays or lists):

1. `poly_features(x, degree)` → array of shape `(len(x), degree + 1)` with columns
   $x^0, x^1, \dots, x^{degree}$.
2. `fit_poly(x, y, degree)` → coefficient array (lowest power first) from
   `np.linalg.lstsq(poly_features(x, degree), y, rcond=None)`.
3. `predict_poly(coef, x)` → predictions $\sum_k c_k x^k$.
4. `errors_by_degree(x_tr, y_tr, x_te, y_te, degrees)` → dict degree → `(train_mse, test_mse)`
   as floats.
5. `best_degree(errors)` → the degree with the smallest **test** MSE (ties: the smaller degree).

## Hints

<details><summary>Hint 1</summary>

`np.column_stack([x ** k for k in range(degree + 1)])` builds the feature matrix.

</details>

<details><summary>Hint 2</summary>

`coef, *_ = np.linalg.lstsq(X, y, rcond=None)`; predictions are `poly_features(x, len(coef) - 1) @ coef`.

</details>

<details><summary>Hint 3</summary>

`min(errors, key=lambda d: (errors[d][1], d))` picks the lowest test error, then the smaller degree.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_features` | Columns must be x**0, x**1, ..., x**degree in that order. |
| `test_exact_recovery` | Fit with `np.linalg.lstsq(X, y, rcond=None)` on the polynomial features. |
| `test_training_error_non_increasing` | Compute the training error on the training points with the coefficients fitted on them. |
| `test_overfitting_visible` | Evaluate each model on the test points too; don't refit on them. |
| `test_best_degree` | Choose by test error (the second value), breaking ties with the smaller degree. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Polynomial regression is linear regression on engineered features, so the same least-squares
solver fits every degree. Evaluating each fitted model on both the training and the held-out
points exposes the familiar pattern, and selection uses only the held-out error with a
deterministic tie-break.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Underfitting vs. Overfitting (scikit-learn example)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html) — scikit-learn developers (`S090`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
