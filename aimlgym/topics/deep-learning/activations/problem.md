# DL-01 · Activation Functions

**Topic:** Deep Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** ML-11 Logistic Regression from Scratch

Read the lesson first: [article.md](article.md)

## Task

Implement element-wise functions on NumPy arrays (return new float arrays; inputs unchanged):
`relu(z)`, `relu_grad(z)` (0 at z = 0), `leaky_relu(z, alpha=0.01)`,
`leaky_relu_grad(z, alpha=0.01)` (alpha at z = 0), `tanh(z)`, `tanh_grad(z)`.

**Examples**
```python
relu(np.array([-2., 0., 3.]))              # [0., 0., 3.]
leaky_relu(np.array([-2., 3.]), alpha=0.1) # [-0.2, 3.]
tanh_grad(np.array([0.]))                  # [1.]
```

## Hints

<details><summary>Hint 1</summary>

`np.maximum(z, 0.0)` for ReLU; `(z > 0).astype(float)` for its gradient.

</details>

<details><summary>Hint 2</summary>

`np.where(z > 0, z, alpha * z)` and `np.where(z > 0, 1.0, alpha)`.

</details>

<details><summary>Hint 3</summary>

`t = np.tanh(z); 1 - t ** 2`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_relu` | relu_grad(0) must be 0 — use z > 0, not z >= 0. |
| `test_leaky` | Leaky gradient is alpha for z <= 0. |
| `test_numeric_grads` | tanh′(z) = 1 − tanh(z)², not 1 − z². |
| `test_no_mutation` | Return new arrays; don't assign into z. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each function is one vectorised expression. Gradients use strict `z > 0`, giving the framework
convention at zero. All functions build new arrays, so inputs are never modified.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
