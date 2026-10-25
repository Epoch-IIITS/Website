# Clipping Client Updates

## Learning outcomes

After this lesson you can:

- Clip update vectors to a maximum L2 norm
- Preserve direction while bounding magnitude
- Report how many clients were clipped

## Intuition
One faulty or malicious client could send an enormous update and wreck the global model. Clipping
caps every update's length while keeping its direction — and it bounds how much any single client
can influence the aggregate, which differential privacy needs (FL-13).

## Precise explanation
$$\text{clip}(\Delta, C) = \Delta \cdot \min\!\left(1, \frac{C}{\lVert\Delta\rVert_2}\right).$$
Updates already within the norm are unchanged; larger ones are scaled down to norm exactly C. The
zero vector stays zero. McMahan et al. (2017) clip per-user updates this way for user-level DP.
After clipping, replacing one client's update changes a *sum* of updates by at most $2C$.

## Worked example
Δ = [3, 4] (norm 5), C = 2.5 → [1.5, 2.0] (norm 2.5). Δ = [0.3, 0.4], C = 2.5 → unchanged.

## Common mistakes
* Clipping each coordinate separately (changes direction).
* Division by zero for a zero update.
* Clipping after aggregation (doesn't bound individual influence).

## Why this matters
Clipping is standard in DP-SGD/DP-FedAvg and a simple robustness measure.

## References

- [Learning Differentially Private Recurrent Language Models](https://arxiv.org/abs/1710.06963) — H. Brendan McMahan, Daniel Ramage, Kunal Talwar, Li Zhang (`S031`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
