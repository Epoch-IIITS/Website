# Momentum

## Learning outcomes

After this lesson you can:

- Implement the momentum update
- Keep optimiser state per parameter
- Compare convergence on an ill-conditioned quadratic

## Intuition
Plain gradient descent zig-zags across narrow valleys. Momentum treats the parameters like a
heavy ball: it accumulates velocity in consistent directions and damps oscillations.

## Precise explanation
For each parameter $\theta$ with gradient $g$:
$$v \leftarrow \beta v + g,\qquad \theta \leftarrow \theta - \eta v,$$
with $v$ initialised to zeros of the same shape and $\beta \in [0, 1)$ (typically 0.9).
$\beta = 0$ is plain SGD. Velocity is optimiser **state**, kept per parameter between steps.
(Some libraries write $v \leftarrow \beta v + (1-\beta) g$; that only rescales the learning rate.)

## Worked example
$\eta = 0.1$, $\beta = 0.9$, constant gradient 1: v = 1, 1.9, 2.71 … so the steps grow
0.1, 0.19, 0.271 — acceleration along a consistent slope.

## Common mistakes
* Re-initialising velocity every step (then it is plain SGD).
* Sharing one velocity array between parameters.
* Mutating the caller's gradient arrays.

## Why this matters
Momentum (and its descendants such as Adam) is how practically every network is trained; FedAvg
servers can also apply momentum to aggregated updates.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
