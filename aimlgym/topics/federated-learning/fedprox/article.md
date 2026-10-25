# FedProx: Limiting Client Drift

## Learning outcomes

After this lesson you can:

- Add a proximal term to the local objective
- Derive and implement its gradient
- Show that μ limits client drift on heterogeneous data

## Intuition
On non-IID data, a client that trains for many local steps runs off towards *its own* optimum, and
averaging such drifted models works poorly. FedProx adds a spring that pulls each local model back
towards the global model.

## Precise explanation (Li et al., 2018)
Local objective for client k:
$$h_k(w) = L_k(w) + \frac{\mu}{2}\lVert w - w^{t}\rVert^2,$$
where $w^t$ is the current global model and $L_k$ the local loss (here MSE). Gradient:
$$\nabla h_k(w) = \nabla L_k(w) + \mu\,(w - w^t).$$
* μ = 0 recovers FedAvg's local training.
* Large μ keeps $w$ near $w^t$ (less drift, slower local progress).
For linear regression the minimiser of $h_k$ interpolates between the local least-squares solution
(μ → 0) and the global model (μ → ∞).

## Worked example
One feature, X = [[1]], y = [4], w^t = 0. Minimiser of $(w - 4)^2 + \frac{\mu}{2}w^2$ is
$w^* = 8/(2 + \mu)$: μ = 0 → 4, μ = 2 → 2, μ = 1000 → ≈ 0.008.

## Common mistakes
* Wrong sign of the proximal gradient.
* Using the *initial* local model instead of the global model as the anchor (they are equal at step 0
  but the anchor must stay fixed).
* Applying the proximal term on the server.

## Why this matters
FedProx is a standard baseline for heterogeneous federated settings.

## References

- [Federated Optimization in Heterogeneous Networks](https://arxiv.org/abs/1812.06127) — Tian Li et al. (`S030`)
- [Advances and Open Problems in Federated Learning](https://arxiv.org/abs/1912.04977) — Peter Kairouz, H. Brendan McMahan et al. (`S032`)
