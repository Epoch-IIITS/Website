"""Deep Learning steps added in the 2026-10 revision: a scalar autograd engine, backpropagation
through a dense layer, and the Adam optimiser."""

PROBLEMS = [
# ---------------------------------------------------------------- scalar-autograd
{
"slug": "scalar-autograd", "title": "A Tiny Autograd Engine",
"difficulty": "intermediate", "prereqs": ["torch-mlp-module", "derivative-rules"], "packages": [],
"objectives": ["Represent a computation as a graph of Value objects",
               "Give each operation a local backward rule from the chain rule",
               "Run backpropagation in reverse topological order and accumulate gradients",
               "Explain what PyTorch's autograd automates"],
"tags": ["autograd", "computational-graph", "backpropagation", "chain-rule", "operator-overloading"],
"sources": ["S094", "S016", "S092"], "entry": "class Value(data); Value.backward()",
"article": r'''
# A Tiny Autograd Engine

## Intuition
A neural network's loss is built from many small operations: multiply, add, `tanh`, ... If every
operation knows its own derivative, the chain rule ([[derivative-rules]]) lets us compute the
derivative of the loss with respect to *every* input by walking the computation backwards. That
is **automatic differentiation**, the engine inside PyTorch and every deep-learning library.

## Precise explanation
Wrap each number in a `Value` that records how it was made:
```python
class Value:
    def __init__(self, data, _children=()):
        self.data = float(data)
        self.grad = 0.0                 # d(output)/d(this value), filled in by backward()
        self._prev = set(_children)
        self._backward = lambda: None   # pushes self.grad to the children
```
Each operation creates a new `Value` and a closure that applies its **local** derivative:
* `out = a + b`: `a.grad += out.grad`, `b.grad += out.grad`.
* `out = a * b`: `a.grad += b.data * out.grad`, `b.grad += a.data * out.grad`.
* `out = a ** k` (number k): `a.grad += k * a.data ** (k - 1) * out.grad`.
* `out = a.tanh()`: `a.grad += (1 - out.data ** 2) * out.grad`.
* `out = a.exp()`: `a.grad += out.data * out.grad`.

`backward()` on the final value: (1) order all nodes so each appears after its children
(**topological order**, by depth-first search); (2) set the output's `grad = 1`; (3) call every
`_backward` in **reverse** order. Gradients use `+=` because a value used twice (e.g. `a * a`)
receives a contribution from each use.

Operator overloading makes it feel like normal maths: define `__add__`, `__mul__`, `__neg__`,
`__sub__`, `__pow__`, and the reflected `__radd__`, `__rmul__` so that `2 * a` and `1 + a` work.
Wrap plain numbers in `Value` inside each operation.

## Worked example
`a = Value(2); b = Value(-3); c = a * b + a` → `c.data = -4`. Backward:
$\partial c/\partial a = b + 1 = -2$, $\partial c/\partial b = a = 2$.

## Common mistakes
* Assigning `a.grad = ...` instead of accumulating with `+=` (wrong when a value is reused).
* Calling the backward closures in forward order.
* Forgetting the reflected operators, so `2 * a` raises `TypeError`.
* Calling `backward()` twice without resetting grads (they accumulate, as in PyTorch).

## Why this matters
[[neuron-backprop]] and [[dense-backward]] derive the same gradients by hand for whole arrays;
frameworks do it automatically with exactly this algorithm.
''',
"statement": r'''
Write `class Value` supporting:

* `Value(data)` with attributes `data` (float) and `grad` (starts at `0.0`).
* `+`, `*`, unary `-`, `-` (binary), `**` with an `int`/`float` exponent, and the reflected forms
  `number + Value`, `number * Value`, `number - Value`. Plain numbers are wrapped in `Value`.
* Methods `tanh()` and `exp()`.
* `backward()` — sets this value's gradient to 1 and fills `grad` for every value it depends on,
  using reverse topological order and accumulated (`+=`) gradients.

**Example**
```python
a, b = Value(2.0), Value(-3.0)
c = a * b + a
c.backward()
(c.data, a.grad, b.grad)    # (-4.0, -2.0, 2.0)
```
''',
"starter": r'''
import math


class Value:
    def __init__(self, data, _children=()):
        self.data = float(data)
        self.grad = 0.0
        self._prev = set(_children)
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    # TODO: __mul__, __pow__, __neg__, __sub__, __radd__, __rmul__, __rsub__, tanh, exp

    def backward(self):
        # TODO: topological order, then call _backward in reverse
        self.grad = 1.0

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
''',
"hints": [
    "Copy the `__add__` pattern for `__mul__`: the local derivatives are `other.data` and `self.data`.",
    "`__neg__` can return `self * -1`, `__sub__` can return `self + (-other)`; `__radd__` returns `self + other` and `__rsub__` returns `other + (-self)`.",
    "Topological order: a recursive `build(v)` that visits `v._prev` first, then appends `v`; skip nodes already in a `visited` set.",
],
"solution": r'''
import math


class Value:
    def __init__(self, data, _children=()):
        self.data = float(data)
        self.grad = 0.0
        self._prev = set(_children)
        self._backward = lambda: None

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other))

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other))

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, k):
        out = Value(self.data ** k, (self,))

        def _backward():
            self.grad += k * self.data ** (k - 1) * out.grad
        out._backward = _backward
        return out

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def __rsub__(self, other):
        return other + (-self)

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,))

        def _backward():
            self.grad += (1 - t * t) * out.grad
        out._backward = _backward
        return out

    def exp(self):
        out = Value(math.exp(self.data), (self,))

        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward
        return out

    def backward(self):
        order, visited = [], set()

        def build(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build(child)
                order.append(v)
        build(self)
        self.grad = 1.0
        for v in reversed(order):
            v._backward()

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"
''',
"explanation": r'''
Every operation stores its inputs and a closure implementing its local chain-rule step.
`backward` performs a depth-first search to list nodes after their children, seeds the output
gradient with 1 and runs the closures from the output back to the leaves. Accumulating with `+=`
handles values that are used several times. Derived operations (`-`, subtraction, reflected
operators) are built from `+` and `*`, so they need no backward rule of their own.
''',
"tests": r'''
def numeric(f, xs, i, h=1e-6):
    up = list(xs); down = list(xs)
    up[i] += h; down[i] -= h
    return (f(*up) - f(*down)) / (2 * h)


class TestAutograd(unittest.TestCase):
    def test_example(self):
        a, b = S.Value(2.0), S.Value(-3.0)
        c = a * b + a
        c.backward()
        self.assertEqual((c.data, a.grad, b.grad), (-4.0, -2.0, 2.0))

    def test_reused_value_accumulates(self):
        a = S.Value(3.0)
        y = a * a + a
        y.backward()
        self.assertAlmostEqual(a.grad, 2 * 3.0 + 1)

    def test_reflected_and_sub(self):
        a = S.Value(4.0)
        y = 2 * a + 1 - a
        z = 10 - a
        self.assertEqual(y.data, 5.0)
        self.assertEqual(z.data, 6.0)
        y.backward()
        self.assertAlmostEqual(a.grad, 1.0)

    def test_pow_and_neg(self):
        a = S.Value(1.5)
        y = -(a ** 3)
        y.backward()
        self.assertAlmostEqual(y.data, -3.375)
        self.assertAlmostEqual(a.grad, -3 * 1.5 ** 2)

    def test_tanh_exp(self):
        a = S.Value(0.3)
        y = a.tanh() * a.exp()
        y.backward()
        f = lambda x: math.tanh(x) * math.exp(x)
        self.assertAlmostEqual(y.data, f(0.3))
        self.assertAlmostEqual(a.grad, numeric(f, [0.3], 0), places=6)

    def test_neuron_matches_numeric(self):
        def f(x1, x2, w1, w2, b):
            return math.tanh(x1 * w1 + x2 * w2 + b) ** 2
        vals = [2.0, -1.0, -0.4, 0.7, 0.1]
        x1, x2, w1, w2, b = [S.Value(v) for v in vals]
        out = (x1 * w1 + x2 * w2 + b).tanh() ** 2
        out.backward()
        for i, node in enumerate([x1, x2, w1, w2, b]):
            self.assertAlmostEqual(node.grad, numeric(f, vals, i), places=6)

    def test_deep_chain_order(self):
        x = S.Value(0.5)
        y = x
        for _ in range(30):
            y = y * 1.1 + 0.01
        y.backward()
        self.assertAlmostEqual(x.grad, 1.1 ** 30, places=6)
''',
"feedback": [
    ("test_example", "Implement `__mul__` with local derivatives `other.data` and `self.data`, and a working `backward`."),
    ("test_reused_value_accumulates", "Use `+=` in every backward closure so reused values collect all contributions."),
    ("test_reflected_and_sub", "Add `__radd__`, `__rmul__`, `__sub__` and `__rsub__`, wrapping numbers in Value."),
    ("test_tanh_exp", "tanh's derivative is `1 - t**2`; exp's derivative is its own output."),
    ("test_deep_chain_order", "Visit nodes in reverse topological order so each gradient is complete before it is pushed further."),
],
"library": {
"text": r'''
PyTorch's autograd records the same graph for tensors: create inputs with
`torch.tensor(2.0, requires_grad=True)`, compute, call `loss.backward()`, and read `x.grad`.
It supports thousands of operations and runs on GPUs, but the algorithm — local derivatives
applied in reverse topological order with accumulation — is the one you wrote. The comparison
runs only when PyTorch is installed.
''',
"optional": ["torch"],
"tests": r'''
try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch_autograd(self):
        vals = [0.8, -1.2, 0.3]
        a, b, c = [S.Value(v) for v in vals]
        out = ((a * b + c).tanh() * (a ** 2)).exp() - 3 * b
        out.backward()
        ta, tb, tc = [torch.tensor(v, dtype=torch.float64, requires_grad=True) for v in vals]
        tout = (torch.tanh(ta * tb + tc) * ta ** 2).exp() - 3 * tb
        tout.backward()
        self.assertAlmostEqual(out.data, tout.item(), places=10)
        for mine, theirs in zip((a, b, c), (ta, tb, tc)):
            self.assertAlmostEqual(mine.grad, theirs.grad.item(), places=10)
''',
},
},
# ---------------------------------------------------------------- dense-backward
{
"slug": "dense-backward", "title": "Backpropagation Through a Dense Layer",
"difficulty": "intermediate", "prereqs": ["neuron-backprop"], "packages": ["numpy"],
"objectives": ["Derive dX, dW and db for Y = XW + b from the chain rule",
               "Backpropagate through ReLU", "Compute the mean-squared-error loss and its gradient",
               "Check every gradient shape against its parameter's shape"],
"tags": ["backpropagation", "dense-layer", "relu", "matrix-calculus", "gradients"],
"sources": ["S016", "S013"], "entry": "dense_backward(X, W, dY); relu_backward(Z, dA); mse_and_grad(Y_hat, Y); two_layer_grads(X, Y, params)",
"article": r'''
# Backpropagation Through a Dense Layer

## Intuition
[[neuron-backprop]] differentiated one neuron for one example. A dense layer is many neurons
applied to a batch at once: $Y = XW + b$. The same chain rule gives compact matrix formulas, and
there is a simple check: every gradient has exactly the same shape as the thing it is the
gradient of.

## Precise explanation
Shapes: $X$ is $(n, d_{in})$, $W$ is $(d_{in}, d_{out})$, $b$ is $(d_{out},)$, and the upstream
gradient $dY = \partial L/\partial Y$ is $(n, d_{out})$. Then
$$dW = X^\top dY \;(d_{in}, d_{out}), \qquad db = \textstyle\sum_{\text{rows}} dY \;(d_{out},),
  \qquad dX = dY\, W^\top \;(n, d_{in}).$$
Each entry $Y_{ij} = \sum_k X_{ik}W_{kj} + b_j$, so $\partial Y_{ij}/\partial W_{kj} = X_{ik}$; summing
over examples $i$ gives $X^\top dY$. The bias is added to every row, so its gradient sums rows.

**ReLU** $A = \max(0, Z)$: $dZ = dA \cdot [Z > 0]$ (gradient passes where the input was positive).

**MSE loss** over all entries: $L = \frac{1}{m}\sum (\hat Y - Y)^2$ with $m$ the number of
entries, so $\partial L/\partial \hat Y = \frac{2}{m}(\hat Y - Y)$.

**Two-layer network** $H = \mathrm{ReLU}(XW_1 + b_1)$, $\hat Y = HW_2 + b_2$: start from
$d\hat Y$, apply the dense rule for layer 2 (giving $dW_2, db_2, dH$), the ReLU rule, then the
dense rule for layer 1.

## Worked example
$X = [[1, 2]]$, $W = [[1], [-1]]$, $dY = [[3]]$: $dW = X^\top dY = [[3], [6]]$, $db = [3]$,
$dX = dY W^\top = [[3, -3]]$.

## Common mistakes
* $dW = dY^\top X$ — the transpose of the right answer (shape $(d_{out}, d_{in})$).
* Averaging $db$ over the batch when the loss already divided by $n$ (dividing twice).
* ReLU backward using $A > 0$ vs $Z > 0$ is fine, but using `dA > 0` is wrong.

## Why this matters
These four lines are the backward pass of every fully connected network; [[gradient-check]]
verifies them numerically and [[train-xor-mlp]] uses them to train.
''',
"statement": r'''
Implement with NumPy:

1. `dense_backward(X, W, dY)` → `(dX, dW, db)`.
2. `relu_backward(Z, dA)` → `dZ`.
3. `mse_and_grad(Y_hat, Y)` → `(loss, dY_hat)` with the mean over **all** entries; `loss` is a
   float.
4. `two_layer_grads(X, Y, params)` with `params = {"W1", "b1", "W2", "b2"}` for
   $H = \mathrm{ReLU}(XW_1+b_1)$, $\hat Y = HW_2 + b_2$ → `(loss, grads)` where `grads` has the
   same keys and shapes as `params`.
''',
"starter": r'''
import numpy as np


def dense_backward(X, W, dY):
    # TODO
    return None, None, None


def relu_backward(Z, dA):
    # TODO
    return dA


def mse_and_grad(Y_hat, Y):
    diff = np.asarray(Y_hat, dtype=float) - np.asarray(Y, dtype=float)
    loss = float(np.mean(diff ** 2))
    # TODO: gradient
    return loss, np.zeros_like(diff)


def two_layer_grads(X, Y, params):
    # TODO: forward pass, then backward through both layers
    return 0.0, {k: np.zeros_like(v) for k, v in params.items()}
''',
"hints": [
    "`dW = X.T @ dY`, `db = dY.sum(axis=0)`, `dX = dY @ W.T`.",
    "`relu_backward` is `dA * (Z > 0)`; the MSE gradient is `2 * diff / diff.size`.",
    "Forward: `Z1 = X @ W1 + b1`, `H = np.maximum(Z1, 0)`, `Y_hat = H @ W2 + b2`; backward: dense (layer 2) → relu → dense (layer 1).",
],
"solution": r'''
import numpy as np


def dense_backward(X, W, dY):
    X, W, dY = (np.asarray(a, dtype=float) for a in (X, W, dY))
    return dY @ W.T, X.T @ dY, dY.sum(axis=0)


def relu_backward(Z, dA):
    return np.asarray(dA, dtype=float) * (np.asarray(Z) > 0)


def mse_and_grad(Y_hat, Y):
    diff = np.asarray(Y_hat, dtype=float) - np.asarray(Y, dtype=float)
    return float(np.mean(diff ** 2)), 2 * diff / diff.size


def two_layer_grads(X, Y, params):
    X = np.asarray(X, dtype=float)
    Z1 = X @ params["W1"] + params["b1"]
    H = np.maximum(Z1, 0)
    Y_hat = H @ params["W2"] + params["b2"]
    loss, dY = mse_and_grad(Y_hat, Y)
    dH, dW2, db2 = dense_backward(H, params["W2"], dY)
    dZ1 = relu_backward(Z1, dH)
    _, dW1, db1 = dense_backward(X, params["W1"], dZ1)
    return loss, {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}
''',
"explanation": r'''
The dense rule follows from $Y_{ij} = \sum_k X_{ik}W_{kj} + b_j$; each output is a transposed product
that matches the parameter's shape. ReLU masks the upstream gradient, and the MSE gradient is
$2(\hat Y - Y)/m$. The two-layer network simply chains these pieces from the loss back to the
input, reusing values cached during the forward pass.
''',
"tests": r'''
import numpy as np


def numeric_grad(f, P, h=1e-6):
    g = np.zeros_like(P)
    for idx in np.ndindex(P.shape):
        old = P[idx]
        P[idx] = old + h; up = f()
        P[idx] = old - h; down = f()
        P[idx] = old
        g[idx] = (up - down) / (2 * h)
    return g


class TestDenseBackward(unittest.TestCase):
    def test_example(self):
        dX, dW, db = S.dense_backward([[1.0, 2.0]], [[1.0], [-1.0]], [[3.0]])
        np.testing.assert_allclose(dW, [[3.0], [6.0]])
        np.testing.assert_allclose(db, [3.0])
        np.testing.assert_allclose(dX, [[3.0, -3.0]])

    def test_shapes(self):
        rng = np.random.default_rng(0)
        X, W, dY = rng.normal(size=(5, 3)), rng.normal(size=(3, 4)), rng.normal(size=(5, 4))
        dX, dW, db = S.dense_backward(X, W, dY)
        self.assertEqual((dX.shape, dW.shape, db.shape), (X.shape, W.shape, (4,)))

    def test_dense_numeric(self):
        rng = np.random.default_rng(1)
        X, W, b = rng.normal(size=(4, 3)), rng.normal(size=(3, 2)), rng.normal(size=2)
        T = rng.normal(size=(4, 2))
        loss = lambda: float(np.sum((X @ W + b) * T))
        dX, dW, db = S.dense_backward(X, W, T)
        np.testing.assert_allclose(dW, numeric_grad(loss, W), atol=1e-6)
        np.testing.assert_allclose(db, numeric_grad(loss, b), atol=1e-6)
        np.testing.assert_allclose(dX, numeric_grad(loss, X), atol=1e-6)

    def test_relu_backward(self):
        Z = np.array([[-1.0, 0.0, 2.0]])
        np.testing.assert_array_equal(S.relu_backward(Z, np.array([[5.0, 5.0, 5.0]])), [[0.0, 0.0, 5.0]])

    def test_mse(self):
        loss, g = S.mse_and_grad([[1.0, 2.0], [3.0, 4.0]], [[1.0, 0.0], [3.0, 2.0]])
        self.assertAlmostEqual(loss, 2.0)
        np.testing.assert_allclose(g, [[0.0, 1.0], [0.0, 1.0]])

    def test_two_layer_numeric(self):
        rng = np.random.default_rng(2)
        X, Y = rng.normal(size=(6, 3)), rng.normal(size=(6, 2))
        params = {"W1": rng.normal(size=(3, 5)), "b1": rng.normal(size=5) * 0.1,
                  "W2": rng.normal(size=(5, 2)), "b2": np.zeros(2)}
        loss, grads = S.two_layer_grads(X, Y, params)
        self.assertEqual(set(grads), set(params))
        for k in params:
            num = numeric_grad(lambda: S.two_layer_grads(X, Y, params)[0], params[k])
            np.testing.assert_allclose(grads[k], num, atol=1e-5, err_msg=k)
''',
"feedback": [
    ("test_example", "Use `dW = X.T @ dY`, `db = dY.sum(axis=0)`, `dX = dY @ W.T`."),
    ("test_shapes", "Each gradient must have the shape of what it differentiates."),
    ("test_relu_backward", "Pass the gradient only where Z > 0."),
    ("test_mse", "Divide by the total number of entries: `2 * diff / diff.size`."),
    ("test_two_layer_numeric", "Run the forward pass, then dense (layer 2) → ReLU → dense (layer 1)."),
],
"library": {
"text": r'''
In PyTorch the layer is `torch.nn.Linear(d_in, d_out)` (it stores the weight transposed, shape
`(d_out, d_in)`) and `loss.backward()` computes exactly these gradients. The comparison below
builds the same two-layer network in PyTorch and checks the gradients match; it runs only when
PyTorch is installed.
''',
"optional": ["torch"],
"tests": r'''
try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch(self):
        rng = np.random.default_rng(3)
        X, Y = rng.normal(size=(4, 3)), rng.normal(size=(4, 2))
        params = {"W1": rng.normal(size=(3, 4)), "b1": rng.normal(size=4),
                  "W2": rng.normal(size=(4, 2)), "b2": rng.normal(size=2)}
        loss, grads = S.two_layer_grads(X, Y, params)
        t = {k: torch.tensor(v, requires_grad=True) for k, v in params.items()}
        H = torch.relu(torch.tensor(X) @ t["W1"] + t["b1"])
        tloss = torch.mean((H @ t["W2"] + t["b2"] - torch.tensor(Y)) ** 2)
        tloss.backward()
        self.assertAlmostEqual(loss, tloss.item(), places=10)
        for k in params:
            np.testing.assert_allclose(grads[k], t[k].grad.numpy(), atol=1e-10)
''',
},
},
# ---------------------------------------------------------------- adam-optimizer
{
"slug": "adam-optimizer", "title": "The Adam Optimiser", "optional": True,
"difficulty": "advanced", "prereqs": ["sgd-momentum"], "packages": ["numpy"],
"objectives": ["Maintain first- and second-moment estimates of the gradient",
               "Apply bias correction for the early steps",
               "Explain why Adam's step size is roughly lr regardless of gradient scale",
               "Use the same params/grads dictionary interface as Momentum"],
"tags": ["optimisers", "adam", "adaptive-learning-rate", "bias-correction"],
"sources": ["S095", "S013"], "entry": "class Adam(lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8); Adam.step(params, grads)",
"article": r'''
# The Adam Optimiser

## Intuition
[[sgd-momentum]] smooths the *direction* of the gradient. Adam also adapts the *step size* of each
parameter: parameters whose gradients are consistently large take proportionally smaller steps,
and rarely-updated parameters take larger ones. It is the default optimiser for most deep
learning.

## Precise explanation
For each parameter, keep $m$ (moving average of gradients) and $v$ (moving average of squared
gradients), both starting at 0, and a step counter $t$ shared by all parameters. At step
$t = 1, 2, \dots$:
$$m \leftarrow \beta_1 m + (1-\beta_1) g,\qquad v \leftarrow \beta_2 v + (1-\beta_2) g^2,$$
$$\hat m = \frac{m}{1-\beta_1^t},\qquad \hat v = \frac{v}{1-\beta_2^t},\qquad
  \theta \leftarrow \theta - \text{lr}\,\frac{\hat m}{\sqrt{\hat v} + \epsilon}.$$
* **Bias correction**: because $m$ and $v$ start at 0 they are too small early on; dividing by
  $1-\beta^t$ fixes that. At $t = 1$, $\hat m = g$ and $\hat v = g^2$, so the first step is
  $\text{lr}\cdot g/(|g| + \epsilon) \approx \text{lr}\cdot\operatorname{sign}(g)$.
* Multiplying all gradients by a constant leaves the steps (almost) unchanged — Adam is
  scale-invariant, unlike plain SGD.
* Defaults from the paper: $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$.

## Worked example
$g = 4$, lr $= 0.1$, first step: $m = 0.4$, $v = 0.016$, $\hat m = 4$, $\hat v = 16$, step
$= 0.1 \cdot 4/(4 + 10^{-8}) \approx 0.1$.

## Common mistakes
* Incrementing $t$ once per parameter instead of once per `step` call.
* Forgetting bias correction, giving tiny early steps.
* Putting $\epsilon$ inside the square root (a different, but common, variant; the paper puts it
  outside).

## Why this matters
Adam (and its variant AdamW) trains most transformers and CNNs; knowing its update explains
learning-rate choices and warm-up schedules.
''',
"statement": r'''
Write `class Adam` with the same interface as `Momentum` in [[sgd-momentum]]:

* `Adam(lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8)`; raise `ValueError` unless `lr > 0` and
  `0 <= beta1 < 1` and `0 <= beta2 < 1`.
* Attributes `m` and `v` (dicts, filled lazily per key with zeros) and `t` (starts at 0).
* `step(params, grads)` — both dicts of arrays with the same keys and shapes (else
  `ValueError`); increment `t` once, update every parameter by the formulas above, and return a
  **new** dict of updated parameters (do not modify the inputs).
''',
"starter": r'''
import numpy as np


class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr, self.beta1, self.beta2, self.eps = lr, beta1, beta2, eps
        self.m, self.v, self.t = {}, {}, 0

    def step(self, params, grads):
        # TODO: validate, increment t, update m, v, apply bias correction
        return {k: np.asarray(p, dtype=float) - self.lr * np.asarray(grads[k]) for k, p in params.items()}
''',
"hints": [
    "Validate in `__init__`; in `step`, compare `set(params) != set(grads)` and each pair of shapes.",
    "Increment `self.t` once at the start of `step`, then loop over keys; create zeros with `np.zeros_like(p)` the first time a key is seen.",
    "`m_hat = m / (1 - beta1 ** t)`, `v_hat = v / (1 - beta2 ** t)`, `p - lr * m_hat / (np.sqrt(v_hat) + eps)`.",
],
"solution": r'''
import numpy as np


class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        if lr <= 0 or not 0 <= beta1 < 1 or not 0 <= beta2 < 1:
            raise ValueError("need lr > 0 and 0 <= beta1, beta2 < 1")
        self.lr, self.beta1, self.beta2, self.eps = lr, beta1, beta2, eps
        self.m, self.v, self.t = {}, {}, 0

    def step(self, params, grads):
        if set(params) != set(grads):
            raise ValueError("params and grads must have the same keys")
        self.t += 1
        new = {}
        for k, p in params.items():
            p = np.asarray(p, dtype=float)
            g = np.asarray(grads[k], dtype=float)
            if g.shape != p.shape:
                raise ValueError(f"shape mismatch for {k}")
            if k not in self.m:
                self.m[k] = np.zeros_like(p)
                self.v[k] = np.zeros_like(p)
            self.m[k] = self.beta1 * self.m[k] + (1 - self.beta1) * g
            self.v[k] = self.beta2 * self.v[k] + (1 - self.beta2) * g * g
            m_hat = self.m[k] / (1 - self.beta1 ** self.t)
            v_hat = self.v[k] / (1 - self.beta2 ** self.t)
            new[k] = p - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        return new
''',
"explanation": r'''
The optimiser keeps per-parameter moment estimates in dictionaries keyed like the parameters and a
single step counter. Bias-corrected moments give an update whose size is about `lr` per
coordinate, independent of the gradient's scale. New arrays are returned so callers' parameters
are never modified in place.
''',
"tests": r'''
import numpy as np


class TestAdam(unittest.TestCase):
    def test_first_step_is_lr_sign(self):
        opt = S.Adam(lr=0.1)
        out = opt.step({"w": np.array([1.0, 1.0, 1.0])}, {"w": np.array([4.0, -0.01, 0.0])})
        np.testing.assert_allclose(out["w"], [0.9, 1.1, 1.0], atol=1e-6)
        self.assertEqual(opt.t, 1)

    def test_matches_reference_recurrence(self):
        opt = S.Adam(lr=0.05, beta1=0.8, beta2=0.99, eps=1e-6)
        p = {"a": np.array([0.5, -1.0])}
        m = v = np.zeros(2)
        ref = p["a"].copy()
        for t, g in enumerate([np.array([1.0, 2.0]), np.array([-0.5, 1.0]), np.array([0.2, 0.2])], 1):
            p = opt.step(p, {"a": g})
            m = 0.8 * m + 0.2 * g
            v = 0.99 * v + 0.01 * g * g
            ref = ref - 0.05 * (m / (1 - 0.8 ** t)) / (np.sqrt(v / (1 - 0.99 ** t)) + 1e-6)
            np.testing.assert_allclose(p["a"], ref, rtol=1e-12)

    def test_scale_invariance(self):
        a, b = S.Adam(lr=0.01), S.Adam(lr=0.01)
        p = {"w": np.array([2.0])}
        pa, pb = dict(p), dict(p)
        for g in (0.3, -0.1, 0.7):
            pa = a.step(pa, {"w": np.array([g])})
            pb = b.step(pb, {"w": np.array([g * 1000])})
        np.testing.assert_allclose(pa["w"], pb["w"], rtol=1e-6)

    def test_minimises_quadratic(self):
        opt = S.Adam(lr=0.1)
        p = {"w": np.array([5.0, -3.0])}
        for _ in range(500):
            p = opt.step(p, {"w": 2 * (p["w"] - np.array([1.0, 2.0]))})
        np.testing.assert_allclose(p["w"], [1.0, 2.0], atol=1e-2)

    def test_does_not_mutate_and_counts_once(self):
        opt = S.Adam()
        params = {"w": np.ones(2), "b": np.zeros(1)}
        opt.step(params, {"w": np.ones(2), "b": np.ones(1)})
        np.testing.assert_array_equal(params["w"], np.ones(2))
        self.assertEqual(opt.t, 1)

    def test_validation(self):
        for kwargs in ({"lr": 0}, {"beta1": 1.0}, {"beta2": -0.1}):
            with self.assertRaises(ValueError):
                S.Adam(**kwargs)
        opt = S.Adam()
        with self.assertRaises(ValueError):
            opt.step({"w": np.ones(2)}, {"b": np.ones(2)})
        with self.assertRaises(ValueError):
            opt.step({"w": np.ones(2)}, {"w": np.ones(3)})
''',
"feedback": [
    ("test_first_step_is_lr_sign", "With bias correction the first step is about `lr * sign(g)`."),
    ("test_matches_reference_recurrence", "Check both moment updates, the bias corrections with the shared `t`, and where eps goes."),
    ("test_scale_invariance", "Divide by `sqrt(v_hat) + eps`, which cancels the gradient's scale."),
    ("test_does_not_mutate_and_counts_once", "Increment `t` once per step call, not once per parameter, and return new arrays."),
    ("test_validation", "Validate the hyperparameters and the keys/shapes of params and grads."),
],
"library": {
"text": r'''
`torch.optim.Adam(parameters, lr=..., betas=(0.9, 0.999), eps=1e-8)` implements the same update
(with ε outside the square root). In PyTorch the optimiser modifies tensors in place after
`loss.backward()`; here the dictionary interface makes each step explicit. The comparison below
runs only when PyTorch is installed.
''',
"optional": ["torch"],
"tests": r'''
try:
    import torch
except ImportError:
    torch = None


@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_matches_torch_adam(self):
        w0 = np.array([0.5, -2.0, 3.0])
        grads = [np.array([1.0, -1.0, 0.5]), np.array([0.2, 0.3, -0.4]), np.array([-1.0, 2.0, 0.0])]
        ours = S.Adam(lr=0.01)
        p = {"w": w0}
        tw = torch.tensor(w0, requires_grad=True)
        topt = torch.optim.Adam([tw], lr=0.01)
        for g in grads:
            p = ours.step(p, {"w": g})
            topt.zero_grad()
            tw.grad = torch.tensor(g)
            topt.step()
        np.testing.assert_allclose(p["w"], tw.detach().numpy(), rtol=1e-7)
''',
},
},
]
