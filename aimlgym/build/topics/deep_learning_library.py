"""Deep learning with PyTorch (library revision, Phase 2).

Library steps are followed by the NumPy implementations they replace on the required path, kept
as optional deep dives: [[mlp-forward]], [[gradient-check]], [[adam-optimizer]],
[[train-xor-mlp]], [[inverted-dropout]], [[batchnorm-forward]], [[conv1d]].
"""

PROBLEMS = [
# ---------------------------------------------------------------- torch-tensors
{
"slug": "torch-tensors", "title": "PyTorch Tensors",
"difficulty": "beginner", "prereqs": ["dense-forward"], "packages": ["numpy", "torch"],
"objectives": ["Create tensors from lists and NumPy arrays with a chosen dtype",
               "Use shapes, matrix products and broadcasting on tensors",
               "Move between NumPy and PyTorch and know when memory is shared"],
"tags": ["pytorch", "tensors", "dtype", "broadcasting"],
"sources": ["S103", "S039"], "entry": "dense_relu(x, W, b)",
"article": r'''
# PyTorch Tensors

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
ReLU gives [[0, 0, 4]] — the same numbers as your NumPy layer in [[dense-forward]], as float32.

## Common mistakes
* Leaving data as float64 and getting "expected scalar type Float but found Double".
* Using `axis` habits with methods that only take `dim` in older code.
* Modifying a NumPy array after `torch.from_numpy` and being surprised the tensor changed.
* Calling `.item()` on a tensor with more than one element.

## Why this matters
Every PyTorch model consumes and produces tensors. The rest of this topic builds layers, losses,
gradients and training loops on top of these few operations.
''',
"statement": r'''
Write `dense_relu(x, W, b)` returning the **tensor** `relu(x @ W + b)` with dtype `torch.float32`.

* `x` (shape `(batch, n_in)`), `W` (`(n_in, n_out)`) and `b` (`(n_out,)`) may be lists, NumPy
  arrays or tensors; convert each with `torch.as_tensor(..., dtype=torch.float32)`.
* Raise `ValueError` if `x` is not 2-D, or the shapes do not fit together.
* Do not modify the inputs.

**Example**
```python
dense_relu([[1, -2]], [[1, 0, 2], [3, 1, -1]], [0.5, 0, 0])   # tensor([[0., 0., 4.]])
```
''',
"starter": r'''
import torch


def dense_relu(x, W, b):
    # TODO: convert to float32 tensors, check shapes, then relu(x @ W + b)
    pass
''',
"hints": [
    "`x = torch.as_tensor(x, dtype=torch.float32)` and the same for W and b.",
    "Check `x.ndim == 2`, `x.shape[1] == W.shape[0]` and `b.shape == (W.shape[1],)`.",
    "`torch.relu(x @ W + b)` broadcasts the bias over the batch.",
],
"solution": r'''
import torch


def dense_relu(x, W, b):
    x = torch.as_tensor(x, dtype=torch.float32)
    W = torch.as_tensor(W, dtype=torch.float32)
    b = torch.as_tensor(b, dtype=torch.float32)
    if x.ndim != 2 or W.ndim != 2 or x.shape[1] != W.shape[0] or tuple(b.shape) != (W.shape[1],):
        raise ValueError("shapes do not fit: need x (batch, n_in), W (n_in, n_out), b (n_out,)")
    return torch.relu(x @ W + b)
''',
"explanation": r'''
`torch.as_tensor` converts lists and arrays to float32 tensors (without copying when no conversion
is needed). The shape checks give a clear error before the matrix product; the bias broadcasts
over the batch exactly as it does in NumPy, and ReLU clips negatives to zero.
''',
"tests": r'''
import numpy as np
import torch


class TestDenseRelu(unittest.TestCase):
    def test_example(self):
        out = S.dense_relu([[1, -2]], [[1, 0, 2], [3, 1, -1]], [0.5, 0, 0])
        self.assertIsInstance(out, torch.Tensor)
        self.assertEqual(out.tolist(), [[0.0, 0.0, 4.0]])

    def test_float32_from_float64(self):
        out = S.dense_relu(np.ones((2, 3)), np.ones((3, 4)), np.zeros(4))
        self.assertEqual(out.dtype, torch.float32)
        self.assertEqual(tuple(out.shape), (2, 4))

    def test_matches_numpy(self):
        rng = np.random.default_rng(0)
        x, W, b = rng.normal(size=(5, 3)), rng.normal(size=(3, 2)), rng.normal(size=2)
        expected = np.maximum(x @ W + b, 0)
        self.assertTrue(np.allclose(S.dense_relu(x, W, b).numpy(), expected, atol=1e-5))

    def test_accepts_tensors(self):
        x = torch.tensor([[1.0, 2.0]]); W = torch.eye(2); b = torch.tensor([-1.5, 0.0])
        self.assertEqual(S.dense_relu(x, W, b).tolist(), [[0.0, 2.0]])

    def test_inputs_unchanged(self):
        x = np.array([[-1.0, 2.0]]); W = np.eye(2); b = np.zeros(2)
        S.dense_relu(x, W, b)
        self.assertEqual(x.tolist(), [[-1.0, 2.0]])

    def test_shape_errors(self):
        for args in [([1, 2], [[1], [1]], [0]), ([[1, 2]], [[1, 2, 3]], [0, 0, 0]), ([[1, 2]], [[1], [1]], [0, 0])]:
            with self.assertRaises(ValueError):
                S.dense_relu(*args)
''',
"feedback": [
    ("test_example", "Compute torch.relu(x @ W + b) and return the tensor itself."),
    ("test_float32_from_float64", "Convert every input with dtype=torch.float32."),
    ("test_inputs_unchanged", "Do not use in-place operations on the inputs."),
    ("test_shape_errors", "Check that x is 2-D and that W and b have matching sizes."),
],
},
# ---------------------------------------------------------------- torch-mlp-module
{
"slug": "torch-mlp-module", "title": "Models with nn.Module",
"difficulty": "beginner", "prereqs": ["torch-tensors"], "packages": ["torch"],
"objectives": ["Define a model as an nn.Module subclass with layers created in __init__",
               "Compose layers with nn.Sequential and nn.Linear",
               "Count and inspect a model's registered parameters"],
"tags": ["pytorch", "nn-module", "mlp", "parameters"],
"sources": ["S104", "S039"], "entry": "class MLP(nn.Module); count_parameters(model)",
"article": r'''
# Models with nn.Module

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
[[mlp-forward]] (the optional deep dive after this step) — with PyTorch's convention that the
weight matrix is stored transposed.

## Common mistakes
* Forgetting `super().__init__()`: assigning a layer then fails.
* Storing layers in a plain Python list: they are not registered (use `nn.ModuleList` or `nn.Sequential`).
* Calling `model.forward(x)` directly, which skips hooks; call `model(x)`.
* Adding a softmax at the end and then using `CrossEntropyLoss`, which applies it again.

## Why this matters
Every model from here on — CNNs, transformers, policy networks — is an `nn.Module` built the same way.
''',
"statement": r'''
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
''',
"starter": r'''
import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        # TODO: call super().__init__() and build self.net
        pass

    def forward(self, x):
        # TODO
        pass


def count_parameters(model):
    # TODO
    pass
''',
"hints": [
    "Start `__init__` with `super().__init__()` so the module can register layers.",
    "`self.net = nn.Sequential(nn.Linear(...), nn.ReLU(), nn.Linear(...))`; `forward` returns `self.net(x)`.",
    "`sum(p.numel() for p in model.parameters())`.",
],
"solution": r'''
import torch
from torch import nn


class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))

    def forward(self, x):
        return self.net(x)


def count_parameters(model):
    return int(sum(p.numel() for p in model.parameters()))
''',
"explanation": r'''
Assigning an `nn.Sequential` to an attribute registers all its layers, so `parameters()` finds the
two weight matrices and two bias vectors. `forward` only describes the data flow; calling the model
runs it. Counting is a sum of `numel()` over the registered tensors.
''',
"tests": r'''
import torch
from torch import nn


class TestMLPModule(unittest.TestCase):
    def test_output_shape(self):
        torch.manual_seed(0)
        model = S.MLP(4, 8, 3)
        self.assertEqual(tuple(model(torch.zeros(5, 4)).shape), (5, 3))

    def test_parameter_count(self):
        self.assertEqual(S.count_parameters(S.MLP(4, 8, 3)), 67)
        self.assertEqual(S.count_parameters(S.MLP(10, 1, 1)), 13)

    def test_is_module_with_registered_layers(self):
        model = S.MLP(2, 3, 1)
        self.assertIsInstance(model, nn.Module)
        names = [name for name, _ in model.named_parameters()]
        self.assertEqual(names, ["net.0.weight", "net.0.bias", "net.2.weight", "net.2.bias"])

    def test_forward_matches_manual(self):
        torch.manual_seed(1)
        model = S.MLP(3, 4, 2)
        x = torch.randn(6, 3)
        l1, l2 = model.net[0], model.net[2]
        manual = torch.relu(x @ l1.weight.T + l1.bias) @ l2.weight.T + l2.bias
        self.assertTrue(torch.allclose(model(x), manual, atol=1e-6))

    def test_seeded_initialisation(self):
        torch.manual_seed(5); a = S.MLP(3, 4, 2)
        torch.manual_seed(5); b = S.MLP(3, 4, 2)
        for pa, pb in zip(a.parameters(), b.parameters()):
            self.assertTrue(torch.equal(pa, pb))

    def test_count_is_int_and_sees_new_modules(self):
        model = S.MLP(2, 2, 2)
        self.assertIs(type(S.count_parameters(model)), int)
        self.assertEqual(S.count_parameters(nn.Linear(5, 2)), 12)
''',
"feedback": [
    ("test_output_shape", "Build self.net from Linear, ReLU, Linear and return self.net(x) in forward."),
    ("test_is_module_with_registered_layers", "Store the layers in an nn.Sequential attribute named net."),
    ("test_forward_matches_manual", "The layers are Linear → ReLU → Linear with no activation at the end."),
    ("test_count_is_int_and_sees_new_modules", "Sum p.numel() over model.parameters() and return an int."),
],
},
# ---------------------------------------------------------------- torch-autograd
{
"slug": "torch-autograd", "title": "Autograd in PyTorch",
"difficulty": "intermediate", "prereqs": ["scalar-autograd", "torch-mlp-module"], "packages": ["torch"],
"objectives": ["Track operations with requires_grad and compute gradients with backward()",
               "Read gradients from .grad and know that they accumulate",
               "Compare automatic gradients with a derivative worked out by hand"],
"tags": ["pytorch", "autograd", "backpropagation", "gradients"],
"sources": ["S092", "S103"], "entry": "neuron_gradients(x, w, b, target)",
"article": r'''
# Autograd in PyTorch

## Intuition
In [[scalar-autograd]] each `Value` remembered its parents and a local derivative, and `backward`
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
[[neuron-backprop]], computed automatically.

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
''',
"statement": r'''
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
''',
"starter": r'''
import torch


def neuron_gradients(x, w, b, target):
    # TODO: leaf tensors with requires_grad, forward, backward, read .grad
    pass
''',
"hints": [
    "`w_t = torch.tensor(w, dtype=torch.float32, requires_grad=True)`; same for b (a 0-d tensor).",
    "`loss = (torch.sigmoid((w_t * x_t).sum() + b_t) - target) ** 2`, then `loss.backward()`.",
    "Return `loss.item()`, `w_t.grad.tolist()` and `b_t.grad.item()`.",
],
"solution": r'''
import torch


def neuron_gradients(x, w, b, target):
    if len(x) != len(w):
        raise ValueError("x and w must have the same length")
    x_t = torch.tensor(x, dtype=torch.float32)
    w_t = torch.tensor(w, dtype=torch.float32, requires_grad=True)
    b_t = torch.tensor(float(b), requires_grad=True)
    loss = (torch.sigmoid((w_t * x_t).sum() + b_t) - target) ** 2
    loss.backward()
    return {"loss": loss.item(), "dw": w_t.grad.tolist(), "db": b_t.grad.item()}
''',
"explanation": r'''
`w` and `b` become leaf tensors that require gradients; every operation on them is recorded.
`backward()` applies the chain rule from the loss back to the leaves, so `.grad` holds ∂L/∂w and
∂L/∂b. New tensors are created on each call, so gradients never accumulate between calls.
''',
"tests": r'''
import torch


def by_hand(x, w, b, t):
    z = sum(xi * wi for xi, wi in zip(x, w)) + b
    p = 1 / (1 + math.exp(-z))
    dz = 2 * (p - t) * p * (1 - p)
    return (p - t) ** 2, [dz * xi for xi in x], dz


class TestNeuronGradients(unittest.TestCase):
    def test_example(self):
        r = S.neuron_gradients([1, 2], [0.5, -1], 0.0, 1.0)
        loss, dw, db = by_hand([1, 2], [0.5, -1], 0.0, 1.0)
        self.assertAlmostEqual(r["loss"], loss, places=5)
        for a, e in zip(r["dw"], dw):
            self.assertAlmostEqual(a, e, places=5)
        self.assertAlmostEqual(r["db"], db, places=5)

    def test_other_point(self):
        r = S.neuron_gradients([0.3, -1.2, 2.0], [1.0, 0.4, -0.7], 0.25, 0.0)
        loss, dw, db = by_hand([0.3, -1.2, 2.0], [1.0, 0.4, -0.7], 0.25, 0.0)
        self.assertAlmostEqual(r["loss"], loss, places=5)
        self.assertTrue(all(abs(a - e) < 1e-5 for a, e in zip(r["dw"], dw)))

    def test_no_accumulation_between_calls(self):
        a = S.neuron_gradients([1, 2], [0.5, -1], 0.0, 1.0)
        b = S.neuron_gradients([1, 2], [0.5, -1], 0.0, 1.0)
        self.assertEqual(a, b)

    def test_caller_tensor_untouched(self):
        w = torch.tensor([0.5, -1.0], requires_grad=True)
        S.neuron_gradients([1, 2], w.tolist(), 0.0, 1.0)
        self.assertIsNone(w.grad)

    def test_types(self):
        r = S.neuron_gradients([1.0], [2.0], 1.0, 0.5)
        self.assertIs(type(r["loss"]), float)
        self.assertIs(type(r["db"]), float)
        self.assertTrue(all(type(v) is float for v in r["dw"]))

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.neuron_gradients([1, 2, 3], [1, 2], 0.0, 1.0)
''',
"feedback": [
    ("test_example", "Mark w and b with requires_grad=True, build the loss with torch.sigmoid and call loss.backward()."),
    ("test_no_accumulation_between_calls", "Create new leaf tensors inside the function each call."),
    ("test_types", "Return loss.item(), w.grad.tolist() and b.grad.item()."),
    ("test_length_mismatch", "Raise ValueError when x and w differ in length."),
],
},
# ---------------------------------------------------------------- torch-gradcheck
{
"slug": "torch-gradcheck", "title": "Custom Gradients and gradcheck",
"difficulty": "intermediate", "prereqs": ["dense-backward", "torch-autograd"], "packages": ["torch"],
"objectives": ["Write a torch.autograd.Function with its own forward and backward",
               "Verify a backward pass numerically with torch.autograd.gradcheck",
               "Use float64 inputs for reliable finite-difference checks"],
"tags": ["pytorch", "autograd", "gradient-checking", "custom-function"],
"sources": ["S110", "S092"], "entry": "class Softplus(torch.autograd.Function); passes_gradcheck(fn, shape, seed=0)",
"article": r'''
# Custom Gradients and gradcheck

## Intuition
Autograd knows the derivatives of PyTorch's own operations. Sometimes you write an operation
yourself — for speed, numerical stability or a research idea — and then you must supply its
backward pass. A wrong backward does not crash; it silently trains badly. `gradcheck` catches it by
comparing your gradients with finite differences, as you did in [[gradient-check]].

## Precise explanation
```python
class Softplus(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)          # keep what backward needs
        return torch.logaddexp(x, torch.zeros_like(x))     # log(1 + e^x), stable

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        return grad_output * torch.sigmoid(x)               # chain rule: upstream × local

y = Softplus.apply(x)                     # use .apply, never call forward directly
```

* `backward` receives the gradient of the loss with respect to the output and returns the
  gradient with respect to each input.
* `torch.autograd.gradcheck(fn, (x,))` perturbs each input element by a small ε, compares the
  numerical slope with your backward, and returns `True` or raises; with
  `raise_exception=False` it returns `False` instead.
* Use **float64** inputs with `requires_grad=True`: in float32 the finite differences are too noisy.

## Worked example
softplus′(x) = eˣ/(1 + eˣ) = σ(x). At x = 0 the value is log 2 = 0.693 and the derivative 0.5. A
backward that returned `grad_output * x` would pass at no point except by luck; gradcheck reports it.

## What the library does inside
For each input element gradcheck evaluates (f(x + ε) − f(x − ε))/2ε, builds the numerical Jacobian,
and compares it with the Jacobian your backward implies — the [[gradient-check]] deep dive, for
every element and output at once.

## Common mistakes
* Calling `Softplus.forward(...)` instead of `Softplus.apply(...)`, so no graph is recorded.
* Forgetting to multiply by `grad_output`.
* Running gradcheck in float32 and chasing false failures.
* Computing `log(1 + exp(x))` directly, which overflows for x around 100.

## Why this matters
Custom operations appear in fused kernels, new activation functions and differentiable
simulators; gradcheck is how their authors trust them.
''',
"statement": r'''
1. Write `class Softplus(torch.autograd.Function)` with static `forward(ctx, x)` returning
   softplus(x) = log(1 + eˣ) computed stably with `torch.logaddexp(x, torch.zeros_like(x))`, and
   `backward(ctx, grad_output)` returning `grad_output * sigmoid(x)`.
2. Write `softplus(x)` returning `Softplus.apply(x)`.
3. Write `passes_gradcheck(fn, shape, seed=0)` that makes a float64 input of that shape with
   `torch.randn` from `torch.Generator().manual_seed(seed)`, `requires_grad=True`, and returns
   `torch.autograd.gradcheck(fn, (x,), raise_exception=False)`.
''',
"starter": r'''
import torch


class Softplus(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        # TODO: save x, return log(1 + e^x) stably
        pass

    @staticmethod
    def backward(ctx, grad_output):
        # TODO
        pass


def softplus(x):
    # TODO
    pass


def passes_gradcheck(fn, shape, seed=0):
    # TODO
    pass
''',
"hints": [
    "In forward: `ctx.save_for_backward(x)`; in backward: `(x,) = ctx.saved_tensors`.",
    "The derivative of softplus is the sigmoid, so return `grad_output * torch.sigmoid(x)`.",
    "`x = torch.randn(shape, generator=g, dtype=torch.float64, requires_grad=True)`.",
],
"solution": r'''
import torch


class Softplus(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return torch.logaddexp(x, torch.zeros_like(x))

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        return grad_output * torch.sigmoid(x)


def softplus(x):
    return Softplus.apply(x)


def passes_gradcheck(fn, shape, seed=0):
    g = torch.Generator().manual_seed(seed)
    x = torch.randn(shape, generator=g, dtype=torch.float64, requires_grad=True)
    return bool(torch.autograd.gradcheck(fn, (x,), raise_exception=False))
''',
"explanation": r'''
The forward pass saves its input and uses `logaddexp`, which never overflows. The backward pass
multiplies the upstream gradient by the local derivative σ(x). gradcheck compares that backward
with central differences on a float64 input and reports whether they agree.
''',
"tests": r'''
import torch
import torch.nn.functional as F


class WrongSquare(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        ctx.save_for_backward(x)
        return x * x

    @staticmethod
    def backward(ctx, grad_output):
        (x,) = ctx.saved_tensors
        return grad_output * x          # should be 2x


class TestSoftplus(unittest.TestCase):
    def test_forward_matches_library(self):
        x = torch.linspace(-5, 5, 11)
        self.assertTrue(torch.allclose(S.softplus(x), F.softplus(x), atol=1e-6))

    def test_backward_is_sigmoid(self):
        x = torch.tensor([-2.0, 0.0, 3.0], requires_grad=True)
        S.softplus(x).sum().backward()
        self.assertTrue(torch.allclose(x.grad, torch.sigmoid(x.detach()), atol=1e-6))

    def test_passes_gradcheck(self):
        self.assertTrue(S.passes_gradcheck(S.softplus, (4, 3)))

    def test_wrong_backward_fails(self):
        self.assertFalse(S.passes_gradcheck(WrongSquare.apply, (5,)))

    def test_stable_for_large_inputs(self):
        x = torch.tensor([100.0, -100.0], dtype=torch.float64)
        out = S.softplus(x)
        self.assertTrue(torch.isfinite(out).all())
        self.assertAlmostEqual(out[0].item(), 100.0, places=6)
        self.assertAlmostEqual(out[1].item(), 0.0, places=6)

    def test_uses_custom_function(self):
        x = torch.tensor([0.5], requires_grad=True)
        self.assertIn("Softplus", type(S.softplus(x).grad_fn).__name__)
        self.assertIsInstance(S.passes_gradcheck(torch.sin, (2,)), bool)
''',
"feedback": [
    ("test_backward_is_sigmoid", "backward must return grad_output * torch.sigmoid(x)."),
    ("test_wrong_backward_fails", "Pass raise_exception=False so gradcheck returns False instead of raising."),
    ("test_stable_for_large_inputs", "Use torch.logaddexp(x, torch.zeros_like(x)) instead of log(1 + exp(x))."),
    ("test_uses_custom_function", "softplus should call Softplus.apply(x)."),
],
},
# ---------------------------------------------------------------- torch-optimizers
{
"slug": "torch-optimizers", "title": "Optimisers in torch.optim",
"difficulty": "advanced", "prereqs": ["sgd-momentum", "torch-gradcheck"], "packages": ["torch"],
"objectives": ["Run the zero_grad / backward / step cycle with torch.optim",
               "Compare SGD, SGD with momentum, Adam and AdamW on the same problem",
               "Explain what weight decay does and how AdamW applies it"],
"tags": ["pytorch", "optimisers", "adam", "sgd", "weight-decay"],
"sources": ["S107", "S106"], "entry": "minimise(name, start, lr, steps)",
"article": r'''
# Optimisers in torch.optim

## Intuition
An optimiser turns gradients into updates. Plain SGD steps straight downhill; momentum
([[sgd-momentum]]) keeps a running velocity; Adam scales each parameter's step by a running
estimate of its gradient size, so steep and flat directions both make progress. In PyTorch they all
share one three-line loop.

## Precise explanation
```python
params = torch.tensor([0.0, 0.0], requires_grad=True)
opt = torch.optim.Adam([params], lr=0.1)
for _ in range(steps):
    opt.zero_grad()           # clear old gradients (they accumulate)
    loss = f(params)
    loss.backward()           # fill params.grad
    opt.step()                # update params in place
```

| Optimiser | Update (per parameter) |
|---|---|
| `SGD(lr)` | θ ← θ − lr·g |
| `SGD(lr, momentum=0.9)` | v ← 0.9v + g; θ ← θ − lr·v |
| `Adam(lr)` | m, v running means of g and g², bias-corrected; θ ← θ − lr·m̂/(√v̂ + ε) |
| `AdamW(lr, weight_decay)` | Adam, plus θ ← θ − lr·wd·θ applied directly to the weights |

* The optimiser receives the tensors to update (`model.parameters()` for a model).
* **Weight decay** shrinks weights a little every step, a form of the regularisation in
  [[sklearn-grid-search]]. In Adam it interacts with the adaptive scaling; AdamW decouples it,
  which is why AdamW is the usual default for transformers.

## Worked example
For f(x, y) = (x − 3)² + 10(y + 1)² from (0, 0): SGD with lr 0.01 crawls along x because the
y-direction forces a small step; Adam with lr 0.1 moves both coordinates at similar speed and reaches
(3, −1) within about 200 steps.

## What the library does inside
`Adam.step` keeps the two running averages per parameter and applies the bias correction you
implement in [[adam-optimizer]], the optional deep dive after this step.

## Common mistakes
* Forgetting `zero_grad()`, so gradients from every previous step are added together.
* Creating the optimiser before the model's parameters exist, or for a copy of them.
* Using the same learning rate for SGD and Adam: good values differ by orders of magnitude.

## Why this matters
The training loop in [[torch-training-loop]] is this loop with a model and data; changing the
optimiser is a one-line experiment.
''',
"statement": r'''
Write `minimise(name, start, lr, steps)` that minimises
`f(x, y) = (x - 3) ** 2 + 10 * (y + 1) ** 2` from `start = [x0, y0]` and returns
`{"point": [x, y], "losses": list[float]}` where `losses[i]` is f **before** step i.

* `name` selects `"sgd"` → `SGD(lr)`, `"momentum"` → `SGD(lr, momentum=0.9)`, `"adam"` →
  `Adam(lr)`, `"adamw"` → `AdamW(lr, weight_decay=0.01)`; anything else raises `ValueError`.
* Use a float32 tensor of the start point with `requires_grad=True`, and the
  `zero_grad` / `backward` / `step` cycle `steps` times.
''',
"starter": r'''
import torch


def minimise(name, start, lr, steps):
    # TODO
    pass
''',
"hints": [
    "Map the name to a constructor with a dict of lambdas, raising ValueError for unknown names.",
    "`p = torch.tensor(start, dtype=torch.float32, requires_grad=True)`; `opt = ...([p], ...)`.",
    "In the loop: `opt.zero_grad()`, compute the loss from `p[0]` and `p[1]`, record `loss.item()`, `backward()`, `step()`.",
],
"solution": r'''
import torch


def minimise(name, start, lr, steps):
    makers = {
        "sgd": lambda params: torch.optim.SGD(params, lr=lr),
        "momentum": lambda params: torch.optim.SGD(params, lr=lr, momentum=0.9),
        "adam": lambda params: torch.optim.Adam(params, lr=lr),
        "adamw": lambda params: torch.optim.AdamW(params, lr=lr, weight_decay=0.01),
    }
    if name not in makers:
        raise ValueError("unknown optimiser " + str(name))
    p = torch.tensor(start, dtype=torch.float32, requires_grad=True)
    opt = makers[name]([p])
    losses = []
    for _ in range(steps):
        opt.zero_grad()
        loss = (p[0] - 3) ** 2 + 10 * (p[1] + 1) ** 2
        losses.append(loss.item())
        loss.backward()
        opt.step()
    return {"point": p.detach().tolist(), "losses": losses}
''',
"explanation": r'''
Every optimiser in `torch.optim` updates the tensors it was given when `step()` is called, using
the gradients that `backward()` left in `.grad`. Zeroing first keeps each step's gradient fresh;
recording the loss before the step gives the curve from the starting point.
''',
"tests": r'''
import torch


class TestMinimise(unittest.TestCase):
    def test_one_sgd_step(self):
        r = S.minimise("sgd", [0.0, 0.0], 0.01, 1)
        # gradient at (0, 0) is (-6, 20)
        self.assertAlmostEqual(r["point"][0], 0.06, places=6)
        self.assertAlmostEqual(r["point"][1], -0.2, places=6)
        self.assertAlmostEqual(r["losses"][0], 19.0, places=5)

    def test_adam_first_step_is_lr_sized(self):
        r = S.minimise("adam", [0.0, 0.0], 0.1, 1)
        self.assertAlmostEqual(r["point"][0], 0.1, places=5)
        self.assertAlmostEqual(r["point"][1], -0.1, places=5)

    def test_adam_converges(self):
        r = S.minimise("adam", [0.0, 0.0], 0.1, 300)
        self.assertAlmostEqual(r["point"][0], 3.0, delta=0.05)
        self.assertAlmostEqual(r["point"][1], -1.0, delta=0.05)

    def test_momentum_beats_sgd(self):
        sgd = S.minimise("sgd", [0.0, 0.0], 0.005, 100)
        mom = S.minimise("momentum", [0.0, 0.0], 0.005, 100)
        self.assertLess(mom["losses"][-1], sgd["losses"][-1])

    def test_losses_recorded_and_fall(self):
        r = S.minimise("adamw", [0.0, 0.0], 0.1, 50)
        self.assertEqual(len(r["losses"]), 50)
        self.assertLess(r["losses"][-1], r["losses"][0] / 10)
        self.assertTrue(all(type(v) is float for v in r["losses"]))

    def test_unknown_name(self):
        with self.assertRaises(ValueError):
            S.minimise("lbfgs-ish", [0.0, 0.0], 0.1, 1)
''',
"feedback": [
    ("test_one_sgd_step", "Record the loss, call backward, then opt.step(); SGD moves by -lr × gradient."),
    ("test_adam_first_step_is_lr_sized", "Use torch.optim.Adam(params, lr=lr) for 'adam'."),
    ("test_momentum_beats_sgd", "'momentum' is SGD with momentum=0.9."),
    ("test_unknown_name", "Raise ValueError for names other than sgd, momentum, adam and adamw."),
],
},
# ---------------------------------------------------------------- torch-datasets
{
"slug": "torch-datasets", "title": "Datasets and DataLoader",
"difficulty": "advanced", "prereqs": ["torch-optimizers"], "packages": ["numpy", "torch"],
"objectives": ["Write a Dataset with __len__ and __getitem__",
               "Batch and shuffle data with DataLoader",
               "Make shuffling reproducible with a seeded torch.Generator"],
"tags": ["pytorch", "dataset", "dataloader", "mini-batches", "reproducibility"],
"sources": ["S105", "S109"], "entry": "class ArrayDataset(Dataset); make_loader(X, y, batch_size, shuffle=True, seed=0)",
"article": r'''
# Datasets and DataLoader

## Intuition
Training uses **mini-batches**: a few dozen examples at a time, in a new random order every epoch.
PyTorch splits the job in two. A `Dataset` knows how many examples there are and how to fetch
one; a `DataLoader` decides the order, groups examples into batches and stacks them into tensors.

## Precise explanation
```python
from torch.utils.data import DataLoader, Dataset

class ArrayDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.as_tensor(X, dtype=torch.float32)
        self.y = torch.as_tensor(y, dtype=torch.long)
    def __len__(self):
        return len(self.y)
    def __getitem__(self, i):
        return self.X[i], self.y[i]

loader = DataLoader(ArrayDataset(X, y), batch_size=32, shuffle=True,
                    generator=torch.Generator().manual_seed(0))
for xb, yb in loader:        # xb: (32, n_features) float32, yb: (32,) int64
    ...
```

* `__getitem__` returns one example; the loader's default **collate** function stacks them.
* With `shuffle=True` the order changes every epoch; the generator makes the sequence of orders
  reproducible. `drop_last=True` drops an incomplete final batch.
* Class labels for `CrossEntropyLoss` must be integer (`torch.long`) class indices.
* For in-memory tensors, `torch.utils.data.TensorDataset(X, y)` does the same as the class above.

## Worked example
10 examples with `batch_size=4` give batches of 4, 4 and 2. With `shuffle=False` the first batch
holds examples 0–3; with shuffling and seed 0 every example still appears exactly once per epoch.

## Common mistakes
* Labels as float32, which CrossEntropyLoss rejects.
* Returning NumPy arrays from `__getitem__` with mixed dtypes.
* Shuffling the test loader (harmless but confusing) or not shuffling the training loader.
* Expecting identical shuffles across runs without passing a generator.

## Why this matters
Real datasets do not fit in one batch; images and text are read lazily in `__getitem__`. The
training loop in the next step iterates over a DataLoader.
''',
"statement": r'''
1. Write `class ArrayDataset(Dataset)` storing `X` as float32 and `y` as `torch.long` tensors,
   with `__len__` and `__getitem__(i)` returning `(X[i], y[i])`. Raise `ValueError` in
   `__init__` if the lengths differ.
2. Write `make_loader(X, y, batch_size, shuffle=True, seed=0)` returning a `DataLoader` over an
   `ArrayDataset`, shuffled with `generator=torch.Generator().manual_seed(seed)` when `shuffle`
   is true.
''',
"starter": r'''
import torch
from torch.utils.data import DataLoader, Dataset


class ArrayDataset(Dataset):
    def __init__(self, X, y):
        # TODO
        pass

    def __len__(self):
        # TODO
        pass

    def __getitem__(self, i):
        # TODO
        pass


def make_loader(X, y, batch_size, shuffle=True, seed=0):
    # TODO
    pass
''',
"hints": [
    "Convert in `__init__`: `torch.as_tensor(X, dtype=torch.float32)` and `torch.as_tensor(y, dtype=torch.long)`.",
    "`__len__` returns `len(self.y)`; `__getitem__` returns `self.X[i], self.y[i]`.",
    "`DataLoader(dataset, batch_size=..., shuffle=shuffle, generator=torch.Generator().manual_seed(seed))`.",
],
"solution": r'''
import torch
from torch.utils.data import DataLoader, Dataset


class ArrayDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.as_tensor(X, dtype=torch.float32)
        self.y = torch.as_tensor(y, dtype=torch.long)
        if len(self.X) != len(self.y):
            raise ValueError("X and y must have the same length")

    def __len__(self):
        return len(self.y)

    def __getitem__(self, i):
        return self.X[i], self.y[i]


def make_loader(X, y, batch_size, shuffle=True, seed=0):
    generator = torch.Generator().manual_seed(seed)
    return DataLoader(ArrayDataset(X, y), batch_size=batch_size, shuffle=shuffle, generator=generator)
''',
"explanation": r'''
The dataset converts once to the dtypes a classifier needs and fetches one row at a time; the
loader groups rows into stacked batches and, with a seeded generator, produces the same sequence
of shuffled orders on every run.
''',
"tests": r'''
import numpy as np
import torch


class TestDataLoading(unittest.TestCase):
    def test_dataset_items(self):
        ds = S.ArrayDataset(np.arange(6).reshape(3, 2), [0, 1, 0])
        self.assertEqual(len(ds), 3)
        x, y = ds[1]
        self.assertEqual((x.dtype, y.dtype), (torch.float32, torch.long))
        self.assertEqual((x.tolist(), y.item()), ([2.0, 3.0], 1))

    def test_batch_sizes(self):
        loader = S.make_loader(np.zeros((10, 3)), np.zeros(10), batch_size=4, shuffle=False)
        self.assertEqual([len(yb) for _, yb in loader], [4, 4, 2])

    def test_unshuffled_order(self):
        X = np.arange(10).reshape(5, 2); y = np.arange(5)
        first_x, first_y = next(iter(S.make_loader(X, y, batch_size=2, shuffle=False)))
        self.assertEqual(first_y.tolist(), [0, 1])
        self.assertEqual(first_x.tolist(), [[0.0, 1.0], [2.0, 3.0]])

    def test_shuffle_covers_everything_once(self):
        y = np.arange(23)
        seen = [v for _, yb in S.make_loader(np.zeros((23, 1)), y, batch_size=5, seed=1) for v in yb.tolist()]
        self.assertEqual(sorted(seen), list(range(23)))
        self.assertNotEqual(seen, list(range(23)))

    def test_seeded_shuffle_reproducible(self):
        y = np.arange(20)
        a = [yb.tolist() for _, yb in S.make_loader(np.zeros((20, 1)), y, batch_size=5, seed=3)]
        b = [yb.tolist() for _, yb in S.make_loader(np.zeros((20, 1)), y, batch_size=5, seed=3)]
        c = [yb.tolist() for _, yb in S.make_loader(np.zeros((20, 1)), y, batch_size=5, seed=4)]
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.ArrayDataset(np.zeros((3, 2)), [0, 1])
''',
"feedback": [
    ("test_dataset_items", "Store X as float32 and y as torch.long; __getitem__ returns (X[i], y[i])."),
    ("test_batch_sizes", "Pass batch_size to the DataLoader and keep the incomplete last batch."),
    ("test_seeded_shuffle_reproducible", "Pass generator=torch.Generator().manual_seed(seed)."),
    ("test_length_mismatch", "Raise ValueError in __init__ when the lengths differ."),
],
},
# ---------------------------------------------------------------- torch-training-loop
{
"slug": "torch-training-loop", "title": "A Full Training Loop",
"difficulty": "advanced", "prereqs": ["torch-datasets"], "packages": ["numpy", "torch"],
"objectives": ["Train a classifier with a DataLoader, CrossEntropyLoss and an optimiser",
               "Switch between train() and eval() and evaluate under torch.no_grad()",
               "Record the loss per epoch and make training reproducible with a seed"],
"tags": ["pytorch", "training-loop", "cross-entropy", "classification"],
"sources": ["S106", "S039"], "entry": "train_classifier(X, y, n_hidden=16, epochs=100, lr=0.05, batch_size=16, seed=0)",
"article": r'''
# A Full Training Loop

## Intuition
Everything comes together: a model, a loss, an optimiser and batches of data. One **epoch** passes
over the whole training set once; after each batch the model's weights move a little. Watching the
average loss per epoch tells you whether learning is working.

## Precise explanation
```python
torch.manual_seed(seed)                                   # initial weights
model = MLP(n_in, n_hidden, n_classes)
loss_fn = nn.CrossEntropyLoss()                           # softmax + negative log-likelihood
opt = torch.optim.Adam(model.parameters(), lr=lr)
for epoch in range(epochs):
    model.train()
    total = 0.0
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)                     # logits (B, C), labels (B,) int64
        loss.backward()
        opt.step()
        total += loss.item() * len(yb)
    history.append(total / len(dataset))                  # mean loss over the epoch

model.eval()
with torch.no_grad():
    predictions = model(X).argmax(dim=1)
```

* `nn.CrossEntropyLoss` takes raw logits and integer class labels; it is the softmax +
  [[cross-entropy]] you wrote earlier, computed stably.
* `model.train()` / `model.eval()` switch layers such as dropout and batch normalisation
  (next steps) between their training and inference behaviour.
* `torch.no_grad()` skips graph building during evaluation: faster, and no accidental gradients.
* Weight the batch loss by batch size when averaging, so a short last batch counts correctly.

## Worked example
XOR (four points, two classes) cannot be separated by a line. An MLP with 16 hidden units trained
with Adam (lr 0.05) for 100 epochs drives the loss from about 0.7 to below 0.05 and classifies all
four points correctly.

## What the library does inside
The loop is the one you write by hand with NumPy in [[train-xor-mlp]], the optional deep dive
after this step — forward pass, loss, backward pass, update — with autograd computing the gradients.

## Common mistakes
* Passing softmax probabilities to `CrossEntropyLoss` (it expects logits).
* Forgetting `model.eval()` before evaluating a model with dropout or batch normalisation.
* Averaging batch losses without weighting by batch size.
* Seeding after the model is created, so the initial weights are not reproducible.

## Why this matters
This loop, with a different model and dataset, trains image classifiers, language models and
policies. The digit-recogniser project idea after this step is the same loop on real images.
''',
"statement": r'''
Write `train_classifier(X, y, n_hidden=16, epochs=100, lr=0.05, batch_size=16, seed=0)` returning
`(model, history)` where `history` lists the mean training loss of each epoch.

* Call `torch.manual_seed(seed)` first, then build
  `nn.Sequential(nn.Linear(n_features, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_classes))`
  with `n_classes = max(y) + 1`.
* Batches come from `DataLoader(TensorDataset(X_float32, y_long), batch_size, shuffle=True,
  generator=torch.Generator().manual_seed(seed))`; use `nn.CrossEntropyLoss` and `torch.optim.Adam`.
* Each epoch's loss is the batch losses weighted by batch size, divided by the number of examples.
* Leave the model in `eval()` mode.

Also write `predict(model, X)` returning a list of predicted class indices, computed with
`model.eval()` and `torch.no_grad()`.
''',
"starter": r'''
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def train_classifier(X, y, n_hidden=16, epochs=100, lr=0.05, batch_size=16, seed=0):
    # TODO
    pass


def predict(model, X):
    # TODO
    pass
''',
"hints": [
    "Convert once: `X = torch.as_tensor(X, dtype=torch.float32)`, `y = torch.as_tensor(y, dtype=torch.long)`; seed before building the model.",
    "Per batch: `opt.zero_grad()`, `loss = loss_fn(model(xb), yb)`, `loss.backward()`, `opt.step()`, `total += loss.item() * len(yb)`.",
    "`predict`: `model.eval()`, then `with torch.no_grad(): return model(X).argmax(dim=1).tolist()`.",
],
"solution": r'''
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset


def train_classifier(X, y, n_hidden=16, epochs=100, lr=0.05, batch_size=16, seed=0):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.long)
    torch.manual_seed(seed)
    model = nn.Sequential(nn.Linear(X.shape[1], n_hidden), nn.ReLU(), nn.Linear(n_hidden, int(y.max()) + 1))
    loader = DataLoader(TensorDataset(X, y), batch_size=batch_size, shuffle=True,
                        generator=torch.Generator().manual_seed(seed))
    loss_fn = nn.CrossEntropyLoss()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    for _ in range(epochs):
        model.train()
        total = 0.0
        for xb, yb in loader:
            opt.zero_grad()
            loss = loss_fn(model(xb), yb)
            loss.backward()
            opt.step()
            total += loss.item() * len(yb)
        history.append(total / len(y))
    model.eval()
    return model, history


def predict(model, X):
    model.eval()
    with torch.no_grad():
        return model(torch.as_tensor(X, dtype=torch.float32)).argmax(dim=1).tolist()
''',
"explanation": r'''
Seeding before the model fixes the initial weights, and the seeded generator fixes the batch
order, so the whole run is reproducible. Each batch does one optimisation step; the epoch loss is
the size-weighted mean. Prediction switches to evaluation mode and disables gradient tracking.
''',
"tests": r'''
import numpy as np
import torch


XOR_X = [[0, 0], [0, 1], [1, 0], [1, 1]]
XOR_Y = [0, 1, 1, 0]


def rings(seed=0, n=200):
    rng = np.random.default_rng(seed)
    r = np.where(np.arange(n) % 2 == 0, 1.0, 2.5) + rng.normal(scale=0.2, size=n)
    angle = rng.uniform(0, 2 * np.pi, n)
    return np.c_[r * np.cos(angle), r * np.sin(angle)], (np.arange(n) % 2)


class TestTrainingLoop(unittest.TestCase):
    def test_learns_xor(self):
        model, history = S.train_classifier(XOR_X, XOR_Y, epochs=150, batch_size=4)
        self.assertEqual(S.predict(model, XOR_X), XOR_Y)
        self.assertLess(history[-1], 0.1)

    def test_loss_falls(self):
        X, y = rings()
        _, history = S.train_classifier(X, y, epochs=40)
        self.assertEqual(len(history), 40)
        self.assertLess(history[-1], history[0] / 2)

    def test_generalises_on_rings(self):
        X, y = rings(1)
        Xt, yt = rings(2)
        model, _ = S.train_classifier(X, y, epochs=60)
        self.assertGreater(np.mean(np.array(S.predict(model, Xt)) == yt), 0.9)

    def test_reproducible(self):
        X, y = rings(3, n=60)
        _, a = S.train_classifier(X, y, epochs=5, seed=7)
        _, b = S.train_classifier(X, y, epochs=5, seed=7)
        self.assertEqual(a, b)

    def test_eval_mode_and_shapes(self):
        X, y = rings(4, n=40)
        model, history = S.train_classifier(X, y, n_hidden=8, epochs=2)
        self.assertFalse(model.training)
        self.assertEqual(model[-1].out_features, 2)
        self.assertTrue(all(type(v) is float for v in history))

    def test_three_classes(self):
        X = [[0, 0], [5, 5], [-5, 5]] * 10
        y = [0, 1, 2] * 10
        model, _ = S.train_classifier(X, y, epochs=60)
        self.assertEqual(S.predict(model, [[0, 0.2], [5, 4.8], [-4.8, 5]]), [0, 1, 2])
''',
"feedback": [
    ("test_learns_xor", "Use CrossEntropyLoss on logits and run zero_grad / backward / step for every batch."),
    ("test_reproducible", "Seed with torch.manual_seed(seed) before building the model and pass a seeded generator to the DataLoader."),
    ("test_eval_mode_and_shapes", "Call model.eval() before returning; the last layer has max(y) + 1 outputs."),
    ("test_loss_falls", "Record the size-weighted mean loss once per epoch."),
],
},
# ---------------------------------------------------------------- torch-dropout
{
"slug": "torch-dropout", "title": "Dropout with train() and eval()",
"difficulty": "advanced", "prereqs": ["torch-training-loop"], "packages": ["torch"],
"objectives": ["Add nn.Dropout to a model and explain inverted dropout scaling",
               "Get deterministic predictions with model.eval() and torch.no_grad()",
               "Restore a model's previous mode after evaluation"],
"tags": ["pytorch", "dropout", "regularisation", "train-eval"],
"sources": ["S113", "S104"], "entry": "class DropoutMLP(nn.Module); predict_proba(model, x)",
"article": r'''
# Dropout with train() and eval()

## Intuition
Dropout randomly switches off a fraction p of a layer's activations during training, so the
network cannot rely on any single unit. At prediction time nothing is dropped. To keep the
expected activation the same in both cases, surviving activations are scaled up by 1/(1 − p)
during training — "inverted" dropout.

## Precise explanation
```python
class DropoutMLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out, p=0.5):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Dropout(p),
                                 nn.Linear(n_hidden, n_out))
```

* In `model.train()` mode, `nn.Dropout(p)` zeroes each element with probability p and multiplies
  the rest by 1/(1 − p). Two forward passes give different outputs.
* In `model.eval()` mode it does nothing: predictions are deterministic.
* `model.training` tells you the current mode. A helper that evaluates should restore the mode it
  found, so it can be called in the middle of training.

## Worked example
With p = 0.5 an activation 2.0 becomes either 0 or 4.0 in training (expected value 2.0) and stays
2.0 in evaluation.

## What the library does inside
The mask-and-scale of [[inverted-dropout]] (the optional deep dive after this step), drawn from
PyTorch's random generator, with the mode taken from the module's `training` flag.

## Common mistakes
* Evaluating in training mode: noisy, worse-looking metrics.
* Scaling at test time as well as in training (double compensation).
* Calling `model.eval()` inside a helper and never switching back, so training continues without dropout.

## Why this matters
Dropout is a standard regulariser in MLPs and transformers, and the train/eval switch matters for
every layer that behaves differently during training.
''',
"statement": r'''
1. Write `class DropoutMLP(nn.Module)` with `__init__(self, n_in, n_hidden, n_out, p=0.5)` storing
   `self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Dropout(p), nn.Linear(n_hidden, n_out))`
   and `forward(x)` returning `self.net(x)`. Raise `ValueError` unless `0 <= p < 1`.
2. Write `predict_proba(model, x)` returning softmax probabilities (a tensor) computed in
   evaluation mode under `torch.no_grad()`, and then **restoring** the model's previous mode.
''',
"starter": r'''
import torch
from torch import nn


class DropoutMLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out, p=0.5):
        # TODO
        pass

    def forward(self, x):
        # TODO
        pass


def predict_proba(model, x):
    # TODO
    pass
''',
"hints": [
    "Validate p before building the layers; remember `super().__init__()`.",
    "Save `was_training = model.training`, call `model.eval()`, compute under `torch.no_grad()`.",
    "`torch.softmax(logits, dim=1)`; finally `model.train(was_training)`.",
],
"solution": r'''
import torch
from torch import nn


class DropoutMLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out, p=0.5):
        super().__init__()
        if not 0 <= p < 1:
            raise ValueError("p must be in [0, 1)")
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Dropout(p),
                                 nn.Linear(n_hidden, n_out))

    def forward(self, x):
        return self.net(x)


def predict_proba(model, x):
    was_training = model.training
    model.eval()
    try:
        with torch.no_grad():
            return torch.softmax(model(torch.as_tensor(x, dtype=torch.float32)), dim=1)
    finally:
        model.train(was_training)
''',
"explanation": r'''
`nn.Dropout` reads the module's mode: random masking with 1/(1 − p) scaling while training, the
identity during evaluation. The helper switches to evaluation for deterministic probabilities, turns
off gradient tracking, and restores whatever mode it found, even if an error occurs.
''',
"tests": r'''
import torch
from torch import nn


class TestDropout(unittest.TestCase):
    def test_training_outputs_vary(self):
        torch.manual_seed(0)
        model = S.DropoutMLP(4, 64, 3, p=0.5)
        model.train()
        x = torch.ones(2, 4)
        self.assertFalse(torch.equal(model(x), model(x)))

    def test_predictions_deterministic(self):
        torch.manual_seed(1)
        model = S.DropoutMLP(4, 32, 3)
        x = torch.randn(5, 4)
        a, b = S.predict_proba(model, x), S.predict_proba(model, x)
        self.assertTrue(torch.equal(a, b))
        self.assertTrue(torch.allclose(a.sum(dim=1), torch.ones(5)))

    def test_mode_restored(self):
        model = S.DropoutMLP(2, 4, 2)
        model.train()
        S.predict_proba(model, [[0.0, 1.0]])
        self.assertTrue(model.training)
        model.eval()
        S.predict_proba(model, [[0.0, 1.0]])
        self.assertFalse(model.training)

    def test_inverted_scaling(self):
        torch.manual_seed(2)
        model = S.DropoutMLP(1, 1, 1, p=0.25)
        dropout = model.net[2]
        self.assertIsInstance(dropout, nn.Dropout)
        dropout.train()
        out = dropout(torch.full((1000,), 2.0))
        kept = out[out != 0]
        self.assertTrue(torch.allclose(kept, torch.full_like(kept, 2.0 / 0.75)))
        self.assertAlmostEqual(out.mean().item(), 2.0, delta=0.15)

    def test_no_gradients_tracked(self):
        model = S.DropoutMLP(3, 4, 2)
        self.assertFalse(S.predict_proba(model, torch.randn(2, 3)).requires_grad)

    def test_invalid_p(self):
        for p in (-0.1, 1.0):
            with self.assertRaises(ValueError):
                S.DropoutMLP(2, 2, 2, p=p)
''',
"feedback": [
    ("test_training_outputs_vary", "Put nn.Dropout(p) between the ReLU and the last Linear layer."),
    ("test_predictions_deterministic", "Switch to model.eval() before predicting and return softmax probabilities."),
    ("test_mode_restored", "Remember model.training and call model.train(was_training) at the end."),
    ("test_no_gradients_tracked", "Compute predictions inside torch.no_grad()."),
],
},
# ---------------------------------------------------------------- torch-batchnorm
{
"slug": "torch-batchnorm", "title": "Batch Normalisation with nn.BatchNorm1d",
"difficulty": "advanced", "prereqs": ["torch-dropout"], "packages": ["torch"],
"objectives": ["Explain how BatchNorm1d uses batch statistics in training and running statistics in evaluation",
               "Compute the running mean and variance updates with momentum",
               "Recognise the biased and unbiased variances BatchNorm uses"],
"tags": ["pytorch", "batch-normalisation", "train-eval", "normalisation"],
"sources": ["S112", "S104"], "entry": "run_batchnorm(batches, x_eval, momentum=0.1)",
"article": r'''
# Batch Normalisation with nn.BatchNorm1d

## Intuition
Batch normalisation standardises each feature using the mean and variance of the current batch,
then lets the network rescale and shift it with learned parameters γ and β. That keeps activations
in a well-behaved range and speeds up training. At prediction time there may be a single example,
so the layer uses **running** averages of the statistics it saw during training.

## Precise explanation
For each feature, in training mode:

$$\hat x = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}},\quad y = \gamma \hat x + \beta,$$

with the batch mean μ_B and the **biased** batch variance σ²_B (divide by n). The running
statistics are updated after each batch:

running_mean ← (1 − m)·running_mean + m·μ_B,  running_var ← (1 − m)·running_var + m·s²_B,

where m is `momentum` (default 0.1) and s²_B is the **unbiased** variance (divide by n − 1).
They start at 0 and 1. In `eval()` mode the layer uses running_mean and running_var instead of
batch statistics. γ starts at 1, β at 0, ε = 1e−5.

## Worked example
One batch with feature values [1, 3]: μ_B = 2, biased variance 1 → outputs ≈ [−1, 1]; unbiased
variance 2, so with m = 0.1 running_mean = 0.2 and running_var = 0.9·1 + 0.1·2 = 1.1.

## What the library does inside
The training-mode computation is your [[batchnorm-forward]] (the optional deep dive after this
step); the layer adds the running averages and the mode switch.

## Common mistakes
* Evaluating in training mode, so predictions depend on the other examples in the batch.
* Training with batch size 1 (the variance is undefined; PyTorch raises an error).
* Expecting the running variance to use the same (biased) estimate as the normalisation.

## Why this matters
Batch normalisation is standard in convolutional networks; its train/eval behaviour is a common
source of "it worked in training but not in production" bugs.
''',
"statement": r'''
Write `run_batchnorm(batches, x_eval, momentum=0.1)` that creates one
`nn.BatchNorm1d(n_features, momentum=momentum)`, passes every batch through it in training mode
(in order), then evaluates `x_eval` in evaluation mode. Return
`{"running_mean": list[float], "running_var": list[float], "train_output": list[list[float]], "eval_output": list[list[float]]}`
where `train_output` is the output for the **last** training batch.

* Each batch and `x_eval` are 2-D `(n, n_features)`; convert them to float32 tensors.
* Raise `ValueError` if `batches` is empty or any batch has fewer than 2 rows.
* Compute outputs under `torch.no_grad()`.
''',
"starter": r'''
import torch
from torch import nn


def run_batchnorm(batches, x_eval, momentum=0.1):
    # TODO
    pass
''',
"hints": [
    "Convert each batch with `torch.as_tensor(b, dtype=torch.float32)` and check its row count.",
    "`bn = nn.BatchNorm1d(n_features, momentum=momentum)`; `bn.train()` and pass the batches; then `bn.eval()`.",
    "Read `bn.running_mean.tolist()` and `bn.running_var.tolist()` after the training batches.",
],
"solution": r'''
import torch
from torch import nn


def run_batchnorm(batches, x_eval, momentum=0.1):
    tensors = [torch.as_tensor(b, dtype=torch.float32) for b in batches]
    if not tensors or any(t.ndim != 2 or t.shape[0] < 2 for t in tensors):
        raise ValueError("need at least one batch, each with two or more rows")
    bn = nn.BatchNorm1d(tensors[0].shape[1], momentum=momentum)
    with torch.no_grad():
        bn.train()
        for t in tensors:
            train_output = bn(t)
        bn.eval()
        eval_output = bn(torch.as_tensor(x_eval, dtype=torch.float32))
    return {"running_mean": bn.running_mean.tolist(), "running_var": bn.running_var.tolist(),
            "train_output": train_output.tolist(), "eval_output": eval_output.tolist()}
''',
"explanation": r'''
In training mode each batch is standardised with its own (biased) statistics and the running
averages move towards the batch's mean and unbiased variance. After switching to evaluation, the
layer standardises with the running averages, so its output no longer depends on the batch.
''',
"tests": r'''
import torch


class TestBatchNorm(unittest.TestCase):
    def test_worked_example(self):
        r = S.run_batchnorm([[[1.0], [3.0]]], [[2.0]])
        self.assertAlmostEqual(r["running_mean"][0], 0.2, places=6)
        self.assertAlmostEqual(r["running_var"][0], 1.1, places=6)
        self.assertAlmostEqual(r["train_output"][0][0], -1 / math.sqrt(1 + 1e-5), places=5)

    def test_running_statistics_formula(self):
        torch.manual_seed(0)
        batches = [torch.randn(8, 3) * 2 + 5 for _ in range(4)]
        r = S.run_batchnorm([b.tolist() for b in batches], [[0.0, 0.0, 0.0]], momentum=0.2)
        mean, var = torch.zeros(3), torch.ones(3)
        for b in batches:
            mean = 0.8 * mean + 0.2 * b.mean(dim=0)
            var = 0.8 * var + 0.2 * b.var(dim=0, unbiased=True)
        self.assertTrue(torch.allclose(torch.tensor(r["running_mean"]), mean, atol=1e-5))
        self.assertTrue(torch.allclose(torch.tensor(r["running_var"]), var, atol=1e-4))

    def test_train_output_standardised(self):
        torch.manual_seed(1)
        r = S.run_batchnorm([(torch.randn(64, 2) * 3 + 10).tolist()], [[10.0, 10.0]])
        out = torch.tensor(r["train_output"])
        self.assertTrue(torch.allclose(out.mean(dim=0), torch.zeros(2), atol=1e-5))
        self.assertTrue(torch.allclose(out.var(dim=0, unbiased=False), torch.ones(2), atol=1e-3))

    def test_eval_uses_running_statistics(self):
        r = S.run_batchnorm([[[1.0, 0.0], [3.0, 4.0]], [[2.0, 2.0], [6.0, 2.0]]], [[4.0, 1.0], [0.0, 0.0]])
        mean, var = torch.tensor(r["running_mean"]), torch.tensor(r["running_var"])
        expected = (torch.tensor([[4.0, 1.0], [0.0, 0.0]]) - mean) / torch.sqrt(var + 1e-5)
        self.assertTrue(torch.allclose(torch.tensor(r["eval_output"]), expected, atol=1e-5))

    def test_single_eval_row_allowed(self):
        r = S.run_batchnorm([[[0.0], [2.0]]], [[1.0]])
        self.assertEqual(len(r["eval_output"]), 1)

    def test_invalid_batches(self):
        with self.assertRaises(ValueError):
            S.run_batchnorm([], [[1.0]])
        with self.assertRaises(ValueError):
            S.run_batchnorm([[[1.0, 2.0]]], [[1.0, 2.0]])
''',
"feedback": [
    ("test_running_statistics_formula", "Pass the batches in training mode with momentum=momentum; running_var uses the unbiased variance."),
    ("test_eval_uses_running_statistics", "Call bn.eval() before evaluating x_eval."),
    ("test_train_output_standardised", "Return the output of the last training batch."),
    ("test_invalid_batches", "Reject an empty list and batches with fewer than two rows."),
],
},
# ---------------------------------------------------------------- torch-conv1d
{
"slug": "torch-conv1d", "title": "1-D Convolution with nn.Conv1d",
"difficulty": "advanced", "prereqs": ["torch-batchnorm", "moving-average"], "packages": ["torch"],
"objectives": ["Use F.conv1d and nn.Conv1d with (batch, channels, length) tensors",
               "Compute output lengths from kernel size, stride and padding",
               "Recognise that deep-learning convolution is cross-correlation"],
"tags": ["pytorch", "convolution", "conv1d", "signals"],
"sources": ["S114", "S093"], "entry": "conv1d_layer(x, weight, bias=None, stride=1, padding=0)",
"article": r'''
# 1-D Convolution with nn.Conv1d

## Intuition
A 1-D convolution slides a small kernel along a signal and takes a weighted sum at each position —
a learnable moving average ([[moving-average]]). With several input channels (for example x, y and
z of an accelerometer) each output channel combines all of them.

## Precise explanation
Shapes follow the convention **(batch, channels, length)**:

```python
import torch.nn.functional as F
out = F.conv1d(x, weight, bias, stride=1, padding=0)
# x: (B, C_in, L), weight: (C_out, C_in, K), bias: (C_out,), out: (B, C_out, L_out)
layer = nn.Conv1d(C_in, C_out, kernel_size=K, stride=1, padding=0)   # holds weight and bias
```

$$\text{out}[b, o, t] = \text{bias}[o] + \sum_{c}\sum_{k} \text{weight}[o, c, k]\,x[b, c, t\cdot s + k]$$
(after zero padding), and $L_{out} = \lfloor (L + 2p - K)/s \rfloor + 1$.

* The kernel is **not flipped**: this is cross-correlation, matching `np.correlate`, not
  `np.convolve`. Since the kernel is learned, the difference does not matter for training.
* `padding=K//2` keeps the length for odd K and stride 1.

## Worked example
x = [1, 2, 3, 4, 5] with kernel [1, 0, −1]: outputs are 1 − 3, 2 − 4, 3 − 5 = [−2, −2, −2]
(length 3). With padding 1 the signal becomes [0, 1, 2, 3, 4, 5, 0], giving
[0 − 2, 1 − 3, 2 − 4, 3 − 5, 4 − 0] = [−2, −2, −2, −2, 4] (length 5).

## What the library does inside
Your [[conv1d]] (the optional deep dive after this step) loops over positions; PyTorch unfolds the
windows into a matrix and does one large matrix multiplication for all channels and batch items.

## Common mistakes
* Passing a (B, L, C) tensor (channels last) instead of (B, C, L).
* Flipping the kernel to "do a real convolution" and getting mirrored results.
* Forgetting that stride shortens the output.

## Why this matters
Conv1d models audio, sensor data and text; the 2-D version in Computer Vision works identically
with one more spatial dimension.
''',
"statement": r'''
Write `conv1d_layer(x, weight, bias=None, stride=1, padding=0)` returning
`F.conv1d(x, weight, bias, stride=stride, padding=padding)` as a float32 tensor.

* Accept lists, NumPy arrays or tensors; convert each with `torch.as_tensor(..., dtype=torch.float32)`.
* Raise `ValueError` if `x` is not 3-D, `weight` is not 3-D, the channel counts differ, `bias`
  (when given) does not have one value per output channel, or the padded input is shorter than
  the kernel.

**Example**
```python
conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]])              # tensor([[[-2., -2., -2.]]])
conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]], padding=1)   # tensor([[[-2., -2., -2., -2., 4.]]])
```
''',
"starter": r'''
import torch
import torch.nn.functional as F


def conv1d_layer(x, weight, bias=None, stride=1, padding=0):
    # TODO
    pass
''',
"hints": [
    "Convert x and weight (and bias if given) to float32 tensors.",
    "Check `x.ndim == 3`, `weight.ndim == 3`, `x.shape[1] == weight.shape[1]` and `x.shape[2] + 2 * padding >= weight.shape[2]`.",
    "`F.conv1d(x, weight, bias, stride=stride, padding=padding)`.",
],
"solution": r'''
import torch
import torch.nn.functional as F


def conv1d_layer(x, weight, bias=None, stride=1, padding=0):
    x = torch.as_tensor(x, dtype=torch.float32)
    weight = torch.as_tensor(weight, dtype=torch.float32)
    if x.ndim != 3 or weight.ndim != 3 or x.shape[1] != weight.shape[1]:
        raise ValueError("need x (B, C_in, L) and weight (C_out, C_in, K) with matching C_in")
    if x.shape[2] + 2 * padding < weight.shape[2]:
        raise ValueError("padded input is shorter than the kernel")
    if bias is not None:
        bias = torch.as_tensor(bias, dtype=torch.float32)
        if tuple(bias.shape) != (weight.shape[0],):
            raise ValueError("bias needs one value per output channel")
    return F.conv1d(x, weight, bias, stride=stride, padding=padding)
''',
"explanation": r'''
After conversion and shape checks, `F.conv1d` does the sliding weighted sums for every batch item,
output channel and position at once. Padding adds zeros at both ends; stride skips positions.
''',
"tests": r'''
import numpy as np
import torch
from torch import nn


def manual(x, w, b, stride, padding):
    x = np.pad(np.asarray(x, dtype=float), ((0, 0), (0, 0), (padding, padding)))
    B, C, L = x.shape
    O, _, K = np.shape(w)
    n = (L - K) // stride + 1
    out = np.zeros((B, O, n))
    for bi in range(B):
        for o in range(O):
            for t in range(n):
                out[bi, o, t] = np.sum(np.asarray(w)[o] * x[bi, :, t * stride:t * stride + K]) + (b[o] if b is not None else 0)
    return out


class TestConv1d(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]]).tolist(), [[[-2.0, -2.0, -2.0]]])

    def test_padding(self):
        out = S.conv1d_layer([[[1, 2, 3, 4, 5]]], [[[1, 0, -1]]], padding=1)
        self.assertEqual(out.tolist(), [[[-2.0, -2.0, -2.0, -2.0, 4.0]]])

    def test_not_flipped(self):
        signal = [1.0, 2.0, 0.0, 5.0, 3.0]; kernel = [1.0, 2.0, 3.0]
        out = S.conv1d_layer([[signal]], [[kernel]])[0, 0].numpy()
        self.assertTrue(np.allclose(out, np.correlate(signal, kernel, mode="valid")))

    def test_channels_stride_bias(self):
        rng = np.random.default_rng(0)
        x, w, b = rng.normal(size=(2, 3, 11)), rng.normal(size=(4, 3, 3)), rng.normal(size=4)
        out = S.conv1d_layer(x, w, b, stride=2, padding=1)
        self.assertEqual(tuple(out.shape), (2, 4, (11 + 2 - 3) // 2 + 1))
        self.assertTrue(np.allclose(out.numpy(), manual(x, w, b, 2, 1), atol=1e-5))

    def test_matches_nn_conv1d(self):
        torch.manual_seed(0)
        layer = nn.Conv1d(2, 3, kernel_size=4)
        x = torch.randn(5, 2, 9)
        out = S.conv1d_layer(x, layer.weight.detach(), layer.bias.detach())
        self.assertTrue(torch.allclose(out, layer(x).detach(), atol=1e-6))

    def test_invalid(self):
        cases = [([[1, 2, 3]], [[[1]]], None), ([[[1, 2, 3]]], [[[1], [1]]], None),
                 ([[[1, 2]]], [[[1, 1, 1]]], None), ([[[1, 2, 3]]], [[[1]]], [1, 2])]
        for x, w, b in cases:
            with self.assertRaises(ValueError):
                S.conv1d_layer(x, w, b)
''',
"feedback": [
    ("test_example", "Shapes are (batch, channels, length); call F.conv1d."),
    ("test_not_flipped", "Do not flip the kernel: PyTorch computes cross-correlation."),
    ("test_channels_stride_bias", "Pass bias, stride and padding through to F.conv1d."),
    ("test_invalid", "Check dimensions, channel counts, bias length and that the kernel fits."),
],
},
# ---------------------------------------------------------------- torch-save-load
{
"slug": "torch-save-load", "title": "Saving, Loading and Reproducibility",
"difficulty": "advanced", "prereqs": ["torch-conv1d"], "packages": ["numpy", "torch"],
"objectives": ["Save and restore a model through its state_dict",
               "Load weights safely with weights_only=True",
               "Seed Python, NumPy and PyTorch together for reproducible runs"],
"tags": ["pytorch", "checkpoints", "state-dict", "reproducibility"],
"sources": ["S108", "S109"], "entry": "set_seed(seed); save_model(model, path); load_model(path, n_in, n_hidden, n_out)",
"article": r'''
# Saving, Loading and Reproducibility

## Intuition
Training can take hours, so you save the result. PyTorch saves the **weights** — a dictionary from
parameter names to tensors — not the Python object. To load, you rebuild the same architecture
and pour the weights in. And to rerun an experiment exactly, every random generator must start
from the same seed.

## Precise explanation
```python
torch.save(model.state_dict(), "model.pt")            # an ordered dict of tensors

model = MLP(4, 8, 3)                                    # same architecture, random weights
model.load_state_dict(torch.load("model.pt", weights_only=True))
model.eval()                                            # ready for inference
```

* `state_dict()` keys look like `net.0.weight`; buffers such as BatchNorm's running statistics are
  included too. A different architecture fails to load with a clear `RuntimeError`.
* `weights_only=True` loads only tensors and simple containers. Loading arbitrary pickled objects
  can execute code, so never load untrusted files without it.
* To continue training, also save the optimiser's `state_dict()` (Adam's running averages) and the
  epoch number in one checkpoint dict.
* Reproducibility: seed `random`, `numpy` and `torch` (`torch.manual_seed`) and pass seeded
  generators to DataLoaders. `torch.use_deterministic_algorithms(True)` makes PyTorch raise an
  error instead of silently using a nondeterministic algorithm.

## Worked example
Train, save, then load into a fresh `MLP(4, 8, 3)`: both models give identical outputs on the same
input. Loading the file into `MLP(4, 16, 3)` raises "size mismatch for net.0.weight".

## Common mistakes
* `torch.save(model)` (pickling the whole object): breaks when the class moves or changes.
* Forgetting `model.eval()` after loading a model with dropout or batch normalisation.
* Seeding only PyTorch while the data split uses NumPy's or Python's random generator.

## Why this matters
Checkpoints let you resume, share and deploy models; seeds let others reproduce your results —
and let you check that a change, not luck, improved a metric.
''',
"statement": r'''
1. `set_seed(seed)` seeds `random`, `numpy.random` and `torch`.
2. `class MLP(nn.Module)` with `self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))`.
3. `save_model(model, path)` saves `model.state_dict()` to `path`.
4. `load_model(path, n_in, n_hidden, n_out)` builds an `MLP`, loads the state dict with
   `torch.load(path, weights_only=True)`, switches it to `eval()` and returns it.
''',
"starter": r'''
import random

import numpy as np
import torch
from torch import nn


def set_seed(seed):
    # TODO
    pass


class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()
        # TODO

    def forward(self, x):
        # TODO
        pass


def save_model(model, path):
    # TODO
    pass


def load_model(path, n_in, n_hidden, n_out):
    # TODO
    pass
''',
"hints": [
    "`random.seed(seed)`, `np.random.seed(seed)`, `torch.manual_seed(seed)`.",
    "`torch.save(model.state_dict(), path)`.",
    "`model.load_state_dict(torch.load(path, weights_only=True))`, then `model.eval()`.",
],
"solution": r'''
import random

import numpy as np
import torch
from torch import nn


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class MLP(nn.Module):
    def __init__(self, n_in, n_hidden, n_out):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(n_in, n_hidden), nn.ReLU(), nn.Linear(n_hidden, n_out))

    def forward(self, x):
        return self.net(x)


def save_model(model, path):
    torch.save(model.state_dict(), path)


def load_model(path, n_in, n_hidden, n_out):
    model = MLP(n_in, n_hidden, n_out)
    model.load_state_dict(torch.load(path, weights_only=True))
    model.eval()
    return model
''',
"explanation": r'''
Only the state dict is written, so the file contains tensors keyed by parameter name. Loading
rebuilds the architecture, copies the tensors in (checking every name and shape) and switches to
evaluation. Seeding all three generators makes any later random choice repeatable.
''',
"tests": r'''
import os
import random
import tempfile

import numpy as np
import torch


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.path = os.path.join(self.dir, "model.pt")

    def test_roundtrip_same_outputs(self):
        S.set_seed(0)
        model = S.MLP(4, 8, 3)
        S.save_model(model, self.path)
        loaded = S.load_model(self.path, 4, 8, 3)
        x = torch.randn(5, 4)
        self.assertTrue(torch.equal(model(x), loaded(x)))

    def test_file_holds_state_dict(self):
        S.save_model(S.MLP(2, 3, 1), self.path)
        state = torch.load(self.path, weights_only=True)
        self.assertEqual(list(state), ["net.0.weight", "net.0.bias", "net.2.weight", "net.2.bias"])

    def test_loaded_model_in_eval(self):
        S.save_model(S.MLP(2, 3, 1), self.path)
        self.assertFalse(S.load_model(self.path, 2, 3, 1).training)

    def test_wrong_architecture_rejected(self):
        S.save_model(S.MLP(4, 8, 3), self.path)
        with self.assertRaises(RuntimeError):
            S.load_model(self.path, 4, 16, 3)

    def test_seed_controls_all_generators(self):
        S.set_seed(42)
        a = (random.random(), np.random.rand(), torch.rand(1).item())
        S.set_seed(42)
        b = (random.random(), np.random.rand(), torch.rand(1).item())
        self.assertEqual(a, b)

    def test_seeded_models_identical(self):
        S.set_seed(3); a = S.MLP(3, 3, 3)
        S.set_seed(3); b = S.MLP(3, 3, 3)
        self.assertTrue(all(torch.equal(p, q) for p, q in zip(a.parameters(), b.parameters())))
''',
"feedback": [
    ("test_roundtrip_same_outputs", "Save model.state_dict() and load it into a freshly built MLP."),
    ("test_file_holds_state_dict", "torch.save the state_dict, not the model object."),
    ("test_loaded_model_in_eval", "Call model.eval() after loading."),
    ("test_seed_controls_all_generators", "Seed random, numpy.random and torch."),
],
},
# ---------------------------------------------------------------- torch-debugging
{
"slug": "torch-debugging", "title": "Debugging Training",
"difficulty": "advanced", "prereqs": ["torch-save-load"], "packages": ["torch"],
"objectives": ["Check a model and loss by overfitting a single small batch",
               "Recognise diverging, stuck and healthy loss curves",
               "Measure gradient norms and tame exploding gradients with clipping"],
"tags": ["pytorch", "debugging", "gradient-clipping", "learning-rate", "training-dynamics"],
"sources": ["S111", "S106"], "entry": "diagnose(losses); overfit_one_batch(model, X, y, steps=200, lr=0.01); train_with_clipping(model, X, y, lr, steps, max_norm=None)",
"article": r'''
# Debugging Training

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
''',
"statement": r'''
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
''',
"starter": r'''
import math

import torch
from torch import nn


def diagnose(losses):
    # TODO
    pass


def overfit_one_batch(model, X, y, steps=200, lr=0.01):
    # TODO
    pass


def train_with_clipping(model, X, y, lr, steps, max_norm=None):
    # TODO
    pass
''',
"hints": [
    "`diagnose`: check `math.isfinite` for every loss first, then compare the last loss with the first.",
    "Both training functions use the usual cycle: zero_grad, loss, backward, (clip), step.",
    "`torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)` goes after `loss.backward()`.",
],
"solution": r'''
import math

import torch
from torch import nn


def diagnose(losses):
    if len(losses) < 2:
        raise ValueError("need at least two losses")
    if not all(math.isfinite(v) for v in losses) or losses[-1] > 2 * losses[0]:
        return "diverging"
    if losses[-1] > 0.95 * losses[0]:
        return "stuck"
    return "learning"


def overfit_one_batch(model, X, y, steps=200, lr=0.01):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.long)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    model.train()
    for _ in range(steps):
        opt.zero_grad()
        loss = loss_fn(model(X), y)
        loss.backward()
        opt.step()
    with torch.no_grad():
        return float(loss_fn(model(X), y))


def train_with_clipping(model, X, y, lr, steps, max_norm=None):
    X = torch.as_tensor(X, dtype=torch.float32)
    y = torch.as_tensor(y, dtype=torch.float32)
    opt = torch.optim.SGD(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    losses = []
    for _ in range(steps):
        opt.zero_grad()
        loss = loss_fn(model(X), y)
        losses.append(loss.item())
        loss.backward()
        if max_norm is not None:
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)
        opt.step()
    return losses
''',
"explanation": r'''
`diagnose` encodes the loss-curve table. Overfitting one batch is a plain training loop on a tiny
fixed batch; reaching a near-zero loss shows the model, labels and loss are wired correctly.
Clipping rescales the gradients after `backward()` so that no single step can be enormous.
''',
"tests": r'''
import torch
from torch import nn


def big_regression(seed=0):
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(32, 3, generator=g) * 20
    return X, X @ torch.tensor([[1.0], [-2.0], [0.5]])


class TestDebugging(unittest.TestCase):
    def test_diagnose_patterns(self):
        self.assertEqual(S.diagnose([1.0, 0.5, 0.2]), "learning")
        self.assertEqual(S.diagnose([1.0, 0.99, 0.98]), "stuck")
        self.assertEqual(S.diagnose([1.0, 3.0, 9.0]), "diverging")
        self.assertEqual(S.diagnose([1.0, float("nan")]), "diverging")

    def test_overfit_tiny_batch(self):
        torch.manual_seed(0)
        model = nn.Sequential(nn.Linear(4, 32), nn.ReLU(), nn.Linear(32, 3))
        X = torch.randn(12, 4, generator=torch.Generator().manual_seed(1))
        y = torch.arange(12) % 3
        self.assertLess(S.overfit_one_batch(model, X, y, steps=300, lr=0.01), 0.05)

    def test_more_steps_lower_loss(self):
        X = torch.randn(12, 4, generator=torch.Generator().manual_seed(2))
        y = torch.arange(12) % 3
        torch.manual_seed(0)
        short = S.overfit_one_batch(nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3)), X, y, steps=5)
        torch.manual_seed(0)
        long = S.overfit_one_batch(nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3)), X, y, steps=100)
        self.assertIs(type(short), float)
        self.assertLess(long, short)

    def test_high_lr_diverges_without_clipping(self):
        X, y = big_regression()
        torch.manual_seed(0)
        losses = S.train_with_clipping(nn.Linear(3, 1), X, y, lr=0.05, steps=15)
        self.assertEqual(S.diagnose(losses), "diverging")

    def test_clipping_keeps_training_stable(self):
        X, y = big_regression()
        torch.manual_seed(0)
        losses = S.train_with_clipping(nn.Linear(3, 1), X, y, lr=0.05, steps=150, max_norm=1.0)
        self.assertTrue(all(math.isfinite(v) for v in losses))
        self.assertLess(losses[-1], losses[0] / 10)

    def test_short_history_rejected(self):
        with self.assertRaises(ValueError):
            S.diagnose([1.0])
''',
"feedback": [
    ("test_diagnose_patterns", "Check for non-finite values first, then last > 2 × first, then last > 0.95 × first."),
    ("test_overfit_tiny_batch", "Train with CrossEntropyLoss and Adam for the given steps and return the final loss."),
    ("test_clipping_keeps_training_stable", "Call clip_grad_norm_ after backward() and before step()."),
    ("test_high_lr_diverges_without_clipping", "Record each loss before the update, using MSELoss and SGD."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "digit-recogniser", "title": "Handwritten Digit Recogniser",
"tags": ["image-classification", "pytorch", "mlp"],
"brief": r'''
Train a neural network that recognises handwritten digits, then try it on digits you draw
yourself. Start with the small 8×8 digits that ship with scikit-learn, then move to MNIST's 28×28
images.
''',
"uses": ["torch-mlp-module", "torch-datasets", "torch-training-loop"],
"milestones": [
    "Load the 8×8 digits with sklearn.datasets.load_digits, scale pixels to [0, 1] and split train/validation/test.",
    "Train an MLP with the training loop from the course and plot train and validation loss per epoch.",
    "Report test accuracy and a confusion matrix; look at the ten worst mistakes.",
    "Switch to MNIST through torchvision and train the same model on 28×28 images.",
    "Write a predict(image) function and test it on digits you draw yourself (scaled to the same size).",
],
"stretch": [
    "Add dropout and compare validation curves; save the best model with its state_dict.",
    "Replace the MLP with a small CNN (see the Computer Vision topic).",
    "Make a tiny web page or FastAPI endpoint where you draw a digit and get a prediction.",
],
"data": r'''
* 1,797 8×8 digits bundled with scikit-learn (no download):
  [`sklearn.datasets.load_digits`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html).
* MNIST, 70,000 28×28 digits, downloaded by
  [`torchvision.datasets.MNIST`](https://docs.pytorch.org/vision/stable/generated/torchvision.datasets.MNIST.html).
''',
"setup": r'''
```bash
pip install torch torchvision scikit-learn matplotlib
python train_digits.py
```
A CPU is enough: an MLP on MNIST trains in a few minutes.
''',
},
{
"kind": "project", "slug": "training-diagnostics", "title": "Training Diagnostics Notebook",
"tags": ["debugging", "learning-rate", "overfitting"],
"brief": r'''
Build a reusable notebook (or script) of experiments that explain why a model trains well or badly:
a learning-rate finder, loss curves for good and bad settings, an overfitting demonstration and
gradient-norm plots. Use it on your digit recogniser or any other model.
''',
"uses": ["torch-optimizers", "torch-training-loop", "torch-dropout", "torch-debugging"],
"milestones": [
    "Write a function that trains a model for a few epochs and returns train and validation losses.",
    "Learning-rate finder: increase the learning rate exponentially over one epoch and plot loss against learning rate.",
    "Show three curves side by side: learning rate too low, about right and too high.",
    "Demonstrate overfitting with a large model on 200 examples, then fix it with dropout or weight decay.",
    "Log the gradient norm of every layer per step and show the effect of gradient clipping.",
],
"stretch": [
    "Add a learning-rate schedule (cosine or one-cycle) and compare final accuracy.",
    "Track experiments in a CSV file and compare runs with different seeds.",
    "Use TensorBoard to view the curves live.",
],
"data": r'''
Any small classification dataset works: `sklearn.datasets.load_digits()` (bundled) or synthetic data
from `sklearn.datasets.make_moons(n_samples=1000, noise=0.25, random_state=0)`.
''',
"setup": r'''
```bash
pip install torch scikit-learn matplotlib jupyter
jupyter notebook
```
''',
},
]
