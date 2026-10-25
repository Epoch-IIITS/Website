r"""Reference solution for DL-23 Batch Normalization by Hand (train/eval).

Training mode normalises with the batch's own statistics and updates exponential running
averages (unbiased variance). Evaluation mode normalises with the stored averages and leaves
state untouched, so outputs no longer depend on the other examples in the batch.
"""
import numpy as np


class BatchNorm1d:
    def __init__(self, n_features, momentum=0.1, eps=1e-5):
        self.n_features = n_features
        self.momentum = momentum
        self.eps = eps
        self.gamma = np.ones(n_features)
        self.beta = np.zeros(n_features)
        self.running_mean = np.zeros(n_features)
        self.running_var = np.ones(n_features)

    def forward(self, x, training=True):
        x = np.asarray(x, dtype=float)
        if x.ndim != 2 or x.shape[1] != self.n_features:
            raise ValueError("x must have shape (n, n_features)")
        if training:
            n = x.shape[0]
            if n < 2:
                raise ValueError("batch size must be >= 2 in training mode")
            mu = x.mean(axis=0)
            var = x.var(axis=0)
            m = self.momentum
            self.running_mean = (1 - m) * self.running_mean + m * mu
            self.running_var = (1 - m) * self.running_var + m * var * n / (n - 1)
        else:
            mu, var = self.running_mean, self.running_var
        x_hat = (x - mu) / np.sqrt(var + self.eps)
        return self.gamma * x_hat + self.beta
