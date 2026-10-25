# DL-19 · Train an MLP on XOR

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** DL-11 Backpropagation Through a Dense Layer, DL-14 SGD with Momentum

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `init_params(n_hidden, seed)` → dict with `W1 (2, H)`, `b1 (H,)`, `W2 (H, 1)`, `b2 (1,)`,
  using `rng = np.random.default_rng(seed)`; `W1 = rng.normal(0, 1, (2, H))` then
  `W2 = rng.normal(0, 1, (H, 1))`; biases zero.
* `forward_backward(X, y, params)` → `(loss, grads)` where `y` has shape `(n,)` and grads has the
  same keys/shapes as params, following the formulas above (BCE with p clipped to [1e-12, 1−1e-12]
  for the loss value).
* `train_xor(n_hidden=8, lr=1.0, epochs=3000, seed=0)` → `(params, history)` trained by full-batch
  gradient descent on the 4 XOR points (`X = [[0,0],[0,1],[1,0],[1,1]]`, `y = [0,1,1,0]`), history =
  loss before each update.

**Example**
```python
params, hist = train_xor()
hist[-1] < 0.05        # True
```

## Hints

<details><summary>Hint 1</summary>

Forward: `h = np.tanh(X @ W1 + b1)`, `p = sigmoid(h @ W2 + b2)[:, 0]`.

</details>

<details><summary>Hint 2</summary>

`d2 = ((p - y) / n)[:, None]`; `d1 = (d2 @ W2.T) * (1 - h ** 2)`.

</details>

<details><summary>Hint 3</summary>

Grads: `W2: h.T @ d2`, `b2: d2.sum(0)`, `W1: X.T @ d1`, `b1: d1.sum(0)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_gradients_numeric` | Check δ1 = (δ2 W2ᵀ) ⊙ (1 − h²) and that δ2 is divided by n. |
| `test_init_recipe` | Draw W1 then W2 from one default_rng(seed); biases are zeros. |
| `test_trains` | Compute all gradients first, then update every parameter with lr. |
| `test_initial_loss_value` | With zero weights p = 0.5 everywhere, so the loss is log 2. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The forward pass stores h and p, the backward pass propagates δ from the output to the hidden
layer using the tanh derivative, and all gradients are computed before any update. Full-batch
gradient descent then drives the loss toward zero; the hidden layer makes XOR linearly separable.

## References

- [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) — free online book (author not stated on landing page) (`S014`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
