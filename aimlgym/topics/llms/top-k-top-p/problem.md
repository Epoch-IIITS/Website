# LM-13 · Top-k and Top-p Filtering

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** LM-03 Logits, Temperature and Softmax

Read the lesson first: [article.md](article.md)

## Task

For a 1-D probability array `p` (non-negative, sums to 1):
* `top_k_filter(p, k)` → renormalised array keeping the k largest (ties → lower index);
  `1 <= k <= len(p)` else `ValueError`.
* `top_p_filter(p, top_p)` → renormalised nucleus; `0 < top_p <= 1` else `ValueError`.
* `sample(p, u)` → int index: first i with `cumsum(p)[i] > u`, for `0 <= u < 1` (if rounding leaves
  no such i, return the last index with `p > 0`).

**Examples**
```python
p = np.array([0.5, 0.2, 0.15, 0.1, 0.05])
top_k_filter(p, 2)     # [0.7143, 0.2857, 0, 0, 0]
top_p_filter(p, 0.8)   # [0.5882, 0.2353, 0.1765, 0, 0]
sample(p, 0.6)         # 1
```

## Hints

<details><summary>Hint 1</summary>

`order = np.argsort(-p, kind='stable')`; keep `order[:k]`.

</details>

<details><summary>Hint 2</summary>

For top-p: `c = np.cumsum(p[order])`; `n_keep = int(np.searchsorted(c, top_p) + 1)` (cap at len).

</details>

<details><summary>Hint 3</summary>

Sampling: `np.searchsorted(np.cumsum(p), u, side='right')`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_top_p` | Keep the smallest prefix whose cumulative probability is >= top_p (include the crossing token). |
| `test_top_p_exact_boundary` | Floating-point sums like 0.5+0.2 may be 0.7000000000000001; use a tiny tolerance. |
| `test_order_preserved` | Return probabilities in original vocabulary order. |
| `test_sample` | Return the first index whose cumulative probability is > u. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

A stable descending argsort gives the ranking. Top-k keeps a fixed prefix; top-p finds the first
prefix whose cumulative mass reaches the threshold (a tiny tolerance absorbs rounding such as
0.5 + 0.2 + 0.15 being slightly below 0.85) and keeps it. Both renormalise in vocabulary order.
Sampling inverts the CDF with `searchsorted`.

## References

- [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) — Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi (`S021`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
