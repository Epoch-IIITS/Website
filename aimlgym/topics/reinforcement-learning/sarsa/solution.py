r"""Reference solution for RL-15 SARSA.

The update bootstraps from the value of the next action actually selected by the ε-greedy policy, so
the learned values reflect the behaviour policy including its exploratory mistakes. The next action is
chosen before the update and then executed.
"""
import numpy as np


def sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma):
    target = r + (0.0 if done else gamma * Q[s2, a2])
    delta = target - Q[s, a]
    Q[s, a] += alpha * delta
    return float(delta)


def sarsa(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100):
    rng = np.random.default_rng(seed)
    Q = np.zeros((n_states, n_actions))

    def eps(state):
        if rng.random() < epsilon:
            return int(rng.integers(n_actions))
        return int(np.argmax(Q[state]))

    returns = []
    for _ in range(episodes):
        s, total = start, 0.0
        a = eps(s)
        for _ in range(max_steps):
            s2, r, done = env_step(s, a)
            a2 = eps(s2) if not done else 0
            sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma)
            total += r
            s, a = s2, a2
            if done:
                break
        returns.append(total)
    return Q, returns
