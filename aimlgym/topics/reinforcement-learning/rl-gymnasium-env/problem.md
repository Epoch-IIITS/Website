# RL-04 · Gymnasium Environments

**Topic:** Reinforcement Learning · **Difficulty:** beginner · **Allowed packages:** numpy, gymnasium

**Builds on:** RL-03 The Environment Interface: reset and step

Read the lesson first: [article.md](article.md)

## Task

1. `class LineWorldEnv(gym.Env)` with `__init__(self, n=5, slip=0.0)` (raise `ValueError` unless
   `n >= 2` and `0 <= slip <= 1`), `observation_space = spaces.Discrete(n)` and
   `action_space = spaces.Discrete(2)`.
   * `reset(self, *, seed=None, options=None)`: call `super().reset(seed=seed)`, set the state to 0 and
     return `(0, {})`.
   * `step(self, action)`: raise `ValueError` if the action is not in the action space. When `slip > 0`,
     reverse the action if `self.np_random.random() < self.slip`. Move left (0) or right (1), clipped to
     `[0, n - 1]`. Return `(state, reward, terminated, False, {})` with reward `1.0` and
     `terminated=True` at state `n - 1`, else `0.0` and `False`. States are Python ints.
2. `make_lineworld(n=5, slip=0.0, max_steps=20)` returns `TimeLimit(LineWorldEnv(n, slip), max_episode_steps=max_steps)`.

## Hints

<details><summary>Hint 1</summary>

Validate the arguments, then create the two `spaces.Discrete` objects.

</details>

<details><summary>Hint 2</summary>

`self.action_space.contains(action)` checks the action; draw the slip with `self.np_random.random()`.

</details>

<details><summary>Hint 3</summary>

`min(max(self.state + step, 0), self.n - 1)` keeps the state on the line.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_check_env` | Subclass gym.Env, define both spaces and return (obs, info) from reset. |
| `test_time_limit_truncates` | Wrap the environment with TimeLimit(env, max_episode_steps=max_steps). |
| `test_seeded_slip_reproducible` | Call super().reset(seed=seed) and draw slips from self.np_random. |
| `test_invalid` | Validate the constructor arguments and reject actions outside the action space. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The spaces document the interface; `super().reset(seed=...)` sets up `self.np_random`, which drives
every random slip, so seeds reproduce episodes. The environment reports only termination; the
TimeLimit wrapper adds truncation.

## References

- [Gymnasium Env API](https://gymnasium.farama.org/api/env/) — Farama Foundation (`S099`)
- [Gymnasium Documentation](https://gymnasium.farama.org/) — Farama Foundation (`S035`)
