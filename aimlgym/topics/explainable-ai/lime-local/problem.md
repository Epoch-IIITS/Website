# XA-12 · LIME-style Local Linear Explanation

**Topic:** Explainable AI · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** XA-10 Global Surrogate and Fidelity, ML-19 Regularisation and Hyperparameter Search

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `sample_masks(n, d, rng)` → int array `(n, d)` of 0/1 with **row 0 all ones** and the other rows
  `(rng.random((n-1, d)) < 0.5).astype(int)`.
* `lime_explain(predict, x, baseline, masks, kernel_width=0.75)` → dict
  `{"intercept": float, "coef": array(d), "weights": array(n)}` via weighted least squares
  (`np.linalg.lstsq` on `sqrt(weights)`-scaled design `[1, masks]` and targets). Raise `ValueError`
  if `kernel_width <= 0` or shapes mismatch.

**Example**
```python
f = lambda X: 2 * X[:, 0] - X[:, 1]
m = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])
lime_explain(f, np.array([3., 1.]), np.zeros(2), m)["coef"]   # [ 6., -1.]
```

## Hints

<details><summary>Hint 1</summary>

Inputs: `Xz = masks * x + (1 - masks) * baseline`; `y = predict(Xz)`.

</details>

<details><summary>Hint 2</summary>

`D = 1 - masks.mean(axis=1)`; `w = np.exp(-D**2 / kernel_width**2)`.

</details>

<details><summary>Hint 3</summary>

`A = np.column_stack([ones, masks]) * sqrt(w)[:, None]`; `beta = lstsq(A, y * sqrt(w))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_linear_exact` | Fit on the binary masks (with intercept), not on the raw perturbed inputs. |
| `test_weights` | D = fraction of features removed; weight = exp(−D²/σ²). |
| `test_masks_recipe` | Row 0 is all ones; other rows are rng.random((n−1, d)) < 0.5. |
| `test_matches_shapley_linear_random_masks` | Scale both the design rows and targets by sqrt(weight) before lstsq. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Masks map to concrete inputs by mixing the instance with the baseline. Samples closer to the
instance (fewer features removed) get larger kernel weights. Scaling rows by the square root of the
weights turns weighted least squares into ordinary least squares, whose coefficients are the local
explanation.

## References

- ["Why Should I Trust You?": Explaining the Predictions of Any Classifier](https://arxiv.org/abs/1602.04938) — Marco Tulio Ribeiro, Sameer Singh, Carlos Guestrin (`S025`)
- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
