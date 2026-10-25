r"""Reference solution for FL-08 Seeded Client Sampling.

The per-round seed sequence `[seed, round_idx]` gives an independent, reproducible stream for every
round. Sampling without replacement guarantees distinct clients, and the count rule never returns zero.
"""
import numpy as np


def sample_clients(n_clients, fraction, seed, round_idx):
    if n_clients < 1 or not 0 < fraction <= 1:
        raise ValueError("need n_clients >= 1 and 0 < fraction <= 1")
    m = max(1, round(fraction * n_clients))
    rng = np.random.default_rng([seed, round_idx])
    return np.sort(rng.choice(n_clients, m, replace=False))
