import numpy as np


class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr, self.beta1, self.beta2, self.eps = lr, beta1, beta2, eps
        self.m, self.v, self.t = {}, {}, 0

    def step(self, params, grads):
        # TODO: validate, increment t, update m, v, apply bias correction
        return {k: np.asarray(p, dtype=float) - self.lr * np.asarray(grads[k]) for k, p in params.items()}
