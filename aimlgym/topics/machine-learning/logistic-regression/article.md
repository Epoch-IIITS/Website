# Logistic Regression

## Learning outcomes

After this lesson you can:

- Implement a numerically stable sigmoid and log-loss
- Derive the log-loss gradient (p − y)
- Train and threshold a binary classifier

## Intuition
To predict a probability, squash a linear score into (0, 1) with the S-shaped **sigmoid**. Train
by rewarding confident correct predictions and heavily penalising confident wrong ones.

## Precise explanation
$p = \sigma(z) = \frac{1}{1+e^{-z}}$, $z = Xw + b$.
**Log-loss (binary cross-entropy):**
$$L = -\frac1n\sum \big[y\log p + (1-y)\log(1-p)\big].$$
Its gradient is remarkably simple: $\nabla_w L = \frac1n X^\top (p - y)$,
$\partial L/\partial b = \frac1n\sum (p-y)$.

**Numerical stability:** for $z = -1000$, `np.exp(1000)` overflows. A stable sigmoid uses
$e^{-|z|}$: for $z\ge0$, $1/(1+e^{-z})$; for $z<0$, $e^{z}/(1+e^{z})$. Clip $p$ into
$[\epsilon, 1-\epsilon]$ before taking logs (ε = 1e−12) so $\log 0$ never occurs.

Predict class 1 when $p \ge 0.5$ (threshold adjustable). The decision boundary $Xw + b = 0$ is
linear.

## Worked example
w = [2], b = −1, x = 1: z = 1, p = 0.731; if y = 1 the loss is −log 0.731 = 0.313.

## Common mistakes
* Using MSE for classification (non-convex with sigmoid, slow learning).
* Overflow warnings from a naive sigmoid.
* `log(0)` → −inf loss.

## Why this matters
Logistic regression is the standard baseline classifier and is exactly a one-neuron network with
sigmoid output — the bridge to Deep Learning.

## Library implementation

`sklearn.linear_model.LogisticRegression` fits the same model with a second-order solver (L-BFGS)
instead of fixed-step gradient descent, and adds L2 regularisation by default (strength `1/C`).
With a very large `C` the regularisation vanishes, and after enough epochs your gradient descent
reaches nearly the same probabilities. The comparison runs when scikit-learn is installed.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
