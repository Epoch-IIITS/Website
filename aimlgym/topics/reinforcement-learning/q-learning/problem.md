# RL-13 · Tabular Q-Learning

**Topic:** Reinforcement Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** RL-05 Epsilon-Greedy Action Selection, RL-02 Gridworld Transition Function, RL-12 TD(0) Prediction

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `q_update(Q, s, a, r, s2, done, alpha, gamma)` → updates `Q` in place and returns the TD error.
* `q_learning(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100)`
  → `(Q, episode_returns)` following the recipe; `env_step(s, a)` returns `(s2, r, done)`;
  `episode_returns` holds the undiscounted reward sum per episode.

**Example**
```python
# 1-D corridor: states 0..3, action 1 moves right, 0 moves left; reaching 3 gives +10 and ends.
Q, rets = q_learning(corridor_step, 0, 4, 2, episodes=300, alpha=0.5, gamma=0.9, epsilon=0.1, seed=0)
Q[:3].argmax(axis=1)     # [1, 1, 1]
```

## Hints

<details><summary>Hint 1</summary>

`target = r + (0 if done else gamma * Q[s2].max())`.

</details>

<details><summary>Hint 2</summary>

ε-greedy: `if rng.random() < epsilon: a = int(rng.integers(n_actions)) else: a = int(np.argmax(Q[s]))`.

</details>

<details><summary>Hint 3</summary>

Accumulate `total += r` per episode; break when done.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_update` | Target = r + γ·max_a' Q(s', a'); Q += α·(target − Q). |
| `test_update_terminal` | When done, the target is just r. |
| `test_corridor_values` | Q-learning bootstraps from the greedy max even while exploring. |
| `test_grid_avoids_pit` | Use one seeded generator for ε-greedy decisions across all episodes. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The update moves Q(s, a) towards the reward plus the discounted value of the best next action
(off-policy target). The loop explores with ε-greedy behaviour from one seeded generator, applies an
update after every step, and records each episode's total reward.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
