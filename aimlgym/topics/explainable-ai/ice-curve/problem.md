# XA-04 · Individual Conditional Expectation

**Topic:** Explainable AI · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** XA-01 Linear Model Contributions

Read the lesson first: [article.md](article.md)

## Task

Write `ice_curve(predict, x, feature, grid)` returning a NumPy array of predictions, one per grid
value, computed with a **single** call to `predict` on an `(len(grid), d)` matrix. `x` must not be
modified. Raise `ValueError` if `feature` is out of range or `grid` is empty.

**Example**
```python
predict = lambda X: X[:, 0] * X[:, 1]
ice_curve(predict, np.array([2., 3.]), 0, [0, 1, 2])   # [0., 3., 6.]
```

## Hints

<details><summary>Hint 1</summary>

`X = np.tile(x, (len(grid), 1))`.

</details>

<details><summary>Hint 2</summary>

`X[:, feature] = grid`.

</details>

<details><summary>Hint 3</summary>

`return np.asarray(predict(X), dtype=float)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_single_call` | Build one (len(grid), d) matrix and call predict once. |
| `test_no_mutation` | Tile copies of x; never write into x. |
| `test_other_features_fixed` | Only the chosen column changes. |
| `test_errors` | Validate the feature index and non-empty grid. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Tiling creates independent copies of the instance, one per grid value, so the original stays intact.
Overwriting a single column and predicting the whole matrix gives the ICE curve in one model call.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
