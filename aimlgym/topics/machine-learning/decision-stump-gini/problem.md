# ML-21 · Decision Stump with Gini Impurity

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** ML-06 Confusion Matrix, Precision, Recall, F1

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `gini(y)` → Gini impurity of a 1-D integer label array (0.0 for empty).
* `best_split(X, y)` → dict `{"feature": int, "threshold": float, "impurity": float,
  "left_class": int, "right_class": int}` using the rules above. If no feature has two distinct
  values, raise `ValueError`.

**Examples**
```python
gini(np.array([0, 0, 1, 1]))     # 0.5
best_split(np.array([[1], [2], [3], [4]]), np.array([0, 0, 1, 1]))
# {'feature': 0, 'threshold': 2.5, 'impurity': 0.0, 'left_class': 0, 'right_class': 1}
```

## Hints

<details><summary>Hint 1</summary>

`_, counts = np.unique(y, return_counts=True); p = counts / len(y); 1 - (p**2).sum()`.

</details>

<details><summary>Hint 2</summary>

Thresholds: `u = np.unique(X[:, j]); (u[:-1] + u[1:]) / 2`.

</details>

<details><summary>Hint 3</summary>

Use strict `<` when comparing impurities so the first (lowest feature/threshold) best is kept.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_weighted_impurity` | Weight each child's Gini by its share of samples. |
| `test_duplicates_midpoints` | Thresholds are midpoints between consecutive *unique* values. |
| `test_tie_lowest_feature` | Only replace the best split when strictly better. |
| `test_gini` | Gini = 1 − Σ p_c²; return 0 for empty input. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Gini comes from class proportions. The search scans features in order and thresholds in
increasing order, keeping a candidate only if it is strictly better, which implements the
tie-breaking rule. `np.unique` with `argmax` picks the smallest label among majority ties.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
