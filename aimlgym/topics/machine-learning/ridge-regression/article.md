# Ridge Regression

## Learning outcomes

After this lesson you can:

- Add L2 regularisation to least squares
- Leave the intercept unpenalised via centring
- Observe shrinkage and stability with collinear features

## Intuition
When features are nearly duplicates, ordinary least squares can produce wild coefficients that
cancel each other (+500 and −499). Ridge regression adds a penalty on large weights, preferring
smaller, more stable coefficients — trading a little bias for much less variance.

## Precise explanation
Minimise $\lVert y - Xw - b\rVert^2 + \alpha \lVert w\rVert^2$ ($\alpha \ge 0$). The intercept is
**not** penalised. Centre the data ($X_c = X - \bar X$, $y_c = y - \bar y$), then
$$w = (X_c^\top X_c + \alpha I)^{-1} X_c^\top y_c,\qquad b = \bar y - \bar X w.$$
Solve with `np.linalg.solve`, not an explicit inverse. For $\alpha > 0$ the matrix is always
invertible, even with perfectly collinear features. $\alpha = 0$ recovers OLS; as $\alpha \to
\infty$, $w \to 0$ and predictions → $\bar y$. Choose α by cross-validation (ML-17).

## Worked example
Two identical columns x and x, y = 2x: OLS is singular (any w₁ + w₂ = 2 works); ridge with small
α gives the symmetric solution w ≈ [1, 1].

## Common mistakes
* Penalising the intercept (adding α to the bias term).
* Not scaling features — the penalty then depends on units.
* Using `np.linalg.inv` (less stable).

## Why this matters
L2 regularisation (weight decay) is used in almost every neural network; ridge is the cleanest
place to see the bias–variance trade-off.

## Library implementation

`sklearn.linear_model.Ridge(alpha=...)` solves the same penalised least-squares problem and, like
your class, does not penalise the intercept (it centres the data first).

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
