# The Environment Interface: reset and step

## Learning outcomes

After this lesson you can:

- Implement reset() and step() with the Gymnasium return signature
- Distinguish terminated (the task ended) from truncated (a time limit hit)
- Make stochastic environments reproducible with a seed passed to reset
- Run an episode loop with any policy function

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

## Library implementation

Gymnasium defines this interface as `gymnasium.Env` with `reset(seed=..., options=...)` and
`step(action)` returning the same five values, plus `action_space` / `observation_space` objects
(`spaces.Discrete(2)` here) and wrappers such as `TimeLimit`, which produces exactly the
truncation you implemented. Gymnasium is not needed for this course; the same agent code would
run on `gymnasium.make("CartPole-v1")` once installed.

## References

- [Gymnasium Env API](https://gymnasium.farama.org/api/env/) — Farama Foundation (`S099`)
- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Gymnasium Documentation](https://gymnasium.farama.org/) — Farama Foundation (`S035`)
