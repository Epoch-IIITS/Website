# DL-27 · Debugging Training

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** DL-26 Saving, Loading and Reproducibility

Read the lesson first: [article.md](article.md)

## Task

Write three functions.

1. `diagnose(losses)` returns `"diverging"` if any loss is not finite or the last loss is more than
   twice the first; `"stuck"` if the last loss is more than 0.95 × the first; otherwise `"learning"`.
   Raise `ValueError` for fewer than 2 losses.
2. `overfit_one_batch(model, X, y, steps=200, lr=0.01)` trains `model` on that one batch with
   `nn.CrossEntropyLoss` and `torch.optim.Adam`, returning the final loss as a float.
3. `train_with_clipping(model, X, y, lr, steps, max_norm=None)` trains with `nn.MSELoss` and
   `torch.optim.SGD(lr)`; when `max_norm` is given, call `clip_grad_norm_` between `backward()`
   and `step()`. Return the list of losses (recorded before each step).

Inputs are converted with `torch.as_tensor` (float32 features; `torch.long` labels for
`overfit_one_batch`, float32 targets of shape `(n, 1)` for `train_with_clipping`).

## Hints

<details><summary>Hint 1</summary>

`diagnose`: check `math.isfinite` for every loss first, then compare the last loss with the first.

</details>

<details><summary>Hint 2</summary>

Both training functions use the usual cycle: zero_grad, loss, backward, (clip), step.

</details>

<details><summary>Hint 3</summary>

`torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)` goes after `loss.backward()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_diagnose_patterns` | Check for non-finite values first, then last > 2 × first, then last > 0.95 × first. |
| `test_overfit_tiny_batch` | Train with CrossEntropyLoss and Adam for the given steps and return the final loss. |
| `test_clipping_keeps_training_stable` | Call clip_grad_norm_ after backward() and before step(). |
| `test_high_lr_diverges_without_clipping` | Record each loss before the update, using MSELoss and SGD. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`diagnose` encodes the loss-curve table. Overfitting one batch is a plain training loop on a tiny
fixed batch; reaching a near-zero loss shows the model, labels and loss are wired correctly.
Clipping rescales the gradients after `backward()` so that no single step can be enormous.

## References

- [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) — Andrej Karpathy (`S111`)
- [Optimizing Model Parameters (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) — PyTorch (`S106`)
