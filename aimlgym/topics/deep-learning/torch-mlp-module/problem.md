# DL-06 · Models with nn.Module

**Topic:** Deep Learning · **Difficulty:** beginner · **Allowed packages:** torch

**Builds on:** DL-05 PyTorch Tensors

Read the lesson first: [article.md](article.md)

## Task

1. Write a class `MLP(nn.Module)` with `__init__(self, n_in, n_hidden, n_out)` that stores
   `self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))`
   and a `forward(self, x)` returning `self.net(x)`.
2. Write `count_parameters(model)` returning the total number of elements in
   `model.parameters()` as an int.

**Example**
```python
torch.manual_seed(0)
model = MLP(4, 8, 3)
model(torch.zeros(5, 4)).shape      # torch.Size([5, 3])
count_parameters(model)             # 67
```

## Hints

<details><summary>Hint 1</summary>

Start `__init__` with `super().__init__()` so the module can register layers.

</details>

<details><summary>Hint 2</summary>

`self.net = nn.Sequential(nn.Linear(...), nn.ReLU(), nn.Linear(...))`; `forward` returns `self.net(x)`.

</details>

<details><summary>Hint 3</summary>

`sum(p.numel() for p in model.parameters())`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_output_shape` | Build self.net from Linear, ReLU, Linear and return self.net(x) in forward. |
| `test_is_module_with_registered_layers` | Store the layers in an nn.Sequential attribute named net. |
| `test_forward_matches_manual` | The layers are Linear → ReLU → Linear with no activation at the end. |
| `test_count_is_int_and_sees_new_modules` | Sum p.numel() over model.parameters() and return an int. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Assigning an `nn.Sequential` to an attribute registers all its layers, so `parameters()` finds the
two weight matrices and two bias vectors. `forward` only describes the data flow; calling the model
runs it. Counting is a sum of `numel()` over the registered tensors.

## References

- [Build the Neural Network (PyTorch tutorial)](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) — PyTorch (`S104`)
- [PyTorch Quickstart tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html) — PyTorch (`S039`)
