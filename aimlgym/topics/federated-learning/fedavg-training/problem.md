# FL-10 · Full FedAvg Training Loop

**Topic:** Federated Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** FL-07 One FedAvg Round, FL-08 Seeded Client Sampling

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `global_loss(w, clients)` → MSE over all clients' data combined.
* `train_fedavg(clients, w0, rounds, fraction, lr, epochs, batch_size, seed)` → `(w, history)` following
  the pseudocode exactly (include your own copies of `sample_clients` and `local_sgd`; `batch_size`
  `None` = full batch). `history[t]` is the global loss after round t.

**Example**
```python
w, hist = train_fedavg(clients, np.zeros(2), rounds=30, fraction=1.0, lr=0.1, epochs=2, batch_size=4, seed=0)
hist[-1] < hist[0]     # True
```

## Hints

<details><summary>Hint 1</summary>

Global loss: total squared error over all clients / total samples.

</details>

<details><summary>Hint 2</summary>

Client seed: `seed * 1000 + t * K + k`.

</details>

<details><summary>Hint 3</summary>

Aggregate only over `S_t` with weights `len(y_k)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_first_round_matches_manual` | Use seed*1000 + t*K + k for client k in round t and average only sampled clients. |
| `test_global_loss` | Global loss = total squared error / total number of samples. |
| `test_converges_iid` | Every round must start local training from the current global w. |
| `test_reproducible` | All randomness must come from seeded generators. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each round samples participants, trains each from the current global model with a unique seed,
aggregates only the participants' models by size, and evaluates the loss on all clients' data. The
seed scheme makes every run fully reproducible.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
