r"""Reference solution for RL-03 The Environment Interface: reset and step.

The environment keeps its own state, step counter, done flag and random generator. `reset`
restores the start and optionally re-seeds; `step` validates, applies the (possibly slipped) move,
and computes termination and truncation separately so a time limit is never mistaken for reaching
the goal. `run_episode` is the standard loop and works with any policy function.
"""
import numpy as np


class LineWorld:
    def __init__(self, n=5, start=0, slip=0.0, max_steps=20):
        if n < 2 or not 0 <= start < n - 1 or not 0 <= slip <= 1 or max_steps < 1:
            raise ValueError("invalid LineWorld settings")
        self.n, self.start, self.slip, self.max_steps = n, start, slip, max_steps
        self.rng = np.random.default_rng(0)
        self.state = start
        self.steps = 0
        self.done = False

    def reset(self, seed=None):
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.state = self.start
        self.steps = 0
        self.done = False
        return self.state, {"steps": 0}

    def step(self, action):
        if action not in (0, 1):
            raise ValueError("action must be 0 (left) or 1 (right)")
        if self.done:
            raise RuntimeError("episode is over; call reset()")
        move = 1 if action == 1 else -1
        if self.slip > 0 and self.rng.random() < self.slip:
            move = -move
        self.state = max(0, min(self.n - 1, self.state + move))
        self.steps += 1
        terminated = self.state == self.n - 1
        truncated = not terminated and self.steps >= self.max_steps
        self.done = terminated or truncated
        reward = 1.0 if terminated else 0.0
        return self.state, reward, terminated, truncated, {"steps": self.steps}


def run_episode(env, policy, seed=None):
    obs, _ = env.reset(seed=seed)
    total, terminated, truncated = 0.0, False, False
    while not (terminated or truncated):
        obs, reward, terminated, truncated, info = env.step(policy(obs))
        total += reward
    return total, info["steps"], terminated
