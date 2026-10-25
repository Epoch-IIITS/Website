# DL-16 · The Adam Optimiser

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** DL-14 SGD with Momentum

Read the lesson first: [article.md](article.md)

## Task

Write `class Adam` with the same interface as `Momentum` in DL-14:

* `Adam(lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8)`; raise `ValueError` unless `lr > 0` and
  `0 <= beta1 < 1` and `0 <= beta2 < 1`.
* Attributes `m` and `v` (dicts, filled lazily per key with zeros) and `t` (starts at 0).
* `step(params, grads)` — both dicts of arrays with the same keys and shapes (else
  `ValueError`); increment `t` once, update every parameter by the formulas above, and return a
  **new** dict of updated parameters (do not modify the inputs).

## Hints

<details><summary>Hint 1</summary>

Validate in `__init__`; in `step`, compare `set(params) != set(grads)` and each pair of shapes.

</details>

<details><summary>Hint 2</summary>

Increment `self.t` once at the start of `step`, then loop over keys; create zeros with `np.zeros_like(p)` the first time a key is seen.

</details>

<details><summary>Hint 3</summary>

`m_hat = m / (1 - beta1 ** t)`, `v_hat = v / (1 - beta2 ** t)`, `p - lr * m_hat / (np.sqrt(v_hat) + eps)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_first_step_is_lr_sign` | With bias correction the first step is about `lr * sign(g)`. |
| `test_matches_reference_recurrence` | Check both moment updates, the bias corrections with the shared `t`, and where eps goes. |
| `test_scale_invariance` | Divide by `sqrt(v_hat) + eps`, which cancels the gradient's scale. |
| `test_does_not_mutate_and_counts_once` | Increment `t` once per step call, not once per parameter, and return new arrays. |
| `test_validation` | Validate the hyperparameters and the keys/shapes of params and grads. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The optimiser keeps per-parameter moment estimates in dictionaries keyed like the parameters and a
single step counter. Bias-corrected moments give an update whose size is about `lr` per
coordinate, independent of the gradient's scale. New arrays are returned so callers' parameters
are never modified in place.

## References

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — Kingma & Ba (`S095`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
