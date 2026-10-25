# A Pre-Norm Transformer Block

## Learning outcomes

After this lesson you can:

- Implement layer normalisation over the feature axis
- Write the position-wise feed-forward network
- Assemble attention and feed-forward sub-layers with residual connections
- Verify causality: earlier outputs do not depend on later tokens

## Intuition
A transformer is a stack of identical **blocks**. Each block lets every token gather information
from earlier tokens (attention, LM-10) and then transforms each token on its
own (a small feed-forward network). Two tricks make deep stacks trainable: **residual
connections** (add the input back to each sub-layer's output) and **layer normalisation** (keep
each token's features at a stable scale).

## Precise explanation
For `x` of shape `(T, d)`:

**Layer norm** normalises each row (token) over its `d` features, then rescales:
$$\mathrm{LN}(x)_t = \gamma \odot \frac{x_t - \mu_t}{\sqrt{\sigma_t^2 + \epsilon}} + \beta,$$
with $\mu_t, \sigma_t^2$ the mean and population variance of row $t$; $\gamma, \beta \in \mathbb R^d$.
Unlike batch norm (DL-23) it does not depend on other examples in the batch.

**Feed-forward**: $\mathrm{FFN}(x) = \mathrm{ReLU}(xW_1 + b_1)W_2 + b_2$ with $W_1$ of shape
$(d, d_{ff})$ (often $d_{ff} = 4d$). (GPT-style models use GELU instead of ReLU.)

**Pre-norm block** (used by GPT-2 and most modern LLMs):
$$h = x + \mathrm{MHA}(\mathrm{LN}_1(x)), \qquad y = h + \mathrm{FFN}(\mathrm{LN}_2(h)).$$
With causal attention, output row $t$ depends only on input rows $0..t$.

## Worked example
If every weight in the attention and feed-forward sub-layers is zero, both sub-layers output
zero and the block returns `x` unchanged — the residual path. Training starts close to this
"identity" behaviour, which is why deep stacks remain stable.

## Common mistakes
* Normalising over the sequence axis (axis 0) instead of features (axis −1).
* Using the sample variance (`ddof=1`); layer norm uses the population variance.
* Post-norm vs pre-norm confusion: the original paper applied LN *after* adding the residual.
* Forgetting the residual additions.

## Why this matters
This block, repeated dozens of times with an embedding table before it and a vocabulary
projection after it, is a GPT-style language model.

## Library implementation

PyTorch provides the pieces as `torch.nn.LayerNorm(d)` (with `eps=1e-5` and population variance,
exactly your formula), `torch.nn.MultiheadAttention` and `torch.nn.TransformerEncoderLayer(...,
norm_first=True)` for a pre-norm block. Comparing whole blocks requires matching PyTorch's packed
weight layout, so the test below checks only layer norm; it runs when PyTorch is installed.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Layer Normalization](https://arxiv.org/abs/1607.06450) — Ba, Kiros & Hinton (`S096`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
