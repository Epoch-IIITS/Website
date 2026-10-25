# LM-12 · A Pre-Norm Transformer Block by Hand

**Topic:** Large Language Models · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** LM-10 Multi-Head Attention, LM-09 Sinusoidal Positional Encoding

Read the lesson first: [article.md](article.md)

## Task

The starter provides a working `multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal)` (from
LM-10). Implement:

1. `layer_norm(x, gamma, beta, eps=1e-5)` over the last axis.
2. `feed_forward(x, W1, b1, W2, b2)` with ReLU.
3. `transformer_block(x, params, h)` — the pre-norm block with **causal** attention. `params`
   has keys `ln1_g, ln1_b, Wq, Wk, Wv, Wo, ln2_g, ln2_b, W1, b1, W2, b2`. Return shape `(T, d)`.

## Hints

<details><summary>Hint 1</summary>

`mu = x.mean(axis=-1, keepdims=True)`, `var = x.var(axis=-1, keepdims=True)`, then `gamma * (x - mu) / np.sqrt(var + eps) + beta`.

</details>

<details><summary>Hint 2</summary>

`np.maximum(x @ W1 + b1, 0) @ W2 + b2`.

</details>

<details><summary>Hint 3</summary>

`a = layer_norm(x, p["ln1_g"], p["ln1_b"])`; `h1 = x + multi_head_attention(a, p["Wq"], ..., h, causal=True)`; then the same pattern with LN2 and the FFN.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_layer_norm_stats` | Normalise along the last axis with the population variance (`x.var(axis=-1)`). |
| `test_feed_forward` | Apply ReLU between the two linear maps. |
| `test_zero_sublayers_identity` | Add each sub-layer's output to its input (residual connections). |
| `test_shape_and_reference` | Pre-norm: normalise *before* each sub-layer and use causal attention. |
| `test_causal` | Pass `causal=True` to the attention so later tokens cannot affect earlier outputs. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Layer norm standardises each token's feature vector with its own mean and population variance.
The block applies "normalise → sub-layer → add back the input" twice: once with causal
multi-head attention, once with the feed-forward network. Because every operation either works
row by row or uses a causal mask, output row t never sees input rows after t.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Layer Normalization](https://arxiv.org/abs/1607.06450) — Ba, Kiros & Hinton (`S096`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
