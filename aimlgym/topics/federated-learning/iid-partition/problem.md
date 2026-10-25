# FL-01 · IID Client Partitioning

**Topic:** Federated Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** ML-16 Cross-Validation with scikit-learn

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `iid_partition(n, n_clients, seed)` → list of `n_clients` sorted index arrays from
  `np.array_split(np.random.default_rng(seed).permutation(n), n_clients)` (sort each part).
  Raise `ValueError` unless `1 <= n_clients <= n`.
* `client_sizes(parts)` → list of ints.

**Example**
```python
parts = iid_partition(10, 3, seed=0)
client_sizes(parts)                        # [4, 3, 3]
sorted(np.concatenate(parts).tolist())     # [0, 1, ..., 9]
```

## Hints

<details><summary>Hint 1</summary>

`perm = np.random.default_rng(seed).permutation(n)`.

</details>

<details><summary>Hint 2</summary>

`[np.sort(p) for p in np.array_split(perm, n_clients)]`.

</details>

<details><summary>Hint 3</summary>

`[len(p) for p in parts]`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe` | Use default_rng(seed).permutation(n) then np.array_split; sort each part. |
| `test_cover_disjoint` | Every index must appear in exactly one client. |
| `test_sizes` | array_split gives the first n % k clients one extra item. |
| `test_errors` | Reject n_clients greater than n. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

One seeded permutation randomises assignment; `array_split` yields disjoint, covering shards whose
sizes differ by at most one. Sorting each shard only makes outputs easier to read.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
