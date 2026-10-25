# A Tiny Autograd Engine

## Learning outcomes

After this lesson you can:

- Represent a computation as a graph of Value objects
- Give each operation a local backward rule from the chain rule
- Run backpropagation in reverse topological order and accumulate gradients
- Explain what PyTorch's autograd automates

## Intuition
A neural network's loss is built from many small operations: multiply, add, `tanh`, ... If every
operation knows its own derivative, the chain rule (MA-11) lets us compute the
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
DL-10 and DL-11 derive the same gradients by hand for whole arrays;
frameworks do it automatically with exactly this algorithm.

## Library implementation

PyTorch's autograd records the same graph for tensors: create inputs with
`torch.tensor(2.0, requires_grad=True)`, compute, call `loss.backward()`, and read `x.grad`.
It supports thousands of operations and runs on GPUs, but the algorithm — local derivatives
applied in reverse topological order with accumulation — is the one you wrote. The comparison
runs only when PyTorch is installed.

## References

- [micrograd: a tiny scalar-valued autograd engine](https://github.com/karpathy/micrograd) — Andrej Karpathy (`S094`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
- [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) — PyTorch (`S092`)
