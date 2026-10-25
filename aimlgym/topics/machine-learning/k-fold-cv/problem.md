# ML-17 · k-Fold Cross-Validation by Hand

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** ML-15 Polynomial Features and Overfitting by Hand

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `kfold_indices(n, k, seed=None)` → list of `k` `(train_idx, test_idx)` pairs. If `seed` is not
  None, shuffle with `np.random.default_rng(seed).permutation(n)`; otherwise use `0..n-1`. Split
  with `np.array_split(order, k)`. Raise `ValueError` unless `2 <= k <= n`.
* `cross_val_score(fit, score, X, y, k=5, seed=0)` → NumPy array of k scores, where
  `model = fit(X_train, y_train)` and `score(model, X_test, y_test)` returns a float.

**Example**
```python
[t.tolist() for _, t in kfold_indices(7, 3)]   # [[0, 1, 2], [3, 4], [5, 6]]
```

## Hints

<details><summary>Hint 1</summary>

`order = np.arange(n)` or the seeded permutation; `folds = np.array_split(order, k)`.

</details>

<details><summary>Hint 2</summary>

Train indices for fold i: `np.concatenate([f for j, f in enumerate(folds) if j != i])`.

</details>

<details><summary>Hint 3</summary>

Loop over folds calling fit and score, collecting scores into an array.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_sizes` | Use np.array_split so the first n % k folds are one larger. |
| `test_partition` | Each index must appear in exactly one test fold; train = all other folds. |
| `test_seeded_recipe` | Shuffle with default_rng(seed).permutation(n) only when seed is not None. |
| `test_cv_values` | Call fit on the training fold and score on the test fold. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`array_split` produces k nearly equal folds; each fold serves once as the test set while the
others are concatenated for training. `cross_val_score` is model-agnostic: it only needs a fit
function and a score function, so any model in this topic can be evaluated.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
