# LM-10 · Multi-Head Attention

**Topic:** Large Language Models · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** LM-07 Scaled Dot-Product Attention, LM-08 Causal Masking

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `split_heads(X, h)` → `(h, T, d/h)`; raise `ValueError` if `d % h != 0`.
* `merge_heads(Xh)` → inverse of `split_heads`.
* `multi_head_attention(X, Wq, Wk, Wv, Wo, h, causal=False)` → `(T, d_model)` output following the
  steps above (causal mask from LM-08 when `causal=True`).

All weight matrices are `(d_model, d_model)`.

**Example**
```python
X = np.arange(8.).reshape(2, 4)
split_heads(X, 2)[1]       # [[2., 3.], [6., 7.]]
merge_heads(split_heads(X, 2))   # equals X
```

## Hints

<details><summary>Hint 1</summary>

`X.reshape(T, h, d // h).transpose(1, 0, 2)`.

</details>

<details><summary>Hint 2</summary>

Merge: `Xh.transpose(1, 0, 2).reshape(T, h * dh)`.

</details>

<details><summary>Hint 3</summary>

Batched scores: `Qh @ Kh.transpose(0, 2, 1) / np.sqrt(dh)` → shape `(h, T, T)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_split` | Reshape to (T, h, d_h) and then transpose to (h, T, d_h). |
| `test_h2_manual` | Scale each head's scores by sqrt(d_h), not sqrt(d_model). |
| `test_h1_equals_single` | Remember the output projection Wo. |
| `test_causal` | Apply the causal mask to every head's scores. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Reshape-then-transpose keeps each position's features together while grouping them by head.
Batched matrix products compute all heads' attention at once; merging reverses the split and the
output projection mixes information across heads.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
