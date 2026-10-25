# DL-09 · Autograd in PyTorch

**Topic:** Deep Learning · **Difficulty:** intermediate · **Allowed packages:** torch

**Builds on:** DL-08 A Tiny Autograd Engine, DL-06 Models with nn.Module

Read the lesson first: [article.md](article.md)

## Task

Write `neuron_gradients(x, w, b, target)` for one sigmoid neuron with squared-error loss
`L = (sigmoid(w · x + b) - target) ** 2`, returning `{"loss": float, "dw": list[float], "db": float}`.

* Create **new** float32 tensors for `w` and `b` with `requires_grad=True` (do not modify the
  caller's data), compute the loss with PyTorch and call `backward()`.
* Raise `ValueError` if `x` and `w` have different lengths.

**Example**
```python
neuron_gradients([1, 2], [0.5, -1], 0.0, 1.0)
# {'loss': 0.6685..., 'dw': [-0.2438..., -0.4876...], 'db': -0.2438...}
```

## Hints

<details><summary>Hint 1</summary>

`w_t = torch.tensor(w, dtype=torch.float32, requires_grad=True)`; same for b (a 0-d tensor).

</details>

<details><summary>Hint 2</summary>

`loss = (torch.sigmoid((w_t * x_t).sum() + b_t) - target) ** 2`, then `loss.backward()`.

</details>

<details><summary>Hint 3</summary>

Return `loss.item()`, `w_t.grad.tolist()` and `b_t.grad.item()`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_example` | Mark w and b with requires_grad=True, build the loss with torch.sigmoid and call loss.backward(). |
| `test_no_accumulation_between_calls` | Create new leaf tensors inside the function each call. |
| `test_types` | Return loss.item(), w.grad.tolist() and b.grad.item(). |
| `test_length_mismatch` | Raise ValueError when x and w differ in length. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`w` and `b` become leaf tensors that require gradients; every operation on them is recorded.
`backward()` applies the chain rule from the loss back to the leaves, so `.grad` holds ∂L/∂w and
∂L/∂b. New tensors are created on each call, so gradients never accumulate between calls.

## References

- [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — PyTorch (`S092`)
- [Tensors (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) — PyTorch (`S103`)
