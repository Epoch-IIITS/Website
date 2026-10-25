# XA-01 · Linear Model Contributions

**Topic:** Explainable AI · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** ML-09 Least-Squares Line

Read the lesson first: [article.md](article.md)

## Task

Write `contributions(w, b, x, baseline)` returning a dict
`{"phi": array, "prediction": float, "baseline_prediction": float}` for a linear model. Raise
`ValueError` if lengths differ.

**Example**
```python
r = contributions(np.array([2., -1.]), 5.0, np.array([3., 4.]), np.array([1., 1.]))
r["phi"], r["prediction"], r["baseline_prediction"]   # ([4., -3.], 7.0, 6.0)
```

## Hints

<details><summary>Hint 1</summary>

Convert all inputs with `np.asarray(..., float)` and compare shapes.

</details>

<details><summary>Hint 2</summary>

`phi = w * (x - baseline)`.

</details>

<details><summary>Hint 3</summary>

`prediction = float(w @ x + b)`; baseline prediction similarly.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_efficiency` | Contributions must be w * (x − baseline) so they sum to f(x) − f(baseline). |
| `test_example` | Return prediction and baseline_prediction as floats including the bias. |
| `test_at_baseline_zero` | At the baseline every contribution is zero. |
| `test_mismatch` | Validate that all vectors have the same length. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each feature's contribution is its weight times its deviation from the baseline; by linearity these
sum exactly to the change in prediction relative to the baseline input.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
