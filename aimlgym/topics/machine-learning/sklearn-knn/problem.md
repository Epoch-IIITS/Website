# ML-12 · k-Nearest Neighbours with scikit-learn

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-07 Scaling inside a Pipeline, ML-11 Logistic Regression from Scratch

Read the lesson first: [article.md](article.md)

## Task

Write `knn_accuracy_by_k(X_train, y_train, X_test, y_test, ks)` returning
`{"accuracy": {k: float, ...}, "best_k": int}`.

* For each k, fit `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))` on the
  training data and record test accuracy with `accuracy_score`.
* `best_k` is the k with the highest accuracy; ties go to the **smallest** k.
* Raise `ValueError` if `ks` is empty or any k is less than 1 or larger than the number of
  training rows.

## Hints

<details><summary>Hint 1</summary>

Validate `ks` against `len(X_train)` first.

</details>

<details><summary>Hint 2</summary>

Inside the loop build a new pipeline for each k, fit it and call `accuracy_score(y_test, pipe.predict(X_test))`.

</details>

<details><summary>Hint 3</summary>

`best_k = min(ks, key=lambda k: (-accuracy[k], k))` picks the highest accuracy, then the smallest k.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_matches_manual_scaled_knn` | Scale inside the pipeline: make_pipeline(StandardScaler(), KNeighborsClassifier(k)). |
| `test_tie_prefers_smaller_k` | On equal accuracy choose the smallest k. |
| `test_float_accuracies` | Store float(accuracy_score(...)) for every k. |
| `test_invalid_k` | Reject an empty list and any k outside 1..len(X_train). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each k gets its own freshly fitted pipeline, so scaling statistics always come from the training
rows. The best k is chosen by sorting on negative accuracy and then on k, which resolves ties
towards the simpler, smaller neighbourhood.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
