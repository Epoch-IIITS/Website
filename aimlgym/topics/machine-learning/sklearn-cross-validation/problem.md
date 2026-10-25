# ML-16 · Cross-Validation with scikit-learn

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy, scikit-learn

**Builds on:** ML-14 Polynomial Features and Validation Curves

Read the lesson first: [article.md](article.md)

## Task

Write `cv_report(model, X, y, n_splits=5, seed=0, stratified=False, scoring=None)` returning
`{"scores": list[float], "mean": float, "std": float}`.

* Folds: `KFold(n_splits, shuffle=True, random_state=seed)`, or `StratifiedKFold` with the same
  arguments when `stratified` is true.
* Use `cross_val_score(model, X, y, cv=folds, scoring=scoring)`; `std` is the population standard
  deviation of the scores (NumPy's default).
* Raise `ValueError` if `n_splits < 2` or `X` and `y` differ in length.

## Hints

<details><summary>Hint 1</summary>

Choose the splitter class from `stratified`, then build it with `shuffle=True, random_state=seed`.

</details>

<details><summary>Hint 2</summary>

`scores = cross_val_score(model, X, y, cv=folds, scoring=scoring)`.

</details>

<details><summary>Hint 3</summary>

Return `[float(s) for s in scores]`, `float(scores.mean())` and `float(scores.std())`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_matches_manual_loop` | Use KFold(n_splits, shuffle=True, random_state=seed) and cross_val_score. |
| `test_stratified_folds` | Use StratifiedKFold when stratified is true. |
| `test_scoring_argument` | Pass scoring through to cross_val_score. |
| `test_invalid` | Reject n_splits < 2 and mismatched lengths. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The splitter defines the folds; `cross_val_score` clones and fits the model once per fold and
returns the held-out scores. The mean is the estimate and the standard deviation shows how much
it moves from fold to fold.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
