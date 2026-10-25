r"""Reference solution for LM-11 A Transformer Block as nn.Module.

Each sub-layer reads a normalised copy of the residual stream and adds its result back. The boolean
upper-triangular mask blocks attention to later positions. Using PyTorch's attribute names makes the
block weight-compatible with `nn.TransformerEncoderLayer` in pre-norm mode.
"""
import torch
import torch.nn.functional as F
from torch import nn


class TransformerBlock(nn.Module):
    def __init__(self, d_model, n_heads):
        super().__init__()
        if d_model % n_heads != 0:
            raise ValueError("d_model must be divisible by n_heads")
        self.norm1 = nn.LayerNorm(d_model)
        self.self_attn = nn.MultiheadAttention(d_model, n_heads, dropout=0.0, batch_first=True)
        self.norm2 = nn.LayerNorm(d_model)
        self.linear1 = nn.Linear(d_model, 4 * d_model)
        self.linear2 = nn.Linear(4 * d_model, d_model)

    def forward(self, x, causal=True):
        T = x.shape[1]
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1) if causal else None
        h = self.norm1(x)
        a, _ = self.self_attn(h, h, h, attn_mask=mask, need_weights=False)
        x = x + a
        return x + self.linear2(F.gelu(self.linear1(self.norm2(x))))
