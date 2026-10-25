r"""Reference solution for RL-11 First-Visit Monte Carlo Prediction.

A backward pass gives the return at every time step. Scanning forward, the first-visit rule skips
repeated states within an episode. Running sums and counts produce averages; unvisited states stay 0.
"""
import numpy as np


def mc_prediction(episodes, n_states, gamma, first_visit=True):
    if not 0 <= gamma <= 1:
        raise ValueError("gamma must be in [0, 1]")
    sums = np.zeros(n_states)
    counts = np.zeros(n_states, dtype=int)
    for ep in episodes:
        G = 0.0
        returns = [0.0] * len(ep)
        for t in range(len(ep) - 1, -1, -1):
            G = ep[t][1] + gamma * G
            returns[t] = G
        seen = set()
        for t, (s, _) in enumerate(ep):
            if first_visit and s in seen:
                continue
            seen.add(s)
            sums[s] += returns[t]
            counts[s] += 1
    V = np.divide(sums, counts, out=np.zeros(n_states), where=counts > 0)
    return V, counts
