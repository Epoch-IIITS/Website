r"""Reference solution for DL-16 The Adam Optimiser.

The optimiser keeps per-parameter moment estimates in dictionaries keyed like the parameters and a
single step counter. Bias-corrected moments give an update whose size is about `lr` per
coordinate, independent of the gradient's scale. New arrays are returned so callers' parameters
are never modified in place.
"""
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
