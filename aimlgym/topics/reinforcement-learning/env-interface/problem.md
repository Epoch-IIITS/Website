# RL-03 · The Environment Interface: reset and step

**Topic:** Reinforcement Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** RL-02 Gridworld Transition Function

Read the lesson first: [article.md](article.md)

## Task

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

## Hints

<details><summary>Hint 1</summary>

Keep `self.done` and `self.steps`; set them in `reset` and check `self.done` at the start of `step`.

</details>

<details><summary>Hint 2</summary>

`move = 1 if action == 1 else -1`; if `self.slip > 0 and self.rng.random() < self.slip`, flip it; then `max(0, min(self.n - 1, self.state + move))`.

</details>

<details><summary>Hint 3</summary>

`terminated = self.state == self.n - 1`; `truncated = not terminated and self.steps >= self.max_steps`; `self.done = terminated or truncated`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_reach_goal` | Reward 1.0 and terminated=True exactly when the new state is n - 1. |
| `test_wall_and_truncation` | Clip moves at the walls; truncate when steps reach max_steps; refuse to step after the end. |
| `test_validation` | Check the constructor arguments and the action value. |
| `test_slip_reproducible` | Re-seed in `reset(seed)` and draw one `rng.random()` per step only when slip > 0. |
| `test_reset_restarts_episode` | Reset the state, the step counter and the done flag. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The environment keeps its own state, step counter, done flag and random generator. `reset`
restores the start and optionally re-seeds; `step` validates, applies the (possibly slipped) move,
and computes termination and truncation separately so a time limit is never mistaken for reaching
the goal. `run_episode` is the standard loop and works with any policy function.

## References

- [Gymnasium Env API](https://gymnasium.farama.org/api/env/) — Farama Foundation (`S099`)
- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Gymnasium Documentation](https://gymnasium.farama.org/) — Farama Foundation (`S035`)
