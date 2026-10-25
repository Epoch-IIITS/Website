# RL-09 · Value Iteration

**Topic:** Reinforcement Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** RL-08 Iterative Policy Evaluation

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `q_from_v(P, V, gamma)` → array `(n_states, n_actions)` of one-step lookahead values (all states
  have the same action set).
* `value_iteration(P, gamma=0.9, theta=1e-10, max_iter=10000)` → `(V, policy)` where `policy` is an
  int array of greedy actions (ties → lowest). Synchronous updates.

**Example**
```python
g = GridWorld(["S..G", ".#.X"])     # from RL-02 (provide your own copy or use P directly)
V, pi = value_iteration(g.build_P(), gamma=0.9)
pi[0], pi[1], pi[2]                 # (1, 1, 1)  — go right towards G
```

## Hints

<details><summary>Hint 1</summary>

`nA = len(P[0])`; `Q = np.zeros((nS, nA))`.

</details>

<details><summary>Hint 2</summary>

`Q[s, a] = sum(p * (r + gamma * (0 if d else V[s2])) for p, s2, r, d in P[s][a])`.

</details>

<details><summary>Hint 3</summary>

Loop: `Q = q_from_v(P, V, gamma); new = Q.max(axis=1)`; policy = `q_from_v(P, V, gamma).argmax(axis=1)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_grid_values` | V(s) = max_a Σ p[r + γ(1−done)V(s')]. |
| `test_q_from_v` | Sum over outcomes weighted by probability; terminal outcomes don't bootstrap. |
| `test_avoids_pit` | The greedy policy uses argmax over actions of Q. |
| `test_ties_lowest` | np.argmax gives the lowest action on ties. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The lookahead helper computes Q from V for every state–action pair. Each sweep replaces V with the
row-wise maximum of Q; after convergence, argmax of Q gives the optimal greedy policy with the
lowest-index tie-break.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
