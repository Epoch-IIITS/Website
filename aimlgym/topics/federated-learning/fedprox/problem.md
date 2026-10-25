# FL-14 · FedProx Local Objective

**Topic:** Federated Learning · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** FL-05 Client Training with a PyTorch Model, FL-10 Full FedAvg Training Loop

Read the lesson first: [article.md](article.md)

## Task

Implement full-batch local training for linear regression:
* `prox_grad(w, w_global, X, y, mu)` → `2/n · Xᵀ(Xw − y) + mu·(w − w_global)`.
* `local_prox_gd(w_global, X, y, mu, lr, steps)` → weights after `steps` gradient steps starting from
  `w_global` (copied). Raise `ValueError` if `mu < 0`, `lr <= 0` or `steps < 1`.

**Example**
```python
local_prox_gd(np.zeros(1), np.array([[1.]]), np.array([4.]), mu=2.0, lr=0.1, steps=500)   # ≈ [2.]
```

## Hints

<details><summary>Hint 1</summary>

MSE gradient from FL-06 plus `mu * (w - w_global)`.

</details>

<details><summary>Hint 2</summary>

Keep `w_global` fixed as the anchor during all steps.

</details>

<details><summary>Hint 3</summary>

Start from `w = np.array(w_global, dtype=float)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_grad_formula` | Proximal gradient adds mu·(w − w_global). |
| `test_closed_form` | Keep the anchor w_global fixed; minimiser is 8/(2 + mu) for the 1-D example. |
| `test_mu0_plain` | With mu = 0, FedProx equals plain gradient descent. |
| `test_anchor_fixed` | Copy w_global; don't modify it. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The proximal gradient adds a linear pull towards the fixed global anchor. Running gradient descent on
the augmented objective yields a local model that balances fitting local data against staying close
to the global model, controlled by μ.

## References

- [Federated Optimization in Heterogeneous Networks](https://arxiv.org/abs/1812.06127) — Tian Li et al. (`S030`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
