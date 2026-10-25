# XA-14 · Integrated Gradients

**Topic:** Explainable AI · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** XA-11 Exact Shapley Values, DL-10 Backprop Through One Neuron

Read the lesson first: [article.md](article.md)

## Task

Write `integrated_gradients(grad_fn, x, baseline, steps=50)` where `grad_fn(points)` takes an array
`(m, d)` of inputs and returns their gradients `(m, d)`. Use the midpoint rule with a **single**
`grad_fn` call on all path points. Return `(attributions, alphas)`. Raise `ValueError` if
`steps < 1` or shapes differ.

**Example**
```python
grad = lambda P: np.column_stack([2 * P[:, 0] * P[:, 1], P[:, 0] ** 2])
ig, _ = integrated_gradients(grad, np.array([1., 2.]), np.zeros(2), steps=1000)
ig        # ≈ [1.33333, 0.66667]
```

## Hints

<details><summary>Hint 1</summary>

`alphas = (np.arange(steps) + 0.5) / steps`.

</details>

<details><summary>Hint 2</summary>

`points = baseline + alphas[:, None] * (x - baseline)`.

</details>

<details><summary>Hint 3</summary>

`ig = (x - baseline) * grad_fn(points).mean(axis=0)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_alphas_midpoint` | Midpoint rule: alpha_k = (k + 0.5) / steps. |
| `test_completeness` | Multiply the averaged gradient by (x − baseline). |
| `test_single_call` | Build all path points and call grad_fn once. |
| `test_saturation_vs_gradient` | IG captures effects even where the local gradient is ~0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

All points along the straight path are built at once and their gradients computed in one batch; the
midpoint average approximates the path integral, and multiplying by the input–baseline difference
gives the attribution per feature.

## References

- [Axiomatic Attribution for Deep Networks](https://arxiv.org/abs/1703.01365) — Mukund Sundararajan, Ankur Taly, Qiqi Yan (`S027`)
- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
