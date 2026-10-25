# ML-20 · Ridge Regression (Closed Form)

**Topic:** Machine Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** ML-17 k-Fold Cross-Validation by Hand, ML-08 Standard Scaler (fit on train only)

Read the lesson first: [article.md](article.md)

## Task

Implement `class Ridge(alpha=1.0)` with `coef_` (shape `(d,)`) and `intercept_` (float):
* `fit(X, y)` — centred closed form above, solved with `np.linalg.solve`; returns `self`.
  Raise `ValueError` if `alpha < 0`. (With `alpha == 0` and singular `X_c^T X_c`,
  `np.linalg.solve` may raise `LinAlgError`; that is acceptable.)
* `predict(X)`; raise `RuntimeError` before fit.

**Example**
```python
X = np.array([[1., 1.], [2., 2.], [3., 3.]]); y = np.array([2., 4., 6.])
Ridge(alpha=1e-6).fit(X, y).coef_    # ≈ [1., 1.]  (collinear columns share the weight)
```

## Hints

<details><summary>Hint 1</summary>

`xm, ym = X.mean(axis=0), y.mean()`; `Xc, yc = X - xm, y - ym`.

</details>

<details><summary>Hint 2</summary>

`A = Xc.T @ Xc + alpha * np.eye(d)`; `w = np.linalg.solve(A, Xc.T @ yc)`.

</details>

<details><summary>Hint 3</summary>

`intercept = ym - xm @ w`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_intercept_not_penalised` | Centre X and y; compute the intercept from the means. |
| `test_shrinkage` | Add alpha·I to Xcᵀ Xc (not to the whole design matrix with a bias column). |
| `test_collinear` | Use np.linalg.solve on (XcᵀXc + αI). |
| `test_alpha0_is_ols` | With alpha = 0 you should recover ordinary least squares. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Centring removes the intercept from the penalised problem; the α·I term makes the system
well-conditioned. The intercept is recovered from the means so that the fitted plane passes
through (X̄, ȳ).

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
