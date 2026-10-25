# Secure Aggregation (simplified)

## Learning outcomes

After this lesson you can:

- Generate cancelling pairwise masks from shared seeds
- Recover the exact sum of updates without seeing any single update
- Recover the sum when a client drops out by removing its pairwise masks

## Intuition
The server should learn only the *sum* of client updates, never an individual update. Each pair of
clients agrees on a random mask; one adds it, the other subtracts it. Every masked update looks like
noise, but in the sum all masks cancel.

## Precise explanation (core idea of Bonawitz et al., 2017)
For clients $i < j$ with a shared seed $s_{ij}$, mask $m_{ij} = \text{PRG}(s_{ij})$ (a random vector).
Client i sends
$$y_i = x_i + \sum_{j > i} m_{ij} - \sum_{j < i} m_{ji}.$$
Then $\sum_i y_i = \sum_i x_i$ because each $m_{ij}$ appears once with + and once with −.
**Dropouts:** if client d never sends $y_d$, the masks between d and the survivors no longer cancel.
In the real protocol survivors reveal secret shares that let the server reconstruct $s_{dj}$; here we
simulate that by letting the server regenerate those pairwise masks and remove them.
Simplifications in this exercise: seeds are derived deterministically from `(base_seed, i, j)` instead
of Diffie–Hellman key agreement, masks are real-valued Gaussian vectors instead of integers modulo a
large number, and there is no secret sharing — so this is **not secure**, only a faithful model of the
cancellation arithmetic.

## Worked example
x₀ = [1], x₁ = [2], m₀₁ = [5]: y₀ = [6], y₁ = [−3]; sum [3] = x₀ + x₁ ✓.

## Common mistakes
* Both clients adding the mask (no cancellation).
* Seeding masks per client instead of per pair.
* Forgetting the dropped client's pairs, leaving a random error in the sum.

## Why this matters
Secure aggregation lets FL provide privacy against an honest-but-curious server and is often combined
with differential privacy (FL-13).

## References

- [Practical Secure Aggregation for Federated Learning on User-Held Data](https://arxiv.org/abs/1611.04482) — Keith Bonawitz et al. (`S029`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
