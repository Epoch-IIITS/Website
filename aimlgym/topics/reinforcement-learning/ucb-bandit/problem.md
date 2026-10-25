# RL-07 · UCB1 Bandit

**Topic:** Reinforcement Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** RL-06 Incremental Value Estimates

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `ucb_select(q, n, t, c=2.0)` → int arm per the rule above.
* `run_bandit(means, steps, seed, policy="ucb", epsilon=0.1, c=2.0)` → dict
  `{"actions": list, "rewards": list, "regret": float}`.
  `rng = np.random.default_rng(seed)`; per step t = 1..steps: choose (UCB uses `t`; "egreedy" uses
  RL-05's recipe with the same rng *before* the reward draw), then reward `float(rng.random() < means[a])`,
  then update sample-average estimates. Regret uses the **true means** of chosen arms.

**Example**
```python
ucb_select(np.array([0.5, 0.4]), np.array([10, 2]), 13)   # 1
r = run_bandit([0.2, 0.8], 1000, seed=0)
r["actions"].count(1) > 900     # True
```

## Hints

<details><summary>Hint 1</summary>

Untried arms: `zeros = np.flatnonzero(n == 0)`; return `zeros[0]` if any.

</details>

<details><summary>Hint 2</summary>

Scores: `q + c * np.sqrt(np.log(t) / n)`; `np.argmax`.

</details>

<details><summary>Hint 3</summary>

Update: `n[a] += 1; q[a] += (r - q[a]) / n[a]`; regret = `steps*max(means) - sum(means[a])`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_untried_first` | Arms with N = 0 must be selected before computing bonuses. |
| `test_select` | Bonus = c·sqrt(ln t / N(a)) using the total time t. |
| `test_regret_definition` | Regret uses true means of the chosen arms, not observed rewards. |
| `test_learns_best` | Update counts and sample averages after every pull. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

UCB first tries every arm once, then adds a confidence bonus that is large for rarely tried arms and
grows slowly with time. The simulation draws rewards from one seeded generator, updates sample
averages, and reports regret against the best arm's true mean.

## References

- [Reinforcement Learning: An Introduction (2nd edition)](http://incompleteideas.net/book/the-book-2nd.html) — Richard S. Sutton, Andrew G. Barto (MIT Press 2018) (`S033`)
