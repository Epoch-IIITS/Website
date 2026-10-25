# RL-06 · Incremental Value Estimates

**Topic:** Reinforcement Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** RL-05 Epsilon-Greedy Action Selection

Read the lesson first: [article.md](article.md)

## Task

Implement `class ValueEstimates(n_actions, alpha=None)` with arrays `q` (zeros) and `n` (int zeros)
and method `update(a, r)` that increments `n[a]` and updates `q[a]` with step `1/n[a]` (if `alpha`
is None) or `alpha`. Return the new `q[a]`. Raise `ValueError` for an invalid action or
`alpha` not in `(0, 1]`.

**Example**
```python
v = ValueEstimates(2)
[v.update(0, r) for r in (2, 4, 6)]       # [2.0, 3.0, 4.0]
w = ValueEstimates(1, alpha=0.5)
[w.update(0, r) for r in (2, 4, 6)]       # [1.0, 2.5, 4.25]
```

## Hints

<details><summary>Hint 1</summary>

`self.q = np.zeros(n_actions)`; `self.n = np.zeros(n_actions, dtype=int)`.

</details>

<details><summary>Hint 2</summary>

Increment `self.n[a]` first, then `step = 1 / self.n[a]` (or alpha).

</details>

<details><summary>Hint 3</summary>

`self.q[a] += step * (r - self.q[a])`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_sample_average` | Increment n[a] before computing the 1/n step. |
| `test_constant_alpha` | With alpha set, use it as a constant step size. |
| `test_tracks_change` | Constant α forgets old rewards; 1/n does not. |
| `test_independent_arms` | Keep separate counts and estimates per action. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Incrementing the count before computing 1/n makes the first update replace the initial zero with the
first reward, and later updates reproduce the running mean exactly. A constant α instead gives an
exponentially weighted average.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
