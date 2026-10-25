# ML-10 · Linear Regression by Gradient Descent

**Topic:** Machine Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** ML-09 Least-Squares Line, MA-14 Numerical Gradient of f(x1..xn)

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `mse_grad(X, y, w, b)` → `(loss, grad_w, grad_b)` for $L = \text{mean}((Xw+b-y)^2)$.
* `fit_gd(X, y, lr=0.1, epochs=1000)` → `(w, b, history)` starting from zeros; `history` holds
  the loss **before** each update (length `epochs`).

Raise `ValueError` for shape mismatches, `lr <= 0` or `epochs < 1`.

**Example**
```python
X = np.array([[0.], [1.], [2.]]); y = np.array([1., 3., 5.])
mse_grad(X, y, np.zeros(1), 0.0)     # (11.666..., array([-8.666...]), -6.0)
w, b, h = fit_gd(X, y, lr=0.1, epochs=2000)   # w ≈ [2.0], b ≈ 1.0
```

## Hints

<details><summary>Hint 1</summary>

`r = X @ w + b - y`; `loss = np.mean(r ** 2)`.

</details>

<details><summary>Hint 2</summary>

`grad_w = 2 / n * X.T @ r`, `grad_b = 2 / n * r.sum()`.

</details>

<details><summary>Hint 3</summary>

In fit_gd append the loss, then update w and b.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_grad_values` | Gradient is (2/n)·Xᵀr with r = Xw + b − y. |
| `test_grad_numerical` | Compare your analytic gradient with central differences (MA-14). |
| `test_history_decreasing` | Record the loss before each update; use minus the gradient. |
| `test_matches_lstsq` | Update both w and b every epoch. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The residual vector gives both the loss and the gradients in two matrix expressions. The training
loop records the current loss and takes a step against the gradient. For a convex loss with a
suitable learning rate, the parameters converge to the least-squares solution.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
