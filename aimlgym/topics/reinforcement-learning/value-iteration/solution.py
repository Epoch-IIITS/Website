r"""Reference solution for RL-09 Value Iteration.

The lookahead helper computes Q from V for every state–action pair. Each sweep replaces V with the
row-wise maximum of Q; after convergence, argmax of Q gives the optimal greedy policy with the
lowest-index tie-break.
"""
import numpy as np


def q_from_v(P, V, gamma):
    nS, nA = len(P), len(P[0])
    Q = np.zeros((nS, nA))
    for s in range(nS):
        for a in range(nA):
            Q[s, a] = sum(p * (r + gamma * (0.0 if d else V[s2])) for p, s2, r, d in P[s][a])
    return Q


def value_iteration(P, gamma=0.9, theta=1e-10, max_iter=10000):
    if not 0 <= gamma < 1:
        raise ValueError("gamma must be in [0, 1)")
    V = np.zeros(len(P))
    for _ in range(max_iter):
        new = q_from_v(P, V, gamma).max(axis=1)
        delta = float(np.max(np.abs(new - V)))
        V = new
        if delta < theta:
            break
    return V, q_from_v(P, V, gamma).argmax(axis=1)
