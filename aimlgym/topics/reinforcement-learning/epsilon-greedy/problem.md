# RL-05 · Epsilon-Greedy Action Selection

**Topic:** Reinforcement Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** RL-03 The Environment Interface: reset and step, NP-10 Seeded Random Generators

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `epsilon_greedy(q_values, epsilon, rng)` → int action following the recipe (one `rng.random()`
  call, then `rng.integers(n)` only when exploring).
* `epsilon_greedy_probs(q_values, epsilon)` → probability array as described.
Raise `ValueError` unless `0 <= epsilon <= 1` and `q_values` is non-empty.

**Examples**
```python
epsilon_greedy_probs([1, 5, 2], 0.3)               # [0.1, 0.8, 0.1]
epsilon_greedy([1, 5, 2], 0.0, np.random.default_rng(0))   # 1
```

## Hints

<details><summary>Hint 1</summary>

`q = np.asarray(q_values)`; `n = len(q)`.

</details>

<details><summary>Hint 2</summary>

`if rng.random() < epsilon: return int(rng.integers(n))`.

</details>

<details><summary>Hint 3</summary>

Probs: `p = np.full(n, epsilon / n); p[np.argmax(q)] += 1 - epsilon`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe` | Draw rng.random() first; call rng.integers(n) only when exploring. |
| `test_probs` | Greedy action gets 1 − ε + ε/|A|; others ε/|A|. |
| `test_ties_lowest` | np.argmax returns the lowest index on ties. |
| `test_frequencies` | Random exploration chooses among all actions, including the greedy one. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One uniform draw decides between exploring and exploiting; exploration samples any action uniformly,
including the greedy one. The probability vector follows directly from that procedure.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
