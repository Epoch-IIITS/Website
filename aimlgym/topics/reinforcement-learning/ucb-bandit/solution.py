r"""Reference solution for RL-07 UCB1 Bandit.

UCB first tries every arm once, then adds a confidence bonus that is large for rarely tried arms and
grows slowly with time. The simulation draws rewards from one seeded generator, updates sample
averages, and reports regret against the best arm's true mean.
"""
import math

import numpy as np


def ucb_select(q, n, t, c=2.0):
    q = np.asarray(q, dtype=float)
    n = np.asarray(n)
    zeros = np.flatnonzero(n == 0)
    if zeros.size:
        return int(zeros[0])
    return int(np.argmax(q + c * np.sqrt(math.log(t) / n)))


def run_bandit(means, steps, seed, policy="ucb", epsilon=0.1, c=2.0):
    if policy not in ("ucb", "egreedy"):
        raise ValueError("policy must be 'ucb' or 'egreedy'")
    means = np.asarray(means, dtype=float)
    k = len(means)
    rng = np.random.default_rng(seed)
    q, n = np.zeros(k), np.zeros(k, dtype=int)
    actions, rewards = [], []
    for t in range(1, steps + 1):
        if policy == "ucb":
            a = ucb_select(q, n, t, c)
        elif rng.random() < epsilon:
            a = int(rng.integers(k))
        else:
            a = int(np.argmax(q))
        r = float(rng.random() < means[a])
        n[a] += 1
        q[a] += (r - q[a]) / n[a]
        actions.append(a)
        rewards.append(r)
    regret = steps * float(means.max()) - float(means[actions].sum())
    return {"actions": actions, "rewards": rewards, "regret": regret}
