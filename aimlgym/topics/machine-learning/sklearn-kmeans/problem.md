# ML-25 · k-Means and Silhouette Scores

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-24 Thresholds, ROC and Precision–Recall Curves

Read the lesson first: [article.md](article.md)

## Task

Write `choose_k(X, ks, seed=0)` returning
`{"inertia": list[float], "silhouette": list[float], "best_k": int, "labels": list[int]}`.

* For each k in `ks`, fit `KMeans(n_clusters=k, n_init=10, random_state=seed)` and record
  `inertia_` and `silhouette_score(X, labels_)`.
* `best_k` has the highest silhouette (ties: smaller k); `labels` are that model's labels.
* Raise `ValueError` if `ks` is empty or any k is less than 2 or at least the number of rows.

## Hints

<details><summary>Hint 1</summary>

Validate `ks` against `len(X)`: silhouette needs 2 ≤ k < n.

</details>

<details><summary>Hint 2</summary>

Keep each fitted model so you can return the best one's `labels_`.

</details>

<details><summary>Hint 3</summary>

`best = max(range(len(ks)), key=lambda i: (silhouette[i], -ks[i]))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_three_blobs` | Pick the k with the highest silhouette score. |
| `test_matches_kmeans` | Use KMeans(n_clusters=k, n_init=10, random_state=seed). |
| `test_types` | Return floats for scores and ints for labels. |
| `test_invalid` | Every k must satisfy 2 <= k < len(X). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each k gets ten seeded restarts and keeps the best; inertia measures tightness and the silhouette
balances tightness against separation. Selecting the highest silhouette (smaller k on ties) gives a
reproducible choice, and the labels come from that same fitted model.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
