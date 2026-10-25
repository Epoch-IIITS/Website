# Autograd in PyTorch

## Learning outcomes

After this lesson you can:

- Track operations with requires_grad and compute gradients with backward()
- Read gradients from .grad and know that they accumulate
- Compare automatic gradients with a derivative worked out by hand

## Intuition
In DL-08 each `Value` remembered its parents and a local derivative, and `backward`
walked the graph in reverse. PyTorch does exactly that for tensors: mark the leaves you want
gradients for, compute a scalar loss, call `backward()`, and read `.grad`.

## Precise explanation
```python
w = torch.tensor([0.5, -1.0], requires_grad=True)     # a leaf we want gradients for
b = torch.tensor(0.0, requires_grad=True)
z = (w * x).sum() + b                                  # every operation is recorded
loss = (torch.sigmoid(z) - target) ** 2
loss.backward()                                        # fills w.grad and b.grad
w.grad, b.grad
```

* Only tensors created with `requires_grad=True` (or model parameters) get `.grad`.
* `backward()` is called on a **scalar**; gradients are **added** to `.grad`, so call it once per
  fresh graph or zero the gradients first (optimisers do this with `zero_grad()`).
* `loss.item()` gives the number; `with torch.no_grad():` turns tracking off (for evaluation and
  for updating weights by hand); `t.detach()` gives a copy without history.

For a sigmoid neuron with p = σ(w·x + b) and loss (p − t)², the chain rule gives
∂L/∂z = 2(p − t)·p(1 − p), ∂L/∂w = ∂L/∂z · x and ∂L/∂b = ∂L/∂z — the result of
DL-10, computed automatically.

## Worked example
x = [1, 2], w = [0.5, −1], b = 0, t = 1: z = −1.5, p = 0.1824, L = 0.6685,
∂L/∂z = 2(−0.8176)(0.1491) = −0.2438, so ∂L/∂w = [−0.2438, −0.4876] and ∂L/∂b = −0.2438.

## Common mistakes
* Calling `backward()` twice on the same graph, or twice in a loop without zeroing, and getting
  doubled gradients.
* Turning a tensor into a Python float in the middle of the computation, which cuts the graph.
* Expecting `.grad` on an intermediate tensor (only leaves keep it, unless you call `retain_grad()`).

## Why this matters
Training is "compute loss, backward, update" in a loop. Once gradients are automatic, any model you
can write in PyTorch can be trained.

## References

- [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — PyTorch (`S092`)
- [Tensors (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) — PyTorch (`S103`)
