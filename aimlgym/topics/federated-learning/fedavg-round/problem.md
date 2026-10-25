# FL-07 · One FedAvg Round

**Topic:** Federated Learning · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** FL-02 Weighted Federated Averaging, FL-05 Client Training with a PyTorch Model

Read the lesson first: [article.md](article.md)

## Task

Write `fedavg_round(global_w, clients, lr, epochs, batch_size, seed)` returning
`(new_global, local_models)`. Each client `k` (tuple `(X, y)`) runs `local_sgd` (FL-06 recipe, include
your own copy) from `global_w` with seed `seed + k`; aggregate with weights `len(y_k)`. `batch_size`
may be `None` meaning full batch (`len(y_k)`). Raise `ValueError` for an empty client list.

**Example**
```python
new_w, locals_ = fedavg_round(np.zeros(2), clients, lr=0.1, epochs=1, batch_size=None, seed=0)
# equals one centralised GD step on all data
```

## Hints

<details><summary>Hint 1</summary>

Loop `for k, (X, y) in enumerate(clients)`.

</details>

<details><summary>Hint 2</summary>

`bs = len(y) if batch_size is None else batch_size`.

</details>

<details><summary>Hint 3</summary>

Aggregate: `sum(n * w for n, w in zip(sizes, locals_)) / sum(sizes)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_equals_centralised_step` | All clients must start from global_w; aggregate with weights n_k/N. |
| `test_seeds_per_client` | Client k uses seed + k. |
| `test_weighting` | Weight each local model by its client's number of samples. |
| `test_global_unchanged` | Never modify global_w in place. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Every client starts from the same broadcast weights and trains with its own seed. The server
combines the returned models by data-size-weighted averaging. With one full-batch epoch, the weighted
average of one-step updates equals a single gradient step on the pooled data.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
