# PyTorch Tensors

## Learning outcomes

After this lesson you can:

- Create tensors from lists and NumPy arrays with a chosen dtype
- Use shapes, matrix products and broadcasting on tensors
- Move between NumPy and PyTorch and know when memory is shared

## Intuition
A PyTorch **tensor** is a NumPy array that can also remember how it was computed (for automatic
gradients) and live on a GPU. Most NumPy habits carry over: shapes, slicing, `@`, broadcasting.
The differences are the defaults and the conversions.

## Precise explanation
```python
import torch
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])   # copies the data; dtype float32
w = torch.as_tensor(np_array, dtype=torch.float32)   # converts (shares memory when it can)
x.shape, x.dtype, x.ndim                       # torch.Size([2, 2]), torch.float32, 2
x @ w, x + torch.tensor([10.0, 20.0])          # matrix product, broadcasting as in NumPy
torch.relu(x), x.sum(dim=0), x.mean()          # dim= plays the role of NumPy's axis=
x.numpy(), x.tolist(), x.sum().item()          # back to NumPy, lists, a Python number
```

| | NumPy | PyTorch |
|---|---|---|
| default float | float64 | **float32** |
| reduce along an axis | `axis=0` | `dim=0` (`axis=` also accepted) |
| integers from `[1, 2]` | int64 | int64 |
| one element to Python | `float(a[0])` | `t[0].item()` |

* Neural-network weights are float32 by default; mixing a float64 tensor with float32 weights
  raises a dtype error, so convert inputs explicitly.
* `torch.from_numpy(a)` and `t.numpy()` share memory: changing one changes the other.
  `torch.tensor(a)` always copies.

## Worked example
For x = [[1, −2]], W = [[1, 0, 2], [3, 1, −1]], b = [0.5, 0, 0]: x @ W + b = [[−4.5, −2, 4]] and
ReLU gives [[0, 0, 4]] — the same numbers as your NumPy layer in DL-04, as float32.

## Common mistakes
* Leaving data as float64 and getting "expected scalar type Float but found Double".
* Using `axis` habits with methods that only take `dim` in older code.
* Modifying a NumPy array after `torch.from_numpy` and being surprised the tensor changed.
* Calling `.item()` on a tensor with more than one element.

## Why this matters
Every PyTorch model consumes and produces tensors. The rest of this topic builds layers, losses,
gradients and training loops on top of these few operations.

## References

- [Tensors (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) — PyTorch (`S103`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)
