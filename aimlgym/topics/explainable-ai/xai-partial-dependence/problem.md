# XA-05 · Partial Dependence with sklearn.inspection

**Topic:** Explainable AI · **Difficulty:** intermediate · **Allowed packages:** numpy, scikit-learn

**Builds on:** XA-04 Individual Conditional Expectation, ML-22 Decision Trees and Random Forests

Read the lesson first: [article.md](article.md)

## Task

Write `pd_curve(model, X, feature, grid_resolution=20, kind="average")` returning
`{"grid": list[float], "values": ...}` from `partial_dependence(model, X, features=[feature],
grid_resolution=grid_resolution, kind=kind)`:

* `kind="average"`: `values` is the list of average predictions (one per grid value);
* `kind="individual"`: `values` is a list of ICE curves, one list per row of `X`.

Raise `ValueError` for another kind or a feature index outside the columns of `X`.

## Hints

<details><summary>Hint 1</summary>

Validate `kind in ("average", "individual")` and `0 <= feature < X.shape[1]`.

</details>

<details><summary>Hint 2</summary>

`result = partial_dependence(model, X, features=[feature], grid_resolution=grid_resolution, kind=kind)`.

</details>

<details><summary>Hint 3</summary>

`result["grid_values"][0]` and `result[kind][0]`; convert with `.tolist()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_linear_slope` | Use partial_dependence with features=[feature] and kind='average'. |
| `test_grid_within_percentiles` | Return result['grid_values'][0] as the grid. |
| `test_individual_curves_average` | For kind='individual' return result['individual'][0]. |
| `test_invalid` | Reject unknown kinds and out-of-range feature indices. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`partial_dependence` builds the grid from the feature's central percentiles, predicts with the feature
replaced by each grid value, and either averages over rows (partial dependence) or keeps every row's
curve (ICE). The function returns the grid and the requested curves as plain lists.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
