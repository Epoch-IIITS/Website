# The Dense (Fully Connected) Layer

## Learning outcomes

After this lesson you can:

- Compute XW + b for a batch
- Check layer shapes
- Count parameters and initialise weights

## Intuition
A dense layer is many linear models side by side: each output unit is a weighted sum of all
inputs plus a bias. For a batch of inputs this is one matrix product.

## Precise explanation
Input $X$ `(n, d_in)`, weights $W$ `(d_in, d_out)`, bias $b$ `(d_out,)`:
$$Y = XW + b \quad\text{shape } (n, d_\text{out}),$$
with $b$ broadcast over rows (NP-07). Parameters: $d_\text{in} d_\text{out} + d_\text{out}$.
For layer sizes $[d_0, d_1, \dots, d_L]$ the total is $\sum_l (d_{l-1}+1)d_l$.

**Initialisation:** all-zero weights make every unit identical forever (symmetry). **He
initialisation** for ReLU networks draws $W \sim \mathcal N(0, 2/d_\text{in})$ so activations keep
roughly constant variance across layers; biases start at 0.

## Worked example
X = [[1, 2]], W = [[1, 0, −1], [2, 1, 0]], b = [0.5, 0, 0] → Y = [[5.5, 2, −1]].
Layers [784, 128, 10]: (784+1)·128 + (128+1)·10 = 100 480 + 1 290 = 101 770 parameters.

## Common mistakes
* `W @ X` instead of `X @ W` (row-vector convention used here).
* Bias with shape `(n,)` instead of `(d_out,)`.
* Initialising all weights to the same constant.

## Why this matters
Dense layers make up MLPs (DL-07), transformer feed-forward blocks and classifier heads.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/) — free online book (author not stated on landing page) (`S014`)
