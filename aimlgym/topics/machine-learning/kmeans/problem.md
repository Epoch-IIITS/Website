# ML-26 · k-Means Clustering by Hand

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** ML-13 k-Nearest Neighbors Classifier by Hand

Read the lesson first: [article.md](article.md)

## Task

Write `kmeans(X, init_centroids, max_iter=100, tol=1e-9)` returning a dict
`{"centroids": (k, d) array, "labels": (n,) int array, "inertia": float, "n_iter": int}`.

* Each iteration: assign (argmin squared distance, lowest index on ties), then update means
  (empty clusters keep their previous centroid). `n_iter` counts completed iterations.
* Stop after an iteration whose maximum squared centroid shift is `<= tol`.
* Final `labels` and `inertia` correspond to the returned centroids.
* Raise `ValueError` on dimension mismatch or `k > n`.

**Example**
```python
r = kmeans(np.array([[0.], [1.], [10.], [11.]]), np.array([[0.], [1.]]))
r["centroids"].ravel()   # [ 0.5, 10.5]
r["labels"]              # [0, 0, 1, 1]
r["inertia"]             # 1.0
```

## Hints

<details><summary>Hint 1</summary>

Distances: `((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)`; labels = `argmin(axis=1)`.

</details>

<details><summary>Hint 2</summary>

New centroid j = `X[labels == j].mean(axis=0)` if any points, else old `C[j]`.

</details>

<details><summary>Hint 3</summary>

After the loop, recompute labels and inertia for the final centroids.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_1d` | Assign with the current centroids, then move each centroid to its members' mean. |
| `test_empty_cluster_kept` | If no points are assigned, keep the old centroid. |
| `test_inertia_matches` | Recompute labels and inertia after the final update. |
| `test_n_iter` | Count iterations and stop when the max squared shift <= tol. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each iteration performs one assignment step and one update step. Empty clusters keep their
previous centre, avoiding NaN. Convergence is detected by the largest squared centroid movement.
A final assignment makes labels and inertia consistent with the returned centroids.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
