r"""Reference solution for DL-14 SGD with Momentum.

Velocity arrays persist inside the optimiser, one per parameter name. Each step blends the old
velocity with the new gradient and moves the parameter against the velocity, returning fresh
arrays so caller data is never mutated.
"""
import numpy as np


class Momentum:
    def __init__(self, lr=0.01, beta=0.9):
        if lr <= 0 or not 0 <= beta < 1:
            raise ValueError("lr must be > 0 and 0 <= beta < 1")
        self.lr = lr
        self.beta = beta
        self.v = {}

    def step(self, params, grads):
        if set(params) != set(grads):
            raise ValueError("params and grads must have the same keys")
        new = {}
        for k, p in params.items():
            g = np.asarray(grads[k], dtype=float)
            p = np.asarray(p, dtype=float)
            if g.shape != p.shape:
                raise ValueError(f"shape mismatch for {k}")
            if k not in self.v:
                self.v[k] = np.zeros_like(p)
            self.v[k] = self.beta * self.v[k] + g
            new[k] = p - self.lr * self.v[k]
        return new
