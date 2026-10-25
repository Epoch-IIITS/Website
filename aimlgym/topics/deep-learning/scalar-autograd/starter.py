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
