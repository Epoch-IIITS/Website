# The Adam Optimiser

## Learning outcomes

After this lesson you can:

- Maintain first- and second-moment estimates of the gradient
- Apply bias correction for the early steps
- Explain why Adam's step size is roughly lr regardless of gradient scale
- Use the same params/grads dictionary interface as Momentum

## Intuition
DL-14 smooths the *direction* of the gradient. Adam also adapts the *step size* of each
parameter: parameters whose gradients are consistently large take proportionally smaller steps,
and rarely-updated parameters take larger ones. It is the default optimiser for most deep
learning.

## Precise explanation
For each parameter, keep $m$ (moving average of gradients) and $v$ (moving average of squared
gradients), both starting at 0, and a step counter $t$ shared by all parameters. At step
$t = 1, 2, \dots$:
$$m \leftarrow \beta_1 m + (1-\beta_1) g,\qquad v \leftarrow \beta_2 v + (1-\beta_2) g^2,$$
$$\hat m = \frac{m}{1-\beta_1^t},\qquad \hat v = \frac{v}{1-\beta_2^t},\qquad
  \theta \leftarrow \theta - \text{lr}\,\frac{\hat m}{\sqrt{\hat v} + \epsilon}.$$
* **Bias correction**: because $m$ and $v$ start at 0 they are too small early on; dividing by
  $1-\beta^t$ fixes that. At $t = 1$, $\hat m = g$ and $\hat v = g^2$, so the first step is
  $\text{lr}\cdot g/(|g| + \epsilon) \approx \text{lr}\cdot\operatorname{sign}(g)$.
* Multiplying all gradients by a constant leaves the steps (almost) unchanged — Adam is
  scale-invariant, unlike plain SGD.
* Defaults from the paper: $\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$.

## Worked example
$g = 4$, lr $= 0.1$, first step: $m = 0.4$, $v = 0.016$, $\hat m = 4$, $\hat v = 16$, step
$= 0.1 \cdot 4/(4 + 10^{-8}) \approx 0.1$.

## Common mistakes
* Incrementing $t$ once per parameter instead of once per `step` call.
* Forgetting bias correction, giving tiny early steps.
* Putting $\epsilon$ inside the square root (a different, but common, variant; the paper puts it
  outside).

## Why this matters
Adam (and its variant AdamW) trains most transformers and CNNs; knowing its update explains
learning-rate choices and warm-up schedules.

## Library implementation

`torch.optim.Adam(parameters, lr=..., betas=(0.9, 0.999), eps=1e-8)` implements the same update
(with ε outside the square root). In PyTorch the optimiser modifies tensors in place after
`loss.backward()`; here the dictionary interface makes each step explicit. The comparison below
runs only when PyTorch is installed.

## References

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980) — Kingma & Ba (`S095`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
