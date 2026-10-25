# LM-11 · A Transformer Block as nn.Module

**Topic:** Large Language Models · **Difficulty:** intermediate · **Allowed packages:** torch

**Builds on:** LM-10 Multi-Head Attention, DL-06 Models with nn.Module

Read the lesson first: [article.md](article.md)

## Task

Write `class TransformerBlock(nn.Module)` with `__init__(self, d_model, n_heads)` creating exactly
these attributes:

* `self.norm1`, `self.norm2`: `nn.LayerNorm(d_model)`;
* `self.self_attn`: `nn.MultiheadAttention(d_model, n_heads, dropout=0.0, batch_first=True)`;
* `self.linear1`: `nn.Linear(d_model, 4 * d_model)`; `self.linear2`: `nn.Linear(4 * d_model, d_model)`.

`forward(self, x, causal=True)` computes the pre-norm block from the lesson with `F.gelu`, using the
causal mask when `causal` is true and no mask otherwise. Raise `ValueError` in `__init__` if
`d_model` is not divisible by `n_heads`.

## Hints

<details><summary>Hint 1</summary>

Check `d_model % n_heads == 0` before creating the layers.

</details>

<details><summary>Hint 2</summary>

`T = x.shape[1]`; `mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1) if causal else None`.

</details>

<details><summary>Hint 3</summary>

Attention returns `(output, weights)`; add the output to x, then add the MLP of `norm2(x)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_causal` | The mask is True above the diagonal: torch.triu(ones, diagonal=1). |
| `test_matches_encoder_layer` | Use pre-norm order, GELU and the attribute names norm1, self_attn, norm2, linear1, linear2. |
| `test_parameter_count` | The MLP hidden layer is 4 × d_model wide. |
| `test_invalid_heads` | Raise ValueError when d_model is not divisible by n_heads. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Each sub-layer reads a normalised copy of the residual stream and adds its result back. The boolean
upper-triangular mask blocks attention to later positions. Using PyTorch's attribute names makes the
block weight-compatible with `nn.TransformerEncoderLayer` in pre-norm mode.

## References

- [torch.nn.TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html) — PyTorch (`S129`)
- [nanoGPT](https://github.com/karpathy/nanoGPT) — Andrej Karpathy (`S128`)
