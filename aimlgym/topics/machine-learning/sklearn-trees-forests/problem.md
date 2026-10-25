# ML-22 · Decision Trees and Random Forests

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-21 Decision Stump with Gini Impurity, ML-19 Regularisation and Hyperparameter Search

Read the lesson first: [article.md](article.md)

## Task

Write `compare_tree_forest(X_train, y_train, X_test, y_test, max_depth=None, n_estimators=100, seed=0)`
returning
`{"tree_train_accuracy", "tree_test_accuracy", "forest_test_accuracy", "tree_depth", "top_feature", "importances"}`.

* Tree: `DecisionTreeClassifier(max_depth=max_depth, random_state=seed)`.
* Forest: `RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=seed)`.
* Accuracies are floats; `tree_depth` is `tree.get_depth()`; `importances` is the forest's
  `feature_importances_` as a list of floats; `top_feature` is the index of the largest one.
* Raise `ValueError` if `n_estimators < 1`.

## Hints

<details><summary>Hint 1</summary>

Fit both models with the same `random_state=seed`.

</details>

<details><summary>Hint 2</summary>

`model.score(X, y)` is accuracy for classifiers.

</details>

<details><summary>Hint 3</summary>

`importances = [float(v) for v in forest.feature_importances_]`; `top_feature = importances.index(max(importances))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_unlimited_tree_memorises` | With max_depth=None the tree grows until its leaves are pure. |
| `test_depth_limit` | Pass max_depth to both models. |
| `test_importances` | Use the forest's feature_importances_ as floats and the index of the largest. |
| `test_reproducible` | Use random_state=seed for both models. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Both models are fitted with the same seed and depth limit, so the comparison isolates the effect
of averaging. `score` gives accuracy, `get_depth` shows how far the single tree grew, and the
forest's normalised impurity importances identify the feature it relied on most.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
