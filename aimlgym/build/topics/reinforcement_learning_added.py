"""Reinforcement Learning step added in the 2026-10 revision: a Gymnasium-style environment
interface, taught before any algorithm interacts with an environment."""

PROBLEMS = [
# ---------------------------------------------------------------- env-interface
{
"slug": "env-interface", "title": "The Environment Interface: reset and step",
"difficulty": "beginner", "prereqs": ["gridworld-step"], "packages": ["numpy"],
"objectives": ["Implement reset() and step() with the Gymnasium return signature",
               "Distinguish terminated (the task ended) from truncated (a time limit hit)",
               "Make stochastic environments reproducible with a seed passed to reset",
               "Run an episode loop with any policy function"],
"tags": ["environments", "gymnasium-api", "episodes", "termination", "truncation"],
"sources": ["S099", "S033", "S035"], "entry": "class LineWorld(n=5, start=0, slip=0.0, max_steps=20); run_episode(env, policy, seed=None)",
"article": r'''
# The Environment Interface: reset and step

## Intuition
Every reinforcement-learning algorithm talks to its world through the same two calls:
**reset** starts a new episode and returns the first observation; **step(action)** applies one
action and reports what happened. If an environment follows this interface, any agent can be
plugged into it — which is why the Gymnasium library standardised it.

## Precise explanation
The Gymnasium-style signatures used here:
```python
obs, info = env.reset(seed=None)
obs, reward, terminated, truncated, info = env.step(action)
```
* `terminated` — the episode ended *inside the task* (goal reached, game over). Future rewards are
  0, so learning algorithms stop bootstrapping here.
* `truncated` — the episode was cut off from outside, e.g. a **time limit**. The state is not
  terminal, so value estimates should still look ahead. Mixing the two up biases learning.
* `info` — a dict of diagnostics (here, the step count).
* **Seeding**: `reset(seed=s)` re-creates the environment's random generator
  (`np.random.default_rng(s)`), so the same seed and actions reproduce the same episode.
  `reset()` without a seed keeps using the existing generator.
* Calling `step` after the episode is over is an error; call `reset` first.

**The episode loop**
```python
obs, info = env.reset(seed=0)
total, done = 0.0, False
while not done:
    obs, r, terminated, truncated, info = env.step(policy(obs))
    total += r
    done = terminated or truncated
```

## Worked example
`LineWorld(n=5, start=0)`: states 0..4, goal 4, actions 0 = left and 1 = right, reward 1 on
reaching the goal and 0 otherwise. Always moving right terminates after 4 steps with total
reward 1. Always moving left hits the wall at 0 until the 20-step limit truncates the episode.

## Common mistakes
* Returning a single `done` flag and losing the terminated/truncated distinction.
* Creating a new random generator on every `step`, so the seed has no effect.
* Forgetting to reset the step counter in `reset`.

## Why this matters
Bandits, Monte Carlo, TD and Q-learning later in this topic all consume episodes through this
interface, and Gymnasium environments for CartPole or Atari work the same way.
''',
"statement": r'''
Write `class LineWorld(n=5, start=0, slip=0.0, max_steps=20)`:

* States are `0 .. n-1`; the goal is `n - 1`. Validate `n >= 2`, `0 <= start < n - 1`,
  `0 <= slip <= 1`, `max_steps >= 1` (else `ValueError`).
* `reset(seed=None)` → `(start, {"steps": 0})`. If `seed` is given, set
  `self.rng = np.random.default_rng(seed)`; the constructor creates one with seed 0.
* `step(action)` with action 0 (left) or 1 (right), else `ValueError`. If the episode is over,
  raise `RuntimeError`. With probability `slip` the action is reversed — draw
  `self.rng.random() < self.slip` **once per step, only when `slip > 0`**. Moves are clipped to
  `[0, n-1]`. Reward `1.0` when the new state is the goal, else `0.0`. `terminated` when at the
  goal; `truncated` when the step count reaches `max_steps` and not terminated. Return
  `(state, reward, terminated, truncated, {"steps": count})`.

And `run_episode(env, policy, seed=None)` → `(total_reward, steps, terminated)` using the loop
above (`policy(obs)` returns an action).
''',
"starter": r'''
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
''',
"hints": [
    "Keep `self.done` and `self.steps`; set them in `reset` and check `self.done` at the start of `step`.",
    "`move = 1 if action == 1 else -1`; if `self.slip > 0 and self.rng.random() < self.slip`, flip it; then `max(0, min(self.n - 1, self.state + move))`.",
    "`terminated = self.state == self.n - 1`; `truncated = not terminated and self.steps >= self.max_steps`; `self.done = terminated or truncated`.",
],
"solution": r'''
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
''',
"explanation": r'''
The environment keeps its own state, step counter, done flag and random generator. `reset`
restores the start and optionally re-seeds; `step` validates, applies the (possibly slipped) move,
and computes termination and truncation separately so a time limit is never mistaken for reaching
the goal. `run_episode` is the standard loop and works with any policy function.
''',
"tests": r'''
import numpy as np

RIGHT = lambda obs: 1
LEFT = lambda obs: 0


class TestLineWorld(unittest.TestCase):
    def test_reset(self):
        env = S.LineWorld(n=5, start=1)
        self.assertEqual(env.reset(), (1, {"steps": 0}))

    def test_reach_goal(self):
        env = S.LineWorld()
        env.reset()
        out = [env.step(1) for _ in range(4)]
        self.assertEqual(out[-1], (4, 1.0, True, False, {"steps": 4}))
        self.assertEqual([o[1] for o in out[:-1]], [0.0, 0.0, 0.0])

    def test_wall_and_truncation(self):
        env = S.LineWorld(max_steps=3)
        env.reset()
        results = [env.step(0) for _ in range(3)]
        self.assertEqual([r[0] for r in results], [0, 0, 0])
        self.assertEqual(results[-1][2:4], (False, True))
        with self.assertRaises(RuntimeError):
            env.step(0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            S.LineWorld(n=1)
        with self.assertRaises(ValueError):
            S.LineWorld(start=4)
        env = S.LineWorld()
        env.reset()
        with self.assertRaises(ValueError):
            env.step(2)

    def test_run_episode(self):
        self.assertEqual(S.run_episode(S.LineWorld(), RIGHT), (1.0, 4, True))
        self.assertEqual(S.run_episode(S.LineWorld(max_steps=7), LEFT), (0.0, 7, False))

    def test_slip_reproducible(self):
        env = S.LineWorld(n=6, slip=0.3, max_steps=50)
        a = [S.run_episode(env, RIGHT, seed=5) for _ in range(2)]
        self.assertEqual(a[0], a[1])
        rng = np.random.default_rng(5)
        state, steps = 0, 0
        while state != 5 and steps < 50:
            move = -1 if rng.random() < 0.3 else 1
            state = max(0, min(5, state + move))
            steps += 1
        self.assertEqual(a[0][1], steps)

    def test_reset_restarts_episode(self):
        env = S.LineWorld(max_steps=2)
        S.run_episode(env, LEFT)
        obs, info = env.reset()
        self.assertEqual((obs, info["steps"]), (0, 0))
        self.assertEqual(env.step(1)[0], 1)
''',
"feedback": [
    ("test_reach_goal", "Reward 1.0 and terminated=True exactly when the new state is n - 1."),
    ("test_wall_and_truncation", "Clip moves at the walls; truncate when steps reach max_steps; refuse to step after the end."),
    ("test_validation", "Check the constructor arguments and the action value."),
    ("test_slip_reproducible", "Re-seed in `reset(seed)` and draw one `rng.random()` per step only when slip > 0."),
    ("test_reset_restarts_episode", "Reset the state, the step counter and the done flag."),
],
"library": {
"text": r'''
Gymnasium defines this interface as `gymnasium.Env` with `reset(seed=..., options=...)` and
`step(action)` returning the same five values, plus `action_space` / `observation_space` objects
(`spaces.Discrete(2)` here) and wrappers such as `TimeLimit`, which produces exactly the
truncation you implemented. Gymnasium is not needed for this course; the same agent code would
run on `gymnasium.make("CartPole-v1")` once installed.
''',
},
},
]
