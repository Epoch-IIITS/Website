# ML-01 · Features, Labels and Baseline Models

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** NP-05 Aggregations Along Axes

Read the lesson first: [article.md](article.md)

## Task

Implement with NumPy:

* `class MeanRegressor` — `fit(X, y)` stores `self.mean_ = float(mean of y)` and returns `self`;
  `predict(X)` returns a float array with one copy of the mean per row of `X`. Calling
  `predict` before `fit` raises `ValueError`.
* `class MajorityClassifier` — `fit` stores `self.label_`, the most frequent label (ties: the
  smallest label); `predict` returns an array of that label, one per row; `ValueError` before
  `fit`.
* `mse(y_true, y_pred)` and `accuracy(y_true, y_pred)` as floats; raise `ValueError` if the
  lengths differ or are 0.

`X` may be a list of lists or a 2-D array; only its number of rows matters to these baselines.

## Hints

<details><summary>Hint 1</summary>

Before fitting, the attribute does not exist: check `hasattr(self, "mean_")` in `predict`.

</details>

<details><summary>Hint 2</summary>

`labels, counts = np.unique(y, return_counts=True)`; `np.unique` sorts labels, so `labels[np.argmax(counts)]` picks the smallest on ties.

</details>

<details><summary>Hint 3</summary>

`np.full(len(X), self.mean_)` repeats a value; MSE is `np.mean((y_true - y_pred) ** 2)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_mean_regressor` | Store the training mean in `self.mean_` and repeat it once per row of X. |
| `test_fit_returns_self` | End `fit` with `return self`. |
| `test_predict_before_fit` | Raise ValueError in `predict` if the model has not been fitted. |
| `test_majority_tie_smallest` | Use `np.unique(..., return_counts=True)` and `np.argmax`, which picks the first (smallest) label on ties. |
| `test_metrics` | Check that lengths match and are non-zero before computing. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each baseline learns a single value in `fit` and repeats it in `predict`, using the row count of
`X` so the output has one prediction per example. `np.unique` returns sorted labels, so taking
the first maximum count resolves ties toward the smallest label. Missing attributes signal an
unfitted model.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
