# DL-07 · MLP Forward Pass

**Topic:** Deep Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** DL-04 Dense Layer Forward Pass

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `mlp_forward(X, params)` → `(logits, cache)` where `params` is a non-empty list of `(W, b)`;
  ReLU after every layer except the last; `cache` is a list with one dict per layer
  `{"a_prev": ..., "z": ...}`.
* `predict_classes(X, params)` → integer array of argmax over logits.

**Example**
```python
params = [(np.eye(2), np.zeros(2)), (np.array([[2.], [3.]]), np.array([0.5]))]
logits, cache = mlp_forward(np.array([[1., -1.]]), params)
logits        # [[2.5]]
cache[1]["a_prev"]   # [[1., 0.]]
```

## Hints

<details><summary>Hint 1</summary>

Loop `for l, (W, b) in enumerate(params)` with `a = X` initially.

</details>

<details><summary>Hint 2</summary>

`z = a @ W + b`; store `{'a_prev': a, 'z': z}`; apply ReLU unless it's the last layer.

</details>

<details><summary>Hint 3</summary>

`mlp_forward(X, params)[0].argmax(axis=1)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_no_relu_on_output` | Don't apply ReLU to the last layer. |
| `test_example` | Cache the layer input a_prev and pre-activation z for every layer. |
| `test_matches_manual` | Apply ReLU between layers: a = max(z, 0). |
| `test_predict` | Predictions are argmax over axis 1 of the logits. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each iteration applies one dense layer, records its input and pre-activation for later
backpropagation, and applies ReLU except at the output. Class predictions use argmax on the
logits.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) — free online book (author not stated on landing page) (`S014`)
