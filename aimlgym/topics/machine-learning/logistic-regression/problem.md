# ML-11 · Logistic Regression from Scratch

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** ML-10 Linear Regression by Gradient Descent, MA-03 The Sigmoid Function

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `sigmoid(z)` — stable, works on scalars and arrays, no overflow warnings for |z| up to 1e4.
* `log_loss(y, p, eps=1e-12)` — mean binary cross-entropy with clipping.
* `class LogisticRegression(lr=0.1, epochs=1000)` with `fit(X, y)` (batch GD from zeros, stores
  `w_`, `b_`, `history_` of losses before each update), `predict_proba(X)`,
  `predict(X, threshold=0.5)` (ints 0/1). Raise `ValueError` if `y` contains values other than 0/1.

**Example**
```python
sigmoid(np.array([-1000., 0., 1000.]))   # [0., 0.5, 1.]
log_loss([1, 0], [0.9, 0.1])             # 0.10536...
```

## Hints

<details><summary>Hint 1</summary>

Stable sigmoid: `e = np.exp(-np.abs(z)); np.where(z >= 0, 1/(1+e), e/(1+e))`.

</details>

<details><summary>Hint 2</summary>

Clip: `p = np.clip(p, eps, 1 - eps)` before logs.

</details>

<details><summary>Hint 3</summary>

Gradient: `g = (p - y)`; `w -= lr * X.T @ g / n`; `b -= lr * g.mean()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_sigmoid_extremes` | Use exp(-|z|) so the exponent is never positive. |
| `test_first_step` | Gradient is Xᵀ(p − y)/n; with w = 0, p = 0.5 for all rows. |
| `test_log_loss_clipped` | Clip p to [eps, 1 − eps] before log. |
| `test_fit_separable` | Update w and b every epoch and record history_ before the update. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The sigmoid only ever exponentiates a non-positive number, so it cannot overflow. Clipping keeps
the logs finite. The log-loss gradient with respect to the linear score is p − y, so training is
the same loop as ML-10 with a different output function.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
