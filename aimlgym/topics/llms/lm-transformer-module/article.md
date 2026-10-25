# A Transformer Block as nn.Module

## Learning outcomes

After this lesson you can:

- Build a pre-norm transformer block from nn.MultiheadAttention, LayerNorm and an MLP
- Apply a causal attention mask so positions cannot see the future
- Check the block against nn.TransformerEncoderLayer

## Intuition
A transformer is a stack of identical blocks. Each block lets every position gather information
from the others (attention) and then transforms each position on its own (an MLP). Residual
connections add each sub-layer's output to its input, and layer normalisation keeps the scale
stable — so blocks can be stacked dozens deep.

## Precise explanation
The **pre-norm** block used by GPT-style models:

```python
h = self.norm1(x)
a, _ = self.self_attn(h, h, h, attn_mask=mask, need_weights=False)
x = x + a                                                     # residual
x = x + self.linear2(F.gelu(self.linear1(self.norm2(x))))     # MLP with a 4× wider hidden layer
```

* `nn.MultiheadAttention(d_model, n_heads, batch_first=True)` takes (batch, time, d_model) tensors and
  holds the query/key/value projections for all heads in `in_proj_weight`, plus `out_proj`.
* A **causal** mask is a boolean (T, T) tensor that is `True` above the diagonal:
  `torch.triu(torch.ones(T, T, dtype=torch.bool), diagonal=1)`. `True` means "may not attend".
* `nn.LayerNorm(d_model)` normalises each position's vector; GELU is the usual activation.
* `nn.TransformerEncoderLayer(d_model, n_heads, 4 * d_model, dropout=0.0, activation="gelu",
  batch_first=True, norm_first=True)` is the same block; with the attribute names above its
  `state_dict` loads into yours.

## Worked example
With d_model = 16 and 2 heads, a (2, 5, 16) input gives a (2, 5, 16) output. Changing token 4 changes
the outputs at position 4 only — positions 0–3 cannot see it through the causal mask.

## What the library does inside
`nn.MultiheadAttention` performs the projections, scaled dot products, masking and head
concatenation that you wrote in LM-10; your NumPy LM-12 (the
optional deep dive after this step) is the same computation without autograd.

## Common mistakes
* Forgetting `batch_first=True` and mixing up (time, batch) and (batch, time).
* A mask with `True` on the allowed positions (the meaning is reversed).
* Post-norm ordering by accident (normalising after adding the residual).

## Why this matters
The tiny GPT next stacks these blocks; large language models differ mostly in size.

## References

- [torch.nn.TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html) — PyTorch (`S129`)
- [nanoGPT](https://github.com/karpathy/nanoGPT) — Andrej Karpathy (`S128`)
