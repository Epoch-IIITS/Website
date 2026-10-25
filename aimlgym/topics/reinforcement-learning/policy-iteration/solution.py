r"""Reference solution for RL-10 Policy Iteration.

Each cycle evaluates the current deterministic policy to convergence, then acts greedily with respect
to the resulting values. Because ties resolve to the lowest action, an unchanged argmax means the
policy is stable and therefore optimal.
"""
import numpy as np


def _q(P, V, gamma):
    nS, nA = len(P), len(P[0])
    Q = np.zeros((nS, nA))
    for s in range(nS):
        for a in range(nA):
            Q[s, a] = sum(p * (r + gamma * (0.0 if d else V[s2])) for p, s2, r, d in P[s][a])
    return Q


def _evaluate(P, pi, gamma, theta, max_sweeps=100000):
    nS = len(P)
    V = np.zeros(nS)
    for _ in range(max_sweeps):
        new = np.array([sum(p * (r + gamma * (0.0 if d else V[s2])) for p, s2, r, d in P[s][int(pi[s])])
                        for s in range(nS)])
        delta = float(np.max(np.abs(new - V)))
        V = new
        if delta < theta:
            break
    return V


def policy_iteration(P, gamma=0.9, theta=1e-10, max_iter=100):
    if not 0 <= gamma < 1:
        raise ValueError("gamma must be in [0, 1)")
    pi = np.zeros(len(P), dtype=int)
    for k in range(1, max_iter + 1):
        V = _evaluate(P, pi, gamma, theta)
        new_pi = _q(P, V, gamma).argmax(axis=1)
        if np.array_equal(new_pi, pi):
            return V, pi, k
        pi = new_pi
    return V, pi, max_iter
