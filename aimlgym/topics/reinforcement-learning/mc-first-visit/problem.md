# RL-11 · First-Visit Monte Carlo Prediction

**Topic:** Reinforcement Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** RL-03 The Environment Interface: reset and step, RL-08 Iterative Policy Evaluation

Read the lesson first: [article.md](article.md)

## Task

Write `mc_prediction(episodes, n_states, gamma, first_visit=True)` returning `(V, counts)` arrays
(`V[s] = 0` and `counts[s] = 0` for unvisited states). Raise `ValueError` for `gamma` outside
`[0, 1]`.

**Example**
```python
eps = [[(0, 1), (1, 0), (0, 2)], [(1, 5)]]
mc_prediction(eps, 2, 1.0)[0]                      # [3. , 3.5]
mc_prediction(eps, 2, 1.0, first_visit=False)[0]   # [2.5, 3.5]
```

## Hints

<details><summary>Hint 1</summary>

For each episode compute `G_t` for all t with a backward pass.

</details>

<details><summary>Hint 2</summary>

First visit: find `first = {}` mapping state → earliest t.

</details>

<details><summary>Hint 3</summary>

Keep `sums[s]` and `counts[s]`; V = sums / counts where counts > 0.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_first_visit` | Only the first occurrence of each state per episode counts. |
| `test_discount` | Return at t is R_{t+1} + γG_{t+1}; compute backwards. |
| `test_every_visit` | With first_visit=False every occurrence adds its return. |
| `test_unvisited` | Unvisited states keep V = 0 and count 0. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A backward pass gives the return at every time step. Scanning forward, the first-visit rule skips
repeated states within an episode. Running sums and counts produce averages; unvisited states stay 0.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
