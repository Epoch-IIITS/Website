# RL-14 · Q-Learning on FrozenLake

**Topic:** Reinforcement Learning · **Difficulty:** advanced · **Allowed packages:** numpy, gymnasium

**Builds on:** RL-13 Tabular Q-Learning, RL-04 Gymnasium Environments

Read the lesson first: [article.md](article.md)

## Task

1. `q_learning(env, episodes, alpha=0.1, gamma=0.99, eps_min=0.05, seed=0)` returns a NumPy array
   `Q` of shape `(n_states, n_actions)` from the env's spaces. Use `rng = np.random.default_rng(seed)`.
   For episode `ep`: `eps = max(eps_min, 1 - ep / (0.7 * episodes))`; `obs, _ = env.reset(seed=seed + ep)`;
   until terminated or truncated, explore with probability `eps` (`int(rng.integers(n_actions))`),
   otherwise take a greedy action with random ties (`int(rng.choice(np.flatnonzero(q == q.max())))`);
   then apply the Q-learning update with no bootstrap on termination.
2. `success_rate(env, Q, episodes=200, seed=10000)` runs the greedy policy `int(np.argmax(Q[obs]))` for
   `episodes` episodes (`env.reset(seed=seed + i)`) and returns the fraction with reward 1 at the end.

Raise `ValueError` in `q_learning` if `episodes < 1`.

## Hints

<details><summary>Hint 1</summary>

`n_states, n_actions = env.observation_space.n, env.action_space.n`; `Q = np.zeros((n_states, n_actions))`.

</details>

<details><summary>Hint 2</summary>

`target = r + (0.0 if terminated else gamma * Q[next_obs].max())`; `Q[obs, a] += alpha * (target - Q[obs, a])`.

</details>

<details><summary>Hint 3</summary>

In `success_rate`, add the final reward of each episode and divide by the number of episodes.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_deterministic_lake_solved` | Break ties randomly among maximal actions and decay epsilon. |
| `test_shape_and_terminal_rows` | Do not bootstrap from terminal states; their rows stay at zero. |
| `test_reproducible` | Seed the generator and each env.reset(seed=seed + ep). |
| `test_untrained_policy_fails` | success_rate uses argmax of Q and counts the final reward. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Decaying epsilon spends the early episodes exploring, and random tie-breaking avoids getting stuck on
action 0 while all values are equal. The update bootstraps only from non-terminal states. Evaluation
turns exploration off and counts how often the greedy policy reaches the goal.

## References

- [Frozen Lake (Gymnasium docs)](https://gymnasium.farama.org/environments/toy_text/frozen_lake/) — Farama Foundation (`S141`)
- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
