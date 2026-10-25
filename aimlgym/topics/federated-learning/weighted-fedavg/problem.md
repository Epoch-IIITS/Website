# FL-02 · Weighted Federated Averaging

**Topic:** Federated Learning · **Difficulty:** beginner · **Allowed packages:** numpy

**Builds on:** FL-01 IID Client Partitioning

Read the lesson first: [article.md](article.md)

## Task

Write `fedavg(client_params, sizes)` where `client_params` is a non-empty list of dicts
name → NumPy array (same keys and shapes) and `sizes` a list of non-negative ints. Return a new dict
of weighted averages. Raise `ValueError` for empty input, length mismatch, negative sizes, zero total
size, or mismatched keys/shapes.

**Example**
```python
fedavg([{"w": np.array([1., 2.])}, {"w": np.array([3., 6.])}], [10, 30])   # {'w': array([2.5, 5. ])}
```

## Hints

<details><summary>Hint 1</summary>

`N = sum(sizes)`; weights `n_k / N`.

</details>

<details><summary>Hint 2</summary>

Check `set(p) == set(client_params[0])` and shapes for every client.

</details>

<details><summary>Hint 3</summary>

`{k: sum(wt * p[k] for wt, p in zip(weights, client_params)) for k in keys}`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_not_plain_mean` | Weight each client by n_k / N, not 1/K. |
| `test_multiple_keys` | Average every parameter tensor separately. |
| `test_zero_size_client` | Clients with zero samples get weight zero. |
| `test_errors` | Validate keys, shapes and the total size. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

After validating structure, each parameter tensor is averaged with weights n_k / N, so larger clients
count more and the weights sum to one.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
