# DP-style Aggregation: Clip, Average, Add Noise

## Learning outcomes

After this lesson you can:

- Clip per-client updates and average them
- Add calibrated Gaussian noise (noise multiplier × clip / m)
- Measure the privacy–utility trade-off empirically

## Intuition
Even aggregated updates can leak information about one client's data. Differential privacy (DP)
limits that leakage: clip each client's influence, then add random noise large enough to hide any
single contribution.

## Precise explanation (Gaussian mechanism as used by DP-FedAvg, McMahan et al., 2017)
For m participating clients with updates $\Delta_k$:
1. Clip: $\tilde\Delta_k = \text{clip}(\Delta_k, C)$ (FL-09).
2. Average: $\bar\Delta = \frac1m\sum_k\tilde\Delta_k$. Replacing one client changes this by at most
   $2C/m$ (L2 sensitivity of the *replace-one* neighbour definition; $C/m$ for add/remove).
3. Noise: $\bar\Delta + \mathcal N(0, \sigma^2 I)$ with $\sigma = z\cdot C/m$, where z is the
   **noise multiplier**.
Larger z → stronger privacy, noisier model. Converting z, sampling rate and rounds into a formal
(ε, δ) guarantee requires a privacy accountant (out of scope here; the paper and the FL survey
discuss it). This exercise implements the mechanism, not the accounting.

## Worked example
Updates [3, 4] and [0.3, 0.4], C = 1 → clipped [0.6, 0.8] and [0.3, 0.4] → mean [0.45, 0.6];
with z = 0 that is the result; with z = 1 the noise std is 1·1/2 = 0.5 per coordinate.

## Common mistakes
* Noise scale using the number of all clients instead of participants.
* Adding noise before clipping.
* Claiming an ε without an accountant.

## Why this matters
DP aggregation is how deployed FL systems give formal privacy guarantees.

## References

- [Learning Differentially Private Recurrent Language Models](https://arxiv.org/abs/1710.06963) — H. Brendan McMahan, Daniel Ramage, Kunal Talwar, Li Zhang (`S031`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
