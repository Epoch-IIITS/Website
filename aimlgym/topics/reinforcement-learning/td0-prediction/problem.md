# RL-12 · TD(0) Prediction

**Topic:** Reinforcement Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** RL-08 Iterative Policy Evaluation, RL-11 First-Visit Monte Carlo Prediction

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `td_error(V, s, r, s_next, done, gamma)` → float δ.
* `td0(episodes, n_states, alpha, gamma, sweeps=1)` → value array; `episodes` is a list of episodes,
  each a list of `(s, r, s_next, done)`; process all episodes in order, `sweeps` times, updating
  in place from `V = zeros`. Raise `ValueError` unless `0 < alpha <= 1` and `0 <= gamma <= 1`.

**Example**
```python
td0([[(0, 1.0, 1, False), (1, 2.0, 1, True)]], 2, alpha=0.5, gamma=1.0)   # [0.5, 1. ]
```

## Hints

<details><summary>Hint 1</summary>

`target = r + (0 if done else gamma * V[s_next])`.

</details>

<details><summary>Hint 2</summary>

`delta = target - V[s]`; then `V[s] += alpha * delta`.

</details>

<details><summary>Hint 3</summary>

Outer loop over sweeps, then episodes, then transitions.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_td_error` | Don't bootstrap when done is True. |
| `test_order_matters` | Update V in place, transition by transition, in order. |
| `test_converges_chain` | Repeat all episodes `sweeps` times. |
| `test_batch_td_vs_mc` | Batch TD values A by bootstrapping from B (Sutton & Barto's A/B example idea). |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The TD error compares the one-step bootstrapped target with the current estimate; the value moves a
fraction α towards the target. Processing transitions in order with in-place updates is online TD(0).

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
