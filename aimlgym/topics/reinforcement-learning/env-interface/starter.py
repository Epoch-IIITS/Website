import numpy as np


class LineWorld:
    def __init__(self, n=5, start=0, slip=0.0, max_steps=20):
        self.n, self.start, self.slip, self.max_steps = n, start, slip, max_steps
        self.rng = np.random.default_rng(0)
        self.state = start
        self.steps = 0

    def reset(self, seed=None):
        # TODO
        return self.start, {}

    def step(self, action):
        # TODO
        self.state = min(self.state + 1, self.n - 1)
        return self.state, 0.0, False, False, {}


def run_episode(env, policy, seed=None):
    # TODO
    return 0.0, 0, False
