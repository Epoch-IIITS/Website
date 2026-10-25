# Non-IID Data: Label Skew

## Learning outcomes

After this lesson you can:

- Build McMahan-style pathological non-IID shards
- Measure per-client label distributions
- Quantify heterogeneity

## Intuition
A phone keyboard user types mostly in one language; a hospital sees mostly certain conditions. Real
clients have very different data. A standard stress test gives each client only a couple of classes.

## Precise explanation (shard method of McMahan et al.)
1. Sort example indices by label (stable sort).
2. Cut the sorted list into `n_clients * shards_per_client` equal-ish shards (`np.array_split`).
3. Shuffle shard ids with `rng.permutation`, and give client k the shards at positions
   `k*s .. (k+1)*s - 1` of the shuffled list.
With 2 shards per client, most clients see only 1–2 labels. **Label counts** per client form a
`(n_clients, n_classes)` table; a simple heterogeneity summary is the average number of distinct
labels per client.

## Worked example
10 examples, labels 0..4 twice each, 5 clients × 1 shard → each client gets exactly one label.

## Common mistakes
* Unstable sorting (non-reproducible shard contents).
* Shards that cross class boundaries unintentionally (fine — that's realistic — but know it happens).
* Forgetting that skewed partitions slow FedAvg convergence (FL-10).

## Why this matters
Non-IID data is the defining challenge of FL and motivates FedProx (FL-14).

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
