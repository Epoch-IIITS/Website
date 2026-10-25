# XA-07 · Permutation Importance with sklearn.inspection

**Topic:** Explainable AI · **Difficulty:** intermediate · **Allowed packages:** numpy, pandas, scikit-learn

**Builds on:** XA-05 Partial Dependence with sklearn.inspection

Read the lesson first: [article.md](article.md)

## Task

Write `importance_table(model, X, y, n_repeats=10, seed=0, scoring=None)` for a fitted model (or
pipeline) and a pandas DataFrame `X`, returning a list of `(column, mean, std)` tuples sorted by mean
importance descending (ties by column name), using
`permutation_importance(model, X, y, n_repeats=n_repeats, random_state=seed, scoring=scoring)`.

Raise `ValueError` if `n_repeats < 1` or `X` is not a DataFrame.

## Hints

<details><summary>Hint 1</summary>

Check `isinstance(X, pd.DataFrame)` and the repeat count.

</details>

<details><summary>Hint 2</summary>

`result = permutation_importance(model, X, y, n_repeats=n_repeats, random_state=seed, scoring=scoring)`.

</details>

<details><summary>Hint 3</summary>

Zip `X.columns`, `result.importances_mean` and `result.importances_std`, then sort by `(-mean, column)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_order` | Sort rows by mean importance, largest first. |
| `test_original_columns` | Pass the whole pipeline and the DataFrame so rows are original columns. |
| `test_matches_library` | Use permutation_importance with random_state=seed and the given scoring. |
| `test_invalid` | Require a DataFrame and n_repeats >= 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The function shuffles each original column of the DataFrame several times, measures the drop in score
of the whole pipeline, and reports the mean and spread per column, most important first.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
