r"""Reference solution for RL-08 Iterative Policy Evaluation.

Each sweep computes, for every state, the policy-weighted expected one-step reward plus discounted
next-state value, using the previous sweep's values. Terminal transitions contribute only their
reward. Iteration stops once values change by less than θ.
"""
import numpy as np


def policy_evaluation(P, policy, gamma=0.9, theta=1e-10, max_iter=10000):
    policy = np.asarray(policy, dtype=float)
    if not 0 <= gamma < 1:
        raise ValueError("gamma must be in [0, 1)")
    if not np.allclose(policy.sum(axis=1), 1.0, atol=1e-8):
        raise ValueError("policy rows must sum to 1")
    n = len(P)
    V = np.zeros(n)
    for it in range(1, max_iter + 1):
        new = np.zeros(n)
        for s in range(n):
            for a, outcomes in P[s].items():
                pa = policy[s, a]
                if pa == 0:
                    continue
                for p, s2, r, done in outcomes:
                    new[s] += pa * p * (r + gamma * (0.0 if done else V[s2]))
        delta = float(np.max(np.abs(new - V)))
        V = new
        if delta < theta:
            return V, it
    return V, max_iter
