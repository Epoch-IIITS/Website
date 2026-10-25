# FL-04 · Label-Skewed (non-IID) Partition

**Topic:** Federated Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** FL-01 IID Client Partitioning

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `shard_partition(labels, n_clients, shards_per_client, seed)` → list of sorted index arrays
  following the recipe (stable `np.argsort(labels, kind="stable")`). Raise `ValueError` if there are
  fewer examples than shards.
* `label_counts(labels, parts, n_classes)` → int array `(n_clients, n_classes)`.

**Example**
```python
labels = np.array([0, 1, 2, 3, 4] * 2)
parts = shard_partition(labels, 5, 1, seed=0)
label_counts(labels, parts, 5).max(axis=1)   # [2, 2, 2, 2, 2] — every client holds one class
```

## Hints

<details><summary>Hint 1</summary>

`order = np.argsort(labels, kind='stable')`; `shards = np.array_split(order, n_clients * s)`.

</details>

<details><summary>Hint 2</summary>

`ids = rng.permutation(len(shards))`; client k gets `ids[k*s:(k+1)*s]`.

</details>

<details><summary>Hint 3</summary>

Counts: `np.bincount(labels[p], minlength=n_classes)` per part.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_recipe` | Stable argsort by label, array_split into n_clients*s shards, deal shards by rng.permutation. |
| `test_one_class_each` | Shards are contiguous slices of the label-sorted indices. |
| `test_cover` | Every example must belong to exactly one client. |
| `test_counts_shape` | Use np.bincount with minlength=n_classes per client. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Sorting by label groups each class together, so contiguous shards contain one (or two) classes.
Randomly dealing shards to clients produces pathological label skew; `bincount` per client reveals
the resulting label distribution.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
