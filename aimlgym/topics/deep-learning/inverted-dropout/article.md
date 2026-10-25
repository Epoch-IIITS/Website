# Inverted Dropout

## Learning outcomes

After this lesson you can:

- Implement inverted dropout for training and evaluation modes
- Keep expected activations unchanged by rescaling
- Backpropagate through the dropout mask

## Intuition
During training, randomly switch off a fraction of units so the network cannot rely on any single
one — like a team practising with random members absent. At test time everyone plays.

## Precise explanation
With drop probability $p$:
* **Training:** mask $m_i \sim \text{Bernoulli}(1-p)$ (1 = keep); output $y = x \odot m / (1-p)$.
  Dividing by $1-p$ ("inverted" dropout) keeps $\mathbb E[y] = x$, so nothing needs rescaling at
  test time.
* **Evaluation:** $y = x$ (no randomness).
* **Backward:** $\partial L/\partial x = \partial L/\partial y \odot m / (1-p)$.
* $p = 0$ → identity; $p = 1$ is invalid (division by zero).
Mask recipe used here: `keep = rng.random(x.shape) >= p`.

## Worked example
x = [2, 2, 2, 2], p = 0.5, mask [1, 0, 1, 1] → y = [4, 0, 4, 4]; mean of y ≈ 2 on average.

## Common mistakes
* Applying dropout at evaluation time.
* Scaling at test time *and* using inverted dropout (double scaling).
* Generating a new mask in the backward pass.

## Why this matters
Dropout is a standard regulariser in MLPs and transformers; train/eval mode switches are a
classic source of bugs.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
