r"""Reference solution for RL-05 Epsilon-Greedy Action Selection.

One uniform draw decides between exploring and exploiting; exploration samples any action uniformly,
including the greedy one. The probability vector follows directly from that procedure.
"""
import numpy as np


def _check(q_values, epsilon):
    q = np.asarray(q_values, dtype=float)
    if q.size == 0 or not 0 <= epsilon <= 1:
        raise ValueError("need non-empty q_values and 0 <= epsilon <= 1")
    return q


def epsilon_greedy(q_values, epsilon, rng):
    q = _check(q_values, epsilon)
    if rng.random() < epsilon:
        return int(rng.integers(len(q)))
    return int(np.argmax(q))


def epsilon_greedy_probs(q_values, epsilon):
    q = _check(q_values, epsilon)
    p = np.full(len(q), epsilon / len(q))
    p[int(np.argmax(q))] += 1 - epsilon
    return p
