# DL-15 · Optimisers in torch.optim

**Topic:** Deep Learning · **Difficulty:** advanced · **Allowed packages:** torch

**Builds on:** DL-14 SGD with Momentum, DL-12 Custom Gradients and gradcheck

Read the lesson first: [article.md](article.md)

## Task

Write `minimise(name, start, lr, steps)` that minimises
`f(x, y) = (x - 3) ** 2 + 10 * (y + 1) ** 2` from `start = [x0, y0]` and returns
`{"point": [x, y], "losses": list[float]}` where `losses[i]` is f **before** step i.

* `name` selects `"sgd"` → `SGD(lr)`, `"momentum"` → `SGD(lr, momentum=0.9)`, `"adam"` →
  `Adam(lr)`, `"adamw"` → `AdamW(lr, weight_decay=0.01)`; anything else raises `ValueError`.
* Use a float32 tensor of the start point with `requires_grad=True`, and the
  `zero_grad` / `backward` / `step` cycle `steps` times.

## Hints

<details><summary>Hint 1</summary>

Map the name to a constructor with a dict of lambdas, raising ValueError for unknown names.

</details>

<details><summary>Hint 2</summary>

`p = torch.tensor(start, dtype=torch.float32, requires_grad=True)`; `opt = ...([p], ...)`.

</details>

<details><summary>Hint 3</summary>

In the loop: `opt.zero_grad()`, compute the loss from `p[0]` and `p[1]`, record `loss.item()`, `backward()`, `step()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_one_sgd_step` | Record the loss, call backward, then opt.step(); SGD moves by -lr × gradient. |
| `test_adam_first_step_is_lr_sized` | Use torch.optim.Adam(params, lr=lr) for 'adam'. |
| `test_momentum_beats_sgd` | 'momentum' is SGD with momentum=0.9. |
| `test_unknown_name` | Raise ValueError for names other than sgd, momentum, adam and adamw. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Every optimiser in `torch.optim` updates the tensors it was given when `step()` is called, using
the gradients that `backward()` left in `.grad`. Zeroing first keeps each step's gradient fresh;
recording the loss before the step gives the curve from the starting point.

## References

- [torch.optim](https://docs.pytorch.org/docs/stable/optim.html) — PyTorch (`S107`)
- [Optimizing Model Parameters (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) — PyTorch (`S106`)
