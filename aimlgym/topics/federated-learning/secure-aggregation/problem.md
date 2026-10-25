# FL-12 · Secure Aggregation with Pairwise Masks

**Topic:** Federated Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** FL-02 Weighted Federated Averaging

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `pair_mask(i, j, dim, base_seed)` → for `i < j`, `np.random.default_rng([base_seed, i, j]).normal(size=dim)`
  (raise `ValueError` if `i >= j`).
* `mask_update(i, update, n_clients, base_seed)` → masked vector per the formula.
* `aggregate(masked, n_clients, dim, base_seed, dropped=())` → `masked` is a dict client id → masked
  vector for **surviving** clients; `dropped` lists ids that sent nothing. Return the sum of the
  survivors' true updates: sum the masked vectors, then for each dropped d and each survivor s remove
  the unmatched mask (if `s < d` the survivor added `m_sd`; if `s > d` it subtracted `m_ds`).

**Example**
```python
ups = [np.array([1., 2.]), np.array([3., 4.]), np.array([5., 6.])]
masked = {i: mask_update(i, ups[i], 3, base_seed=7) for i in range(3)}
aggregate(masked, 3, 2, 7)                                    # ≈ [9., 12.]
aggregate({0: masked[0], 2: masked[2]}, 3, 2, 7, dropped=[1])  # ≈ [6., 8.]
```

## Hints

<details><summary>Hint 1</summary>

In `mask_update`, loop `j` over all other clients: add `pair_mask(i, j)` if `j > i`, subtract `pair_mask(j, i)` if `j < i`.

</details>

<details><summary>Hint 2</summary>

Sum the survivors' masked vectors.

</details>

<details><summary>Hint 3</summary>

For dropped d and survivor s: subtract `pair_mask(s, d)` if `s < d`, add `pair_mask(d, s)` if `s > d`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_full_sum` | Client i adds m_ij for j > i and subtracts m_ji for j < i. |
| `test_dropout` | For each dropped d, remove the masks between d and every survivor with the right sign. |
| `test_pair_mask` | Seed each pair with default_rng([base_seed, i, j]) for i < j. |
| `test_individual_hidden` | Masked updates should look nothing like the raw updates. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each pair's mask enters one client's message with + and the other's with −, so they cancel in the
sum. When a client drops, its partners' masks with it are left uncancelled; regenerating exactly
those pairwise masks and removing them recovers the survivors' true sum.

## References

- [Practical Secure Aggregation for Federated Learning on User-Held Data](https://arxiv.org/abs/1611.04482) — Keith Bonawitz et al. (`S029`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
