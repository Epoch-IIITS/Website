# LM-09 · Sinusoidal Positional Encoding

**Topic:** Large Language Models · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** LM-07 Scaled Dot-Product Attention

Read the lesson first: [article.md](article.md)

## Task

Write `positional_encoding(T, d)` returning a float array `(T, d)` per the formula (positions
`0..T-1`). Raise `ValueError` if `T < 1`, `d < 2`, or `d` is odd. No Python loops over positions are
required (vectorise if you can).

**Example**
```python
pe = positional_encoding(2, 4)
pe[0]   # [0., 1., 0., 1.]
pe[1]   # [0.84147, 0.54030, 0.01000, 0.99995]
```

## Hints

<details><summary>Hint 1</summary>

`pos = np.arange(T)[:, None]`; `i = np.arange(d // 2)[None, :]`.

</details>

<details><summary>Hint 2</summary>

`angles = pos / 10000 ** (2 * i / d)`.

</details>

<details><summary>Hint 3</summary>

`pe[:, 0::2] = np.sin(angles)`; `pe[:, 1::2] = np.cos(angles)`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_pos1` | Exponent is 2i/d with i indexing dimension *pairs*. |
| `test_pos0` | Sines go in even columns, cosines in odd columns. |
| `test_relative_rotation` | Use the exact frequencies 1/10000^(2i/d). |
| `test_errors` | Reject odd d. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A `(T, d/2)` grid of angles is built by broadcasting positions against frequencies; sines fill even
columns and cosines odd columns.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
