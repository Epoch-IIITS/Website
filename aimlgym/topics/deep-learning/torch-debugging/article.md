# Debugging Training

## Learning outcomes

After this lesson you can:

- Check a model and loss by overfitting a single small batch
- Recognise diverging, stuck and healthy loss curves
- Measure gradient norms and tame exploding gradients with clipping

## Intuition
When training fails, the code usually runs without errors — it just does not learn. A few quick
experiments narrow down the cause: can the model memorise one tiny batch? Is the loss exploding or
flat? Are the gradients huge or zero?

## Precise explanation
1. **Overfit one batch.** Train on 8–16 examples for a few hundred steps. A correct model and loss
   drive the loss close to zero. If they cannot, there is a bug (wrong labels, wrong loss, a
   detached graph) — more data will not help.
2. **Read the loss curve.**

   | Pattern | Likely cause |
   |---|---|
   | becomes `nan`/`inf` or grows | learning rate too high, exploding gradients |
   | barely moves | learning rate too low, dead ReLUs, bug that blocks gradients |
   | falls on train, rises on validation | overfitting — regularise or stop earlier |

3. **Look at gradient norms.** After `backward()`, `p.grad.norm()` for each parameter. Values of
   1e6 mean explosion; exactly 0 means no gradient reaches that layer.
4. **Clip gradients.** `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)` rescales all
   gradients together when their total norm exceeds `max_norm`, between `backward()` and `step()`.

## Worked example
A linear model with lr = 1.0 on data with large inputs diverges to `nan` within ten steps. Clipping
the gradient norm to 1.0 keeps every step bounded, and the loss falls instead.

## Common mistakes
* Tuning the architecture before checking that one batch can be overfitted.
* Clipping after `step()` (too late) or before `backward()` (nothing to clip).
* Treating a `nan` loss as a numerical curiosity rather than a learning-rate problem.

## Why this matters
These checks save hours. The training-diagnostics project idea after this step turns them into a
notebook you can reuse.

## References

- [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) — Andrej Karpathy (`S111`)
- [Optimizing Model Parameters (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) — PyTorch (`S106`)
