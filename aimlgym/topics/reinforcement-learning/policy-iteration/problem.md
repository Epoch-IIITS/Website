# RL-10 · Policy Iteration

**Topic:** Reinforcement Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** RL-08 Iterative Policy Evaluation, RL-09 Value Iteration

Read the lesson first: [article.md](article.md)

## Task

Write `policy_iteration(P, gamma=0.9, theta=1e-10, max_iter=100)` returning `(V, policy, n_improvements)`
where `policy` is an int array and `n_improvements` the number of evaluate-improve cycles performed
(including the final one where the policy did not change). Include your own policy evaluation and
lookahead helpers. Raise `ValueError` if `gamma` not in `[0, 1)`.

**Example**
```python
V, pi, k = policy_iteration(grid_P(["S..G", ".#.X"]), gamma=0.9)
pi[:3]     # [1, 1, 1]
```

## Hints

<details><summary>Hint 1</summary>

Deterministic policy matrix: `pm = np.zeros((nS, nA)); pm[np.arange(nS), pi] = 1`.

</details>

<details><summary>Hint 2</summary>

Evaluate synchronously until max change < theta; compute Q from V.

</details>

<details><summary>Hint 3</summary>

`new_pi = Q.argmax(axis=1)`; stop when `np.array_equal(new_pi, pi)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_matches_value_iteration` | Evaluate the current policy fully before improving. |
| `test_stochastic` | Lookahead must weight outcomes by probability and stop bootstrapping at done. |
| `test_already_optimal_one_cycle` | Count the final cycle in which the policy did not change. |
| `test_grid` | Improvement is argmax over actions of Q computed from V^π. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each cycle evaluates the current deterministic policy to convergence, then acts greedily with respect
to the resulting values. Because ties resolve to the lowest action, an unchanged argmax means the
policy is stable and therefore optimal.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
- [Dive into Deep Learning — Reinforcement Learning chapter](https://d2l.ai/chapter_reinforcement-learning/index.html) — Pratik Chaudhari, Rasool Fakoor, Kavosh Asadi (D2L) (`S034`)
