# LM-07 · Scaled Dot-Product Attention

**Topic:** Large Language Models · **Difficulty:** intermediate · **Allowed packages:** numpy

**Builds on:** LM-03 Logits, Temperature and Softmax, NP-06 Matrix Products with @

Read the lesson first: [article.md](article.md)

## Task

Write `attention(Q, K, V, mask=None)` returning `(output, weights)`.
* `mask` (optional) is a boolean array broadcastable to `(T_q, T_k)`; False entries get −∞ scores.
* Every query row must have at least one allowed key, else `ValueError`.
* Raise `ValueError` on incompatible shapes.

**Example**
```python
out, w = attention(np.array([[1., 0.]]), np.array([[1., 0.], [0., 1.]]), np.array([[1., 2.], [3., 4.]]))
w     # [[0.6698, 0.3302]]
out   # [[1.6605, 2.6605]]
```

## Hints

<details><summary>Hint 1</summary>

`scores = Q @ K.T / np.sqrt(Q.shape[-1])`.

</details>

<details><summary>Hint 2</summary>

`scores = np.where(mask, scores, -np.inf)`; check `mask.any(axis=1)` for every row.

</details>

<details><summary>Hint 3</summary>

Stable row softmax, then `weights @ V`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_scaling` | Divide scores by sqrt(d_k). |
| `test_rows_sum_one` | Softmax over the key axis (axis=1). |
| `test_mask` | Set disallowed scores to −inf *before* softmax. |
| `test_all_masked_row` | Raise ValueError if a query has no allowed keys. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

Scores compare every query with every key, scaled by √d. Masked positions become −∞ so their
softmax weight is exactly 0. A stable row-wise softmax gives attention weights, which mix the value
vectors.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
