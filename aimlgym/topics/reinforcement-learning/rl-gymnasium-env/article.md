# Gymnasium Environments

## Learning outcomes

After this lesson you can:

- Write an environment as a gymnasium.Env subclass with observation and action spaces
- Use the seeded self.np_random generator through super().reset(seed=seed)
- Add a time limit with the TimeLimit wrapper and validate the environment with check_env

## Intuition
Your `LineWorld` in RL-03 followed the reset/step contract by convention. Gymnasium makes
it official: subclass `gymnasium.Env`, declare what observations and actions look like, and every
Gymnasium tool — wrappers, checkers, vectorised runners, and RL libraries — works with your environment.

## Precise explanation
```python
import gymnasium as gym
from gymnasium import spaces

class LineWorldEnv(gym.Env):
    def __init__(self, n=5, slip=0.0):
        self.observation_space = spaces.Discrete(n)     # states 0 .. n-1
        self.action_space = spaces.Discrete(2)          # 0 = left, 1 = right

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)                        # (re)seeds self.np_random
        return 0, {}

    def step(self, action):
        ...
        return obs, reward, terminated, False, {}
```

* **Spaces** describe valid values: `Discrete(n)` is {0, …, n−1}; `Box` is for real-valued vectors.
  `space.contains(x)` checks a value and `space.sample()` draws a random one.
* `super().reset(seed=seed)` creates `self.np_random`, a NumPy generator; use it for every random
  choice so a seed reproduces an episode.
* Time limits belong in a **wrapper**: `gymnasium.wrappers.TimeLimit(env, max_episode_steps=20)` sets
  `truncated=True` after 20 steps, so the environment itself only reports `terminated`.
* `gymnasium.utils.env_checker.check_env(env)` checks the API: return types, spaces, seeding.
* Built-in environments are created with `gym.make("FrozenLake-v1")`, used in the next step.

## Worked example
`make_lineworld(n=5, max_steps=6)`: moving right four times terminates with reward 1; moving left six
times returns `truncated=True` from the wrapper. With `slip=0.5` and seed 3, two runs with the same
actions produce the same states.

## Common mistakes
* Using `random` or a module-level NumPy generator instead of `self.np_random`.
* Putting the step limit inside the environment and also wrapping it.
* Returning NumPy integers outside the declared space, or forgetting the `info` dict.

## Why this matters
Q-learning on FrozenLake next, and the grid-game project idea, use this interface; so do libraries such
as Stable-Baselines3 for larger problems.

## References

- [Gymnasium Env API](https://gymnasium.farama.org/api/env/) — Farama Foundation (`S099`)
- [Gymnasium Documentation](https://gymnasium.farama.org/) — Farama Foundation (`S035`)
