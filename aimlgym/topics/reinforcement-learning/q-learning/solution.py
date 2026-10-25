r"""Reference solution for RL-13 Tabular Q-Learning.

The update moves Q(s, a) towards the reward plus the discounted value of the best next action
(off-policy target). The loop explores with ε-greedy behaviour from one seeded generator, applies an
update after every step, and records each episode's total reward.
"""
import numpy as np


def q_update(Q, s, a, r, s2, done, alpha, gamma):
    target = r + (0.0 if done else gamma * float(np.max(Q[s2])))
    delta = target - Q[s, a]
    Q[s, a] += alpha * delta
    return float(delta)


def q_learning(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100):
    rng = np.random.default_rng(seed)
    Q = np.zeros((n_states, n_actions))
    returns = []
    for _ in range(episodes):
        s, total = start, 0.0
        for _ in range(max_steps):
            if rng.random() < epsilon:
                a = int(rng.integers(n_actions))
            else:
                a = int(np.argmax(Q[s]))
            s2, r, done = env_step(s, a)
            q_update(Q, s, a, r, s2, done, alpha, gamma)
            total += r
            s = s2
            if done:
                break
        returns.append(total)
    return Q, returns
