# FL-08 · Seeded Client Sampling

**Topic:** Federated Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** FL-07 One FedAvg Round

Read the lesson first: [article.md](article.md)

## Task

Write `sample_clients(n_clients, fraction, seed, round_idx)` → sorted int array of
`max(1, round(fraction * n_clients))` distinct client ids, chosen with
`np.random.default_rng([seed, round_idx]).choice(n_clients, m, replace=False)`.
Raise `ValueError` unless `0 < fraction <= 1` and `n_clients >= 1`.

**Example**
```python
s = sample_clients(10, 0.3, seed=0, round_idx=0)
len(s), len(set(s.tolist()))     # (3, 3)
sample_clients(10, 1.0, 0, 5)    # array([0, 1, ..., 9])
```

## Hints

<details><summary>Hint 1</summary>

`m = max(1, round(fraction * n_clients))`.

</details>

<details><summary>Hint 2</summary>

`rng = np.random.default_rng([seed, round_idx])`.

</details>

<details><summary>Hint 3</summary>

`np.sort(rng.choice(n_clients, m, replace=False))`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe_and_round_independence` | Seed with default_rng([seed, round_idx]) and use choice(..., replace=False). |
| `test_min_one` | Always select at least one client. |
| `test_count_distinct` | Sample without replacement. |
| `test_participation_rate` | Each round must be an independent draw. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The per-round seed sequence `[seed, round_idx]` gives an independent, reproducible stream for every
round. Sampling without replacement guarantees distinct clients, and the count rule never returns zero.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
