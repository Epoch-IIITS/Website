# DL-04 · Dense Layer Forward Pass

**Topic:** Deep Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** DL-01 Activation Functions, NP-06 Matrix Products with @

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `dense(X, W, b)` → `X @ W + b`; raise `ValueError` on any shape mismatch
  (`X` must be 2-D, `W.shape[0] == X.shape[1]`, `b.shape == (W.shape[1],)`).
* `n_params(layer_sizes)` → total weights + biases for consecutive dense layers (int); raise
  `ValueError` for fewer than 2 sizes or non-positive sizes.
* `he_init(fan_in, fan_out, rng)` → `(W, b)` with `W = rng.normal(0, sqrt(2/fan_in), (fan_in, fan_out))`
  and `b = zeros(fan_out)`.

**Examples**
```python
dense(np.array([[1., 2.]]), np.array([[1., 0., -1.], [2., 1., 0.]]), np.array([0.5, 0., 0.]))
# [[5.5, 2., -1.]]
n_params([784, 128, 10])   # 101770
```

## Hints

<details><summary>Hint 1</summary>

Validate all three shapes, then `X @ W + b`.

</details>

<details><summary>Hint 2</summary>

`sum((a + 1) * c for a, c in zip(sizes[:-1], sizes[1:]))`.

</details>

<details><summary>Hint 3</summary>

`rng.normal(0.0, np.sqrt(2.0 / fan_in), size=(fan_in, fan_out))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_forward` | Compute X @ W + b (row-vector convention). |
| `test_shape_errors` | Check W rows == X columns and b length == W columns. |
| `test_n_params` | Each layer has (fan_in + 1) * fan_out parameters. |
| `test_he_stats` | Standard deviation is sqrt(2 / fan_in). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The forward pass is one matrix product plus a broadcast bias, guarded by shape checks. Each
layer has (inputs + 1) × outputs parameters. He initialisation scales the weight spread by the
fan-in to keep signal variance stable through ReLU layers.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) — free online book (author not stated on landing page) (`S014`)
