# Activation Functions

## Learning outcomes

After this lesson you can:

- Implement ReLU, leaky ReLU and tanh
- Implement their derivatives
- Explain why non-linear activations are necessary

## Intuition
Stacking linear layers gives… another linear layer: $W_2(W_1x) = (W_2W_1)x$. Non-linear
**activations** between layers let networks bend and fold space, so they can model curves,
XOR and images.

## Precise explanation
| name | $f(z)$ | $f'(z)$ |
|---|---|---|
| ReLU | $\max(0, z)$ | 1 if $z>0$ else 0 |
| Leaky ReLU | $z$ if $z>0$ else $\alpha z$ | 1 if $z>0$ else $\alpha$ |
| tanh | $\tanh z$ | $1-\tanh^2 z$ |
| sigmoid | $\sigma(z)$ (ML-11) | $\sigma(z)(1-\sigma(z))$ |

ReLU is not differentiable at 0; frameworks use the convention $f'(0) = 0$, and so do we.
Leaky ReLU keeps a small slope for negatives, avoiding "dead" units that never activate.
tanh is zero-centred with range (−1, 1); its gradient vanishes for large $|z|$.

<svg xmlns="http://www.w3.org/2000/svg" width="300" height="160" viewBox="0 0 300 160" role="img" aria-label="Plots of ReLU (a hinge at zero) and tanh (an S-curve between minus one and one)">
<title>ReLU and tanh</title>
<line x1="10" y1="80" x2="290" y2="80" stroke="#bbb"/><line x1="150" y1="10" x2="150" y2="150" stroke="#bbb"/>
<polyline points="20,80 150,80 220,10" fill="none" stroke="#1f77b4" stroke-width="2.5"/>
<path d="M 20 125 C 110 125, 120 80, 150 80 S 190 35, 280 35" fill="none" stroke="#d62728" stroke-width="2.5"/>
<text x="225" y="22" font-size="12" fill="#1f77b4">ReLU</text><text x="240" y="52" font-size="12" fill="#d62728">tanh</text>
</svg>

*Figure (original): ReLU (blue) is a hinge; tanh (red) saturates at ±1 (vertical scale differs).*

## Worked example
z = [−2, 0, 3]: ReLU [0, 0, 3]; ReLU′ [0, 0, 1]; leaky (α = 0.1) [−0.2, 0, 3]; tanh′(0) = 1.

## Common mistakes
* `np.maximum(z, 0)` is right; `max(z, 0)` (Python) fails on arrays.
* Computing tanh′ as `1 - z**2` instead of `1 - tanh(z)**2`.
* In-place modification of the input array.

## Why this matters
Activations and their derivatives are the per-layer ingredients of backpropagation (DL-10, DL-19).

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
