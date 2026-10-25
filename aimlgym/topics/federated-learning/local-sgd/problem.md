# FL-06 · Local SGD on a Client

**Topic:** Federated Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** ML-10 Linear Regression by Gradient Descent, FL-03 Client Updates as Deltas

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `mse_grad(w, X, y)` → gradient of the mean squared error on `(X, y)`.
* `local_sgd(w, X, y, lr, epochs, batch_size, seed)` → new weight array following the recipe exactly.
  Raise `ValueError` if `lr <= 0`, `epochs < 1` or `batch_size < 1`.

**Example**
```python
X = np.array([[1., 0.], [0., 1.]]); y = np.array([1., 2.])
local_sgd(np.zeros(2), X, y, lr=0.5, epochs=1, batch_size=2, seed=0)   # [0.5, 1.0]
```

## Hints

<details><summary>Hint 1</summary>

`2 / len(y) * X.T @ (X @ w - y)`.

</details>

<details><summary>Hint 2</summary>

`rng = np.random.default_rng(seed)` once, outside the epoch loop.

</details>

<details><summary>Hint 3</summary>

`for s in range(0, n, batch_size): b = order[s:s + batch_size]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe` | Create the generator once; new permutation each epoch; batch-mean gradient per step. |
| `test_full_batch_one_step` | Gradient is 2/|B| · Xᵀ(Xw − y). |
| `test_no_mutation` | Copy w before updating (np.array(w)). |
| `test_converges` | The last batch of an epoch may be smaller — include it. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`np.array(w)` copies the global weights so the caller's array is untouched. One generator produces a
fresh permutation per epoch; each minibatch takes one gradient step with its own batch-mean gradient.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
