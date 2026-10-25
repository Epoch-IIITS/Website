# FL-03 · Client Updates as Deltas

**Topic:** Federated Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** FL-02 Weighted Federated Averaging

Read the lesson first: [article.md](article.md)

## Task

Implement with NumPy arrays:
* `client_delta(global_w, local_w)` → `local_w - global_w` (shapes must match, else `ValueError`).
* `server_update(global_w, deltas, sizes, server_lr=1.0)` → new global array. Raise `ValueError` for
  empty deltas, length mismatch, or zero total size. Inputs must not be modified.

**Example**
```python
server_update(np.zeros(2), [np.array([1., 1.]), np.array([3., -1.])], [1, 1], server_lr=0.5)   # [1., 0.]
```

## Hints

<details><summary>Hint 1</summary>

Delta is `local - global`.

</details>

<details><summary>Hint 2</summary>

Weighted mean: `sum(n / N * d for n, d in zip(sizes, deltas))`.

</details>

<details><summary>Hint 3</summary>

Return `global_w + server_lr * mean_delta` (a new array).

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_delta` | Delta = local − global. |
| `test_equals_fedavg` | Weight deltas by n_k/N; with server_lr = 1 you must reproduce FedAvg. |
| `test_no_mutation` | Return a new array; don't use += on global_w. |
| `test_server_lr` | Multiply the aggregated delta by server_lr. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Deltas are local minus global parameters. The server takes their size-weighted mean and steps in
that direction with its own learning rate; with rate 1 the result is algebraically identical to
FedAvg.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
