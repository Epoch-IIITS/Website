# ML-23 · Gradient Boosting

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-22 Decision Trees and Random Forests

Read the lesson first: [article.md](article.md)

## Task

Write `boosting_curve(X_train, y_train, X_val, y_val, max_iter=100, learning_rate=0.1, seed=0)`
for binary labels, returning
`{"train_loss": list[float], "val_loss": list[float], "best_iteration": int, "val_accuracy": float}`.

* Fit `HistGradientBoostingClassifier(max_iter=max_iter, learning_rate=learning_rate,
  early_stopping=False, random_state=seed)` on the training data.
* `train_loss[i]` and `val_loss[i]` are `log_loss` after `i + 1` trees, computed from
  `staged_predict_proba` (pass `labels=[0, 1]`).
* `best_iteration` is the 1-based iteration with the lowest validation loss (earliest on ties);
  `val_accuracy` is the final model's accuracy on the validation set.
* Raise `ValueError` if `max_iter < 1` or `learning_rate <= 0`.

## Hints

<details><summary>Hint 1</summary>

Validate the arguments, then fit the classifier with `early_stopping=False`.

</details>

<details><summary>Hint 2</summary>

`[float(log_loss(y_val, p, labels=[0, 1])) for p in model.staged_predict_proba(X_val)]`.

</details>

<details><summary>Hint 3</summary>

`best_iteration = val_loss.index(min(val_loss)) + 1`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_curve_lengths` | Use staged_predict_proba to get one probability set per tree. |
| `test_validation_overfits_late` | best_iteration is the 1-based position of the smallest validation loss. |
| `test_final_accuracy` | Fit with early_stopping=False and random_state=seed; score the validation set. |
| `test_invalid` | Reject max_iter < 1 and learning_rate <= 0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`staged_predict_proba` replays the ensemble one tree at a time, so a single fit yields the whole
loss curve. Training loss keeps falling as trees are added, while validation loss bottoms out;
its minimum marks how many trees to keep.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
