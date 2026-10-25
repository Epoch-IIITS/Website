# Client Sampling

## Learning outcomes

After this lesson you can:

- Select a fraction C of clients per round without replacement
- Make each round's selection reproducible
- Check participation rates over many rounds

## Intuition
In cross-device FL (millions of phones) only a small fraction of clients participate in each round —
those that are charging, idle and on Wi-Fi. Simulations model this by sampling a fraction C of
clients per round.

## Precise explanation
* Number per round: $m = \max(1, \operatorname{round}(C\cdot K))$ (McMahan et al. use $\max(\lceil
  CK\rceil, 1)$; we use round — a design choice — and test it).
* Sample without replacement and sort for readability.
* Reproducibility per round: seed the generator with `(seed, round_idx)` —
  `np.random.default_rng([seed, round_idx])` — so round 7 always selects the same clients regardless
  of how many earlier rounds were simulated.
* Over many rounds each client participates with frequency ≈ m/K.
Cross-silo FL (a few hospitals) often uses all clients every round (C = 1).

## Worked example
K = 10, C = 0.3 → 3 clients per round, e.g. [1, 4, 8].

## Common mistakes
* Sampling with replacement (the same client twice).
* m = 0 for tiny fractions.
* One global RNG whose state depends on the simulation history.

## Why this matters
Partial participation is a key source of noise and bias in FL; FL-10 uses this sampler.

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
