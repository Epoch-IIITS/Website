# XA-06 · Partial Dependence by Hand

**Topic:** Explainable AI · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** XA-04 Individual Conditional Expectation

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `partial_dependence(predict, X, feature, grid)` → array of average predictions per grid value.
* `ice_spread(predict, X, feature, grid)` → float: the mean over grid points of the standard deviation
  (population) across instances of **centred** ICE curves (each curve minus its value at `grid[0]`).
Raise `ValueError` for empty `X`/`grid` or an invalid feature.

**Example**
```python
f = lambda X: X[:, 0] * X[:, 1]
X = np.array([[0., -1.], [0., 1.]])
partial_dependence(f, X, 0, [0, 1, 2])   # [0., 0., 0.]
ice_spread(f, X, 0, [0, 1, 2])           # 1.0  (curves 0,-1,-2 and 0,1,2)
```

## Hints

<details><summary>Hint 1</summary>

Write `_ice_matrix` returning shape `(n, m)`: for each grid value g, copy X, set column, predict.

</details>

<details><summary>Hint 2</summary>

PD = `ice.mean(axis=0)`.

</details>

<details><summary>Hint 3</summary>

Centred: `ice - ice[:, [0]]`; spread = `centred.std(axis=0).mean()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_interaction_flat` | PD averages predictions over instances with the feature fixed at each grid value. |
| `test_spread` | Centre each ICE curve at grid[0], then take the std across instances and average over the grid. |
| `test_additive_no_spread` | Additive effects give parallel ICE curves, hence zero spread. |
| `test_no_mutation` | Copy X before overwriting the feature column. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The helper builds the full ICE matrix (instances × grid values). Averaging over instances gives PD;
centring each ICE curve and measuring the spread across instances quantifies heterogeneity that
signals interactions.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
