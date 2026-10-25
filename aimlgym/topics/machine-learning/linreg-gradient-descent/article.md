# Training Linear Regression with Gradient Descent

## Learning outcomes

After this lesson you can:

- Derive the MSE gradient in vector form
- Train with batch gradient descent
- Verify against the closed-form solution

## Intuition
Closed forms don't exist for most models. Gradient descent (MA-13) works for all differentiable
losses: compute how the loss changes with each weight, step against it, repeat.

## Precise explanation
Model $\hat y = Xw + b$, loss $L = \frac1n\lVert \hat y - y\rVert^2$. With residual
$r = \hat y - y$:
$$\nabla_w L = \frac{2}{n} X^\top r,\qquad \frac{\partial L}{\partial b} = \frac{2}{n}\sum_i r_i.$$
Update: $w \leftarrow w - \eta \nabla_w L$, $b \leftarrow b - \eta\,\partial L/\partial b$.
**Batch** gradient descent uses all rows every step. Standardised features let one learning rate
work for all weights. The result should match `np.linalg.lstsq`.

## Worked example
One feature, x = [0, 1, 2], y = [1, 3, 5], start w = b = 0: r = [−1, −3, −5];
∂w = (2/3)(0·−1 + 1·−3 + 2·−5) = −8.67, ∂b = (2/3)(−9) = −6. With η = 0.1:
w = 0.867, b = 0.6.

## Common mistakes
* Forgetting the factor 2/n (only scales the learning rate, but tests expect the exact gradient).
* `X @ r` instead of `X.T @ r` (shape error or wrong result).
* Learning rate too large → loss explodes (MA-13).

## Why this matters
This loop — forward, loss, gradient, update — is exactly how neural networks (DL), logistic
regression (ML-11) and federated clients (FL-06) are trained.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [Mathematics for Machine Learning](https://mml-book.github.io/) — Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong (Cambridge University Press) (`S009`)
