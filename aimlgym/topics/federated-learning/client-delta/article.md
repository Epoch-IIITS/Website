# Sending Deltas Instead of Models

## Learning outcomes

After this lesson you can:

- Represent client work as a model delta
- Apply aggregated deltas with a server learning rate
- Show equivalence with FedAvg when server_lr = 1

## Intuition
Clients start from the same global model and change it a little. Sending the *change* (delta) rather
than the whole model makes aggregation look like a gradient step on the server — and it is the
quantity that clipping (FL-09) and privacy noise (FL-13) operate on.

## Precise explanation
* Client delta: $\Delta_k = w_k - w$ (local minus global).
* Server: $w \leftarrow w + \eta_s \sum_k \frac{n_k}{N}\Delta_k$.
* With $\eta_s = 1$ this equals FedAvg exactly:
  $w + \sum_k \frac{n_k}{N}(w_k - w) = \sum_k \frac{n_k}{N} w_k$.
* $\eta_s \ne 1$ (or server momentum) gives "FedOpt"-style variants discussed in the FL survey.

## Worked example
w = [0, 0]; local A = [1, 1] (n 1), local B = [3, −1] (n 1) → deltas [1, 1], [3, −1] → mean [2, 0];
η_s = 0.5 → new w = [1, 0].

## Common mistakes
* Sign errors (global − local).
* Applying deltas computed from different global versions.
* Mutating the global model in place on the client side.

## Why this matters
Delta-based aggregation is how production FL systems and privacy mechanisms are described.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
