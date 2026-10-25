# DL-11 · Backpropagation Through a Dense Layer

**Topic:** Deep Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** DL-10 Backprop Through One Neuron

Read the lesson first: [article.md](article.md)

## Task

Implement with NumPy:

1. `dense_backward(X, W, dY)` → `(dX, dW, db)`.
2. `relu_backward(Z, dA)` → `dZ`.
3. `mse_and_grad(Y_hat, Y)` → `(loss, dY_hat)` with the mean over **all** entries; `loss` is a
   float.
4. `two_layer_grads(X, Y, params)` with `params = {"W1", "b1", "W2", "b2"}` for
   $H = \mathrm{ReLU}(XW_1+b_1)$, $\hat Y = HW_2 + b_2$ → `(loss, grads)` where `grads` has the
   same keys and shapes as `params`.

## Hints

<details><summary>Hint 1</summary>

`dW = X.T @ dY`, `db = dY.sum(axis=0)`, `dX = dY @ W.T`.

</details>

<details><summary>Hint 2</summary>

`relu_backward` is `dA * (Z > 0)`; the MSE gradient is `2 * diff / diff.size`.

</details>

<details><summary>Hint 3</summary>

Forward: `Z1 = X @ W1 + b1`, `H = np.maximum(Z1, 0)`, `Y_hat = H @ W2 + b2`; backward: dense (layer 2) → relu → dense (layer 1).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Use `dW = X.T @ dY`, `db = dY.sum(axis=0)`, `dX = dY @ W.T`. |
| `test_shapes` | Each gradient must have the shape of what it differentiates. |
| `test_relu_backward` | Pass the gradient only where Z > 0. |
| `test_mse` | Divide by the total number of entries: `2 * diff / diff.size`. |
| `test_two_layer_numeric` | Run the forward pass, then dense (layer 2) → ReLU → dense (layer 1). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The dense rule follows from $Y_{ij} = \sum_k X_{ik}W_{kj} + b_j$; each output is a transposed product
that matches the parameter's shape. ReLU masks the upstream gradient, and the MSE gradient is
$2(\hat Y - Y)/m$. The two-layer network simply chains these pieces from the loss back to the
input, reusing values cached during the forward pass.

## References

- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
