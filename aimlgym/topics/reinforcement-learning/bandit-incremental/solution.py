r"""Reference solution for RL-06 Incremental Value Estimates.

Incrementing the count before computing 1/n makes the first update replace the initial zero with the
first reward, and later updates reproduce the running mean exactly. A constant α instead gives an
exponentially weighted average.
"""
import numpy as np


class ValueEstimates:
    def __init__(self, n_actions, alpha=None):
        if alpha is not None and not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        self.q = np.zeros(n_actions)
        self.n = np.zeros(n_actions, dtype=int)
        self.alpha = alpha

    def update(self, a, r):
        if not 0 <= a < len(self.q):
            raise ValueError("invalid action")
        self.n[a] += 1
        step = 1.0 / self.n[a] if self.alpha is None else self.alpha
        self.q[a] += step * (r - self.q[a])
        return float(self.q[a])
