# LM-08 · Causal Masking

**Topic:** Large Language Models · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** LM-07 Scaled Dot-Product Attention

Read the lesson first: [article.md](article.md)

## Task

Implement:
* `causal_mask(T)` → bool `(T, T)` lower triangle with diagonal. `T >= 1` else `ValueError`.
* `padding_mask(lengths, T)` → bool `(B, T)`, True for `j < lengths[b]`; each length in `1..T`.
* `combined_mask(lengths, T)` → bool `(B, T, T)` = causal AND padding-over-keys, **but** with the
  diagonal always True (so padded query rows still have one allowed key).

**Examples**
```python
causal_mask(3)              # [[T,F,F],[T,T,F],[T,T,T]]
padding_mask([2, 3], 3)     # [[T,T,F],[T,T,T]]
combined_mask([2], 3)[0]    # [[T,F,F],[T,T,F],[T,T,T]]  — row 2's own diagonal kept
```

## Hints

<details><summary>Hint 1</summary>

`np.tril(np.ones((T, T), dtype=bool))`.

</details>

<details><summary>Hint 2</summary>

`np.arange(T)[None, :] < np.asarray(lengths)[:, None]`.

</details>

<details><summary>Hint 3</summary>

`causal[None] & pad[:, None, :]`, then OR with `np.eye(T, dtype=bool)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_causal` | Use the lower triangle including the diagonal (np.tril). |
| `test_padding` | Key j is valid iff j < length. |
| `test_combined` | AND the masks over keys, then OR with the identity so the diagonal stays True. |
| `test_no_future_leak` | With a correct causal mask, changing the last token leaves earlier outputs unchanged. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

`tril` builds the causal pattern; comparing positions with lengths builds padding masks by
broadcasting. Their conjunction over keys, plus the diagonal, gives a per-sequence mask in which
every query has at least one allowed key.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
