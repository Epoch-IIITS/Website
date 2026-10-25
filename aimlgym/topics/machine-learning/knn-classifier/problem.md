# ML-13 · k-Nearest Neighbors Classifier by Hand

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** ML-06 Confusion Matrix, Precision, Recall, F1, NP-11 Vectorized Pairwise Distances

Read the lesson first: [article.md](article.md)

## Task

Write `knn_predict(X_train, y_train, X_test, k=3)` returning a NumPy array of predicted labels
(integers) for each test row.

* Squared Euclidean distances; neighbours ordered with `np.argsort(d, kind="stable")`.
* Majority vote; vote ties go to the tied label that appears first in the neighbour order.
* Raise `ValueError` unless `1 <= k <= len(X_train)`, or if feature dimensions differ.

**Example**
```python
Xtr = np.array([[0, 0], [1, 0], [5, 5], [6, 5], [5, 6]]); ytr = np.array([0, 0, 1, 1, 1])
knn_predict(Xtr, ytr, np.array([[2, 1]]), k=3)   # array([0])
knn_predict(Xtr, ytr, np.array([[2, 1]]), k=5)   # array([1])
```

## Hints

<details><summary>Hint 1</summary>

Compute the (n_test, n_train) squared-distance matrix with broadcasting (NP-11).

</details>

<details><summary>Hint 2</summary>

For each row: `order = np.argsort(d_row, kind='stable')[:k]`; `labels = y_train[order]`.

</details>

<details><summary>Hint 3</summary>

Count votes in neighbour order; pick the label with the max count, scanning `labels` left to right for ties.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_k5_majority` | Vote among the k nearest *training points*, not class means. |
| `test_vote_tie_nearest_wins` | On a vote tie pick the tied label that appears first in neighbour (distance) order. |
| `test_distance_tie_index` | Use np.argsort(..., kind='stable') so equal distances keep training order. |
| `test_not_nearest_centroid` | Nearest centroid would predict differently here — vote among neighbours. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All test–train distances are computed at once. For each test point a stable argsort orders
neighbours (ties by training index); the vote counts labels among the first k, and the first
label in neighbour order reaching the maximum count wins, which implements the nearest-member
tie-break.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [NumPy: the absolute basics for beginners (NumPy v2.5 Manual)](https://numpy.org/doc/stable/user/absolute_beginners.html) — NumPy Developers (`S007`)
