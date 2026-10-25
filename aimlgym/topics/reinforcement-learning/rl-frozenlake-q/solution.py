r"""Reference solution for RL-14 Q-Learning on FrozenLake.

Decaying epsilon spends the early episodes exploring, and random tie-breaking avoids getting stuck on
action 0 while all values are equal. The update bootstraps only from non-terminal states. Evaluation
turns exploration off and counts how often the greedy policy reaches the goal.
"""
import numpy as np


def q_learning(env, episodes, alpha=0.1, gamma=0.99, eps_min=0.05, seed=0):
    if episodes < 1:
        raise ValueError("episodes must be at least 1")
    n_states, n_actions = env.observation_space.n, env.action_space.n
    Q = np.zeros((n_states, n_actions))
    rng = np.random.default_rng(seed)
    for ep in range(episodes):
        eps = max(eps_min, 1 - ep / (0.7 * episodes))
        obs, _ = env.reset(seed=seed + ep)
        done = False
        while not done:
            if rng.random() < eps:
                a = int(rng.integers(n_actions))
            else:
                q = Q[obs]
                a = int(rng.choice(np.flatnonzero(q == q.max())))
            next_obs, r, terminated, truncated, _ = env.step(a)
            target = r + (0.0 if terminated else gamma * Q[next_obs].max())
            Q[obs, a] += alpha * (target - Q[obs, a])
            obs, done = next_obs, terminated or truncated
    return Q


def success_rate(env, Q, episodes=200, seed=10000):
    wins = 0.0
    for i in range(episodes):
        obs, _ = env.reset(seed=seed + i)
        done = False
        while not done:
            obs, r, terminated, truncated, _ = env.step(int(np.argmax(Q[obs])))
            done = terminated or truncated
        wins += r
    return wins / episodes
