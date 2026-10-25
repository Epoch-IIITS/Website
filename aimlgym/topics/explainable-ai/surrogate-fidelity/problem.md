# XA-10 · Global Surrogate and Fidelity

**Topic:** Explainable AI · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** XA-07 Permutation Importance with sklearn.inspection, ML-09 Least-Squares Line

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `fit_linear_surrogate(predict, X)` → `(intercept, coef)` from least squares of `predict(X)` on
  `[1, X]` (`np.linalg.lstsq`, `rcond=None`).
* `fidelity_r2(predict, surrogate, X)` → R² of `surrogate(X)` against `predict(X)`; if the black box
  is constant on X, return 1.0 when the surrogate matches it exactly (within 1e-12) else 0.0.

**Example**
```python
f = lambda X: 2 * X[:, 0] - X[:, 1] + 3
b, w = fit_linear_surrogate(f, X)     # (3.0, [2., -1.])
fidelity_r2(f, lambda X: b + X @ w, X)  # 1.0
```

## Hints

<details><summary>Hint 1</summary>

`yhat = predict(X)`; `A = np.column_stack([np.ones(len(X)), X])`.

</details>

<details><summary>Hint 2</summary>

`w, *_ = np.linalg.lstsq(A, yhat, rcond=None)`; return `w[0], w[1:]`.

</details>

<details><summary>Hint 3</summary>

R² = 1 − Σ(yhat − s)² / Σ(yhat − mean)²; handle zero denominator.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_fits_predictions_not_labels` | Fit the surrogate to predict(X), the black box's outputs. |
| `test_linear_recovered` | Include an intercept column of ones in the least-squares design. |
| `test_nonlinear_low_fidelity` | Fidelity is R² between black-box and surrogate predictions. |
| `test_constant_blackbox` | Handle zero variance of the black-box predictions explicitly. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The surrogate is fitted to the black box's own outputs, so it learns to imitate the model rather than
the data. Fidelity is R² between the two models' predictions, with an explicit rule for a constant
black box.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
