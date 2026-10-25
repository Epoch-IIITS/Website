import gymnasium as gym
from gymnasium import spaces
from gymnasium.wrappers import TimeLimit


class LineWorldEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(self, n=5, slip=0.0):
        # TODO
        pass

    def reset(self, *, seed=None, options=None):
        # TODO
        pass

    def step(self, action):
        # TODO
        pass


def make_lineworld(n=5, slip=0.0, max_steps=20):
    # TODO
    pass
