# RL-15 · SARSA

**Topic:** Reinforcement Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** RL-13 Tabular Q-Learning

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `sarsa_update(Q, s, a, r, s2, a2, done, alpha, gamma)` → updates in place, returns the TD error.
* `sarsa(env_step, start, n_states, n_actions, episodes, alpha, gamma, epsilon, seed, max_steps=100)`
  → `(Q, episode_returns)` following the recipe.

**Example**
```python
Q = np.zeros((2, 2)); Q[1] = [5., 2.]
sarsa_update(Q, 0, 1, -1.0, 1, 1, False, 0.5, 0.9); Q[0, 1]   # 0.4
```

## Hints

<details><summary>Hint 1</summary>

`target = r + (0 if done else gamma * Q[s2, a2])`.

</details>

<details><summary>Hint 2</summary>

Write an inner `eps(state)` using the shared rng.

</details>

<details><summary>Hint 3</summary>

Choose `a2` before calling `sarsa_update`, then set `s, a = s2, a2`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_update` | SARSA's target uses Q(s', a') for the next action actually chosen, not the max. |
| `test_update_terminal` | No bootstrapping when done. |
| `test_cliff_safe_path_vs_qlearning` | Choose a' with ε-greedy before updating and carry it forward; SARSA should learn the safe path. |
| `test_reproducible` | Use one seeded generator for all action choices. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The update bootstraps from the value of the next action actually selected by the ε-greedy policy, so
the learned values reflect the behaviour policy including its exploratory mistakes. The next action is
chosen before the update and then executed.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
