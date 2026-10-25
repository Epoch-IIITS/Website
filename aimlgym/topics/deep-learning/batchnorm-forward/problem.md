# DL-23 · Batch Normalization by Hand (train/eval)

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** DL-21 Inverted Dropout

Read the lesson first: [article.md](article.md)

## Task

Implement `class BatchNorm1d(n_features, momentum=0.1, eps=1e-5)` with attributes `gamma`,
`beta` (ones/zeros), `running_mean` (zeros), `running_var` (ones) and
`forward(x, training=True)`:
* training: normalise with batch mean / population variance, update running stats as above
  (unbiased variance; requires batch size ≥ 2, else `ValueError`), return `gamma * x_hat + beta`;
* evaluation: use running stats, no updates.
Raise `ValueError` if `x.shape[1] != n_features`.

**Example**
```python
bn = BatchNorm1d(1)
bn.forward(np.array([[1.], [3.]]))   # ≈ [[-1.], [1.]]
bn.running_mean, bn.running_var      # (array([0.2]), array([1.1]))
```

## Hints

<details><summary>Hint 1</summary>

`mu = x.mean(0)`, `var = x.var(0)` (population) for normalisation.

</details>

<details><summary>Hint 2</summary>

Unbiased: `var * n / (n - 1)` for the running variance update.

</details>

<details><summary>Hint 3</summary>

Eval: `(x - running_mean) / sqrt(running_var + eps)` then scale/shift.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_running_stats` | Running var uses the unbiased batch variance (× n/(n−1)) with momentum 0.1. |
| `test_eval_uses_running` | In eval mode use running statistics and do not update them. |
| `test_normalised_stats` | Normalise per feature over axis 0 (the batch). |
| `test_gamma_beta` | Output is gamma * x_hat + beta. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Training mode normalises with the batch's own statistics and updates exponential running
averages (unbiased variance). Evaluation mode normalises with the stored averages and leaves
state untouched, so outputs no longer depend on the other examples in the batch.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
