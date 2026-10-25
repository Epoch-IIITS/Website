# Models with nn.Module

## Learning outcomes

After this lesson you can:

- Define a model as an nn.Module subclass with layers created in __init__
- Compose layers with nn.Sequential and nn.Linear
- Count and inspect a model's registered parameters

## Intuition
A network is a set of layers plus a rule for chaining them. In PyTorch you describe both in a
class: layers are attributes created in `__init__`, and `forward` says how data flows. Because
the layers are attributes of an `nn.Module`, PyTorch finds their weights automatically — for
gradients, optimisers, saving and moving to a GPU.

## Precise explanation
```python
from torch import nn

class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()                      # always call this first
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))

    def forward(self, x):
        return self.net(x)

model = MLP(4, 8, 3)
model(torch.randn(10, 4)).shape                 # torch.Size([10, 3]) — call the model, not forward
```

* `nn.Linear(n_in, n_out)` holds `weight` with shape **(n_out, n_in)** and `bias` (n_out,), and
  computes `x @ weight.T + bias`. Weights start random (seed with `torch.manual_seed`).
* `nn.Sequential` applies its modules in order; `model.net[0]` is the first layer.
* `model.parameters()` yields every learnable tensor; `named_parameters()` adds names such as
  `net.0.weight`. A Linear layer has n_in·n_out + n_out parameters.
* The outputs of the last layer are **logits** (unnormalised scores); losses such as
  `nn.CrossEntropyLoss` apply softmax themselves.

## Worked example
`MLP(4, 8, 3)` has 4·8 + 8 = 40 parameters in the first layer and 8·3 + 3 = 27 in the second:
67 in total, in four tensors.

## What the library does inside
Calling `model(x)` runs `forward`, which is the chain of matrix products and ReLUs you wrote in
DL-07 (the optional deep dive after this step) — with PyTorch's convention that the
weight matrix is stored transposed.

## Common mistakes
* Forgetting `super().__init__()`: assigning a layer then fails.
* Storing layers in a plain Python list: they are not registered (use `nn.ModuleList` or `nn.Sequential`).
* Calling `model.forward(x)` directly, which skips hooks; call `model(x)`.
* Adding a softmax at the end and then using `CrossEntropyLoss`, which applies it again.

## Why this matters
Every model from here on — CNNs, transformers, policy networks — is an `nn.Module` built the same way.

## References

- [Build the Neural Network (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) — PyTorch (`S104`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)
