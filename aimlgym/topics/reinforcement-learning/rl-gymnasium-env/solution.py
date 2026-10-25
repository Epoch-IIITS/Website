r"""Reference solution for RL-04 Gymnasium Environments.

The spaces document the interface; `super().reset(seed=...)` sets up `self.np_random`, which drives
every random slip, so seeds reproduce episodes. The environment reports only termination; the
TimeLimit wrapper adds truncation.
"""
import gymnasium as gym
from gymnasium import spaces
from gymnasium.wrappers import TimeLimit


class LineWorldEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, n=5, slip=0.0):
        if n < 2 or not 0 <= slip <= 1:
            raise ValueError("need n >= 2 and 0 <= slip <= 1")
        self.n, self.slip = n, slip
        self.observation_space = spaces.Discrete(n)
        self.action_space = spaces.Discrete(2)
        self.state = 0

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.state = 0
        return self.state, {}

    def step(self, action):
        if not self.action_space.contains(action):
            raise ValueError("action must be 0 or 1")
        if self.slip > 0 and self.np_random.random() < self.slip:
            action = 1 - action
        self.state = int(min(max(self.state + (1 if action == 1 else -1), 0), self.n - 1))
        terminated = self.state == self.n - 1
        return self.state, 1.0 if terminated else 0.0, terminated, False, {}


def make_lineworld(n=5, slip=0.0, max_steps=20):
    return TimeLimit(LineWorldEnv(n, slip), max_episode_steps=max_steps)
