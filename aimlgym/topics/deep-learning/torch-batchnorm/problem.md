# DL-22 · Batch Normalisation with nn.BatchNorm1d

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** DL-20 Dropout with train() and eval()

Read the lesson first: [article.md](article.md)

## Task

Write `run_batchnorm(batches, x_eval, momentum=0.1)` that creates one
`nn.BatchNorm1d(n_features, momentum=momentum)`, passes every batch through it in training mode
(in order), then evaluates `x_eval` in evaluation mode. Return
`{"running_mean": list[float], "running_var": list[float], "train_output": list[list[float]], "eval_output": list[list[float]]}`
where `train_output` is the output for the **last** training batch.

* Each batch and `x_eval` are 2-D `(n, n_features)`; convert them to float32 tensors.
* Raise `ValueError` if `batches` is empty or any batch has fewer than 2 rows.
* Compute outputs under `torch.no_grad()`.

## Hints

<details><summary>Hint 1</summary>

Convert each batch with `torch.as_tensor(b, dtype=torch.float32)` and check its row count.

</details>

<details><summary>Hint 2</summary>

`bn = nn.BatchNorm1d(n_features, momentum=momentum)`; `bn.train()` and pass the batches; then `bn.eval()`.

</details>

<details><summary>Hint 3</summary>

Read `bn.running_mean.tolist()` and `bn.running_var.tolist()` after the training batches.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_running_statistics_formula` | Pass the batches in training mode with momentum=momentum; running_var uses the unbiased variance. |
| `test_eval_uses_running_statistics` | Call bn.eval() before evaluating x_eval. |
| `test_train_output_standardised` | Return the output of the last training batch. |
| `test_invalid_batches` | Reject an empty list and batches with fewer than two rows. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

In training mode each batch is standardised with its own (biased) statistics and the running
averages move towards the batch's mean and unbiased variance. After switching to evaluation, the
layer standardises with the running averages, so its output no longer depends on the batch.

## References

- [torch.nn.BatchNorm1d](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html) — PyTorch (`S112`)
- [Build the Neural Network (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) — PyTorch (`S104`)
