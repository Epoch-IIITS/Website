# DL-21 · Inverted Dropout

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** DL-19 Train an MLP on XOR, NP-10 Seeded Random Generators

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `dropout_forward(x, p, rng, training=True)` → `(y, mask)`. In training, `mask = rng.random(x.shape) >= p`
  (boolean) and `y = x * mask / (1 - p)`; in evaluation return `(x.copy(), None)`.
  Raise `ValueError` unless `0 <= p < 1`.
* `dropout_backward(grad_out, mask, p)` → gradient w.r.t. `x`.

**Example**
```python
y, m = dropout_forward(np.ones(8), 0.5, np.random.default_rng(0))
set(np.unique(y)) <= {0.0, 2.0}    # True
dropout_forward(np.ones(3), 0.5, None, training=False)[0]   # [1., 1., 1.]
```

## Hints

<details><summary>Hint 1</summary>

Validate `0 <= p < 1` first.

</details>

<details><summary>Hint 2</summary>

`mask = rng.random(x.shape) >= p`; `y = x * mask / (1 - p)`.

</details>

<details><summary>Hint 3</summary>

Backward uses the same mask: `grad_out * mask / (1 - p)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe` | Mask = rng.random(x.shape) >= p; scale kept values by 1/(1 − p). |
| `test_eval_identity` | In evaluation mode return x unchanged and mask None. |
| `test_backward` | Reuse the forward mask and the same 1/(1 − p) scale. |
| `test_bad_p` | p must satisfy 0 <= p < 1. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Training mode samples a keep-mask with probability 1 − p and rescales the survivors, so the
expected output equals the input. Evaluation mode is the identity. The backward pass reuses the
forward mask because the operation is element-wise multiplication by a constant.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
