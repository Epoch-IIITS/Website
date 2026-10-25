r"""Reference solution for DL-08 A Tiny Autograd Engine.

Every operation stores its inputs and a closure implementing its local chain-rule step.
`backward` performs a depth-first search to list nodes after their children, seeds the output
gradient with 1 and runs the closures from the output back to the leaves. Accumulating with `+=`
handles values that are used several times. Derived operations (`-`, subtraction, reflected
operators) are built from `+` and `*`, so they need no backward rule of their own.
"""
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
