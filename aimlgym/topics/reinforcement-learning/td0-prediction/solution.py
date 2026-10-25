r"""Reference solution for RL-12 TD(0) Prediction.

The TD error compares the one-step bootstrapped target with the current estimate; the value moves a
fraction α towards the target. Processing transitions in order with in-place updates is online TD(0).
"""
import numpy as np


def td_error(V, s, r, s_next, done, gamma):
    target = r + (0.0 if done else gamma * V[s_next])
    return float(target - V[s])


def td0(episodes, n_states, alpha, gamma, sweeps=1):
    if not 0 < alpha <= 1 or not 0 <= gamma <= 1:
        raise ValueError("need 0 < alpha <= 1 and 0 <= gamma <= 1")
    V = np.zeros(n_states)
    for _ in range(sweeps):
        for ep in episodes:
            for s, r, s2, done in ep:
                V[s] += alpha * td_error(V, s, r, s2, done, gamma)
    return V
