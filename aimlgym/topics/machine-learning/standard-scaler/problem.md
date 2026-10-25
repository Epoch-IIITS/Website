# ML-08 · Standard Scaler (fit on train only)

**Topic:** Machine Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** ML-05 Seeded Train/Test Split

Read the lesson first: [article.md](article.md)

## Task

Implement `class StandardScaler` with attributes `mean_` and `scale_` (both `None` until fit):
* `fit(X)` → stores column means and population stds (zero std replaced by 1.0); returns `self`.
* `transform(X)` → standardized array; raise `RuntimeError` if not fitted, `ValueError` if the
  number of columns differs from fit.
* `fit_transform(X)`, `inverse_transform(Z)`.

**Example**
```python
sc = StandardScaler().fit(np.array([[1., 10.], [3., 10.]]))
sc.mean_, sc.scale_        # (array([ 2., 10.]), array([1., 1.]))
sc.transform([[5., 10.]])  # array([[3., 0.]])
```

## Hints

<details><summary>Hint 1</summary>

In fit: `self.mean_ = X.mean(axis=0)`; `std = X.std(axis=0)`.

</details>

<details><summary>Hint 2</summary>

`self.scale_ = np.where(std == 0, 1.0, std)`.

</details>

<details><summary>Hint 3</summary>

Check `self.mean_ is None` in transform and compare `X.shape[1]` with `len(self.mean_)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_transform_test_point` | Use the stored training mean/std; never refit inside transform. |
| `test_fit_returns_self` | fit must `return self`. |
| `test_not_fitted` | Raise RuntimeError when transform is called before fit. |
| `test_fit_params` | Constant columns get scale 1.0 (not 0). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`fit` learns per-column statistics only from the data it is given and returns `self` for
chaining. `transform` reuses the stored statistics, so test data is scaled with training
parameters. A shared `_check` enforces fitting and column consistency.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
