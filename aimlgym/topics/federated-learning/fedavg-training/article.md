# The Full FedAvg Algorithm

## Learning outcomes

After this lesson you can:

- Combine sampling, local training and aggregation over many rounds
- Track global loss per round
- Compare IID and non-IID convergence

## Intuition
Repeat FedAvg rounds with a random subset of clients each time. Watch the global loss fall, using far
fewer communication rounds than one-gradient-step-per-round SGD would need.

## Precise explanation
```text
w = w0
for t in 0..R-1:
    S_t = sample_clients(K, C, seed, t)                 # FL-08
    for k in S_t: w_k = local_sgd(w, data_k, lr, E, B, seed*1000 + t*K + k)   # FL-06
    w = Σ_{k∈S_t} n_k w_k / Σ_{k∈S_t} n_k               # FL-02 over participants only
    record global_loss(w)
```
**Global loss** = size-weighted mean of client MSEs = MSE on the pooled data.
On IID data FedAvg converges quickly; on label/feature-skewed data local models drift apart and
progress slows or oscillates (McMahan et al.; FL survey), motivating FedProx (FL-14).

<svg xmlns="http://www.w3.org/2000/svg" width="270" height="150" viewBox="0 0 270 150" role="img" aria-label="Two decreasing loss curves over rounds; the IID curve drops faster than the non-IID curve">
<title>FedAvg loss curves</title>
<line x1="30" y1="130" x2="260" y2="130" stroke="#999"/><line x1="30" y1="130" x2="30" y2="10" stroke="#999"/>
<path d="M 30 20 C 60 90, 90 115, 250 122" fill="none" stroke="#1f77b4" stroke-width="2"/>
<path d="M 30 20 C 80 50, 130 85, 250 108" fill="none" stroke="#d62728" stroke-width="2" stroke-dasharray="5 3"/>
<text x="180" y="112" font-size="11" fill="#1f77b4">IID</text><text x="180" y="88" font-size="11" fill="#d62728">non-IID</text>
<text x="120" y="146" font-size="11">round</text>
</svg>

*Figure (original, schematic): typical global loss curves.*

## Worked example
3 clients holding noise-free data from y = 2x₀ − x₁ converge to w ≈ [2, −1].

## Common mistakes
* Averaging over all clients instead of the sampled ones.
* Evaluating loss only on participants.
* Reusing one seed for every client and round.

## Why this matters
This is the end-to-end algorithm deployed in production FL systems (with many engineering additions).

## References

- [Communication-Efficient Learning of Deep Networks from Decentralized Data](https://arxiv.org/abs/1602.05629) — H. Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, Blaise Agüera y Arcas (`S028`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
