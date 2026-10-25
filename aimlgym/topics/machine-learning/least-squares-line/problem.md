# ML-09 · Least-Squares Line

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** ML-02 The scikit-learn Estimator API, ST-11 Covariance and Pearson Correlation

Read the lesson first: [article.md](article.md)

## Task

Implement `class SimpleLinearRegression` with attributes `intercept_`, `slope_` (None before fit):
* `fit(x, y)` — closed form; return `self`. Raise `ValueError` for fewer than 2 points,
  mismatched lengths, or constant `x`.
* `predict(x)` → NumPy array; raise `RuntimeError` if not fitted.
* `score(x, y)` → R² of predictions.

**Example**
```python
m = SimpleLinearRegression().fit([1, 2, 3, 4], [2, 4, 5, 8])
m.slope_, m.intercept_    # (1.9, 0.0)
m.predict([5])            # array([9.5])
```

## Hints

<details><summary>Hint 1</summary>

`dx = x - x.mean()`, `dy = y - y.mean()`; `sxx = (dx**2).sum()`.

</details>

<details><summary>Hint 2</summary>

`slope = (dx*dy).sum() / sxx`, `intercept = y.mean() - slope * x.mean()`.

</details>

<details><summary>Hint 3</summary>

R² = 1 − SS_res / SS_tot (ML-03).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_fit` | slope = Σdx·dy / Σdx²; intercept = ȳ − slope·x̄. |
| `test_matches_polyfit` | Centre x and y before multiplying. |
| `test_constant_x` | Raise ValueError when Σdx² = 0. |
| `test_not_fitted` | predict must raise RuntimeError before fit. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The slope is the centred cross-product over the centred sum of squares of x; the intercept makes
the line pass through the means. Prediction is a vectorised affine map; `score` computes R² from
residuals.

## References

- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
