# XA-08 · Permutation Feature Importance by Hand

**Topic:** Explainable AI · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** XA-06 Partial Dependence by Hand, ML-02 The scikit-learn Estimator API

Read the lesson first: [article.md](article.md)

## Task

Write `permutation_importance(predict, X, y, score, n_repeats=5, seed=0)` returning a dict
`{"baseline": float, "mean": array(d), "std": array(d)}` following the recipe above (`score(y_true,
y_pred)` returns a float; `X` must not be modified). Raise `ValueError` if `n_repeats < 1`.

**Example**
```python
r = permutation_importance(lambda X: 3 * X[:, 0], X, y, r2_score, n_repeats=5, seed=0)
r["mean"][0] > 1.0 and abs(r["mean"][1]) < 1e-12    # True (model ignores feature 1)
```

## Hints

<details><summary>Hint 1</summary>

`base = score(y, predict(X))`; `rng = np.random.default_rng(seed)`.

</details>

<details><summary>Hint 2</summary>

For each j, r: `Xp = X.copy(); Xp[:, j] = X[rng.permutation(n), j]`.

</details>

<details><summary>Hint 3</summary>

Collect drops `base - score(y, predict(Xp))`; take mean and std per feature.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe` | One default_rng(seed); loop features outer, repeats inner; permute rows of column j only. |
| `test_relevant_vs_irrelevant` | Importance = baseline score − permuted score (don't refit). |
| `test_no_mutation` | Permute a copy of X, not X itself. |
| `test_std_shape` | Return mean and std arrays with one entry per feature. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The baseline score is computed once. Each feature is permuted on a fresh copy of X, which breaks
its link with y while keeping its marginal distribution; the average drop in score across repeats is
the importance and the spread shows its uncertainty.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
