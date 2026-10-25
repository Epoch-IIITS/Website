# LM-15 · Incremental Decoding with a KV Cache

**Topic:** Large Language Models · **Difficulty:** advanced · **Allowed packages:** numpy

**Builds on:** LM-08 Causal Masking, LM-10 Multi-Head Attention

Read the lesson first: [article.md](article.md)

## Task

Implement single-head attention (weights `(d, d)`):
* `full_causal_attention(X, Wq, Wk, Wv)` → `(T, d)` outputs with a causal mask.
* `class KVCache(Wq, Wk, Wv)` with attributes `K` and `V` (arrays with 0 rows initially, shape
  `(0, d)`) and `step(x_t)` taking one token vector `(d,)`, appending its key/value and returning its
  output `(d,)`.

**Example**
```python
cache = KVCache(Wq, Wk, Wv)
outs = np.array([cache.step(x) for x in X])
np.allclose(outs, full_causal_attention(X, Wq, Wk, Wv))   # True
cache.K.shape   # (len(X), d)
```

## Hints

<details><summary>Hint 1</summary>

Full: scores `Q @ K.T / sqrt(d)`, mask with `np.tril`, softmax rows, multiply V.

</details>

<details><summary>Hint 2</summary>

Cache init: `self.K = np.zeros((0, d))`; append with `np.vstack([self.K, k_t])`.

</details>

<details><summary>Hint 3</summary>

Step: `s = self.K @ q_t / sqrt(d)`; softmax over s; `w @ self.V`.

</details>

## If a test fails

| Test | What to check |
|---|---|
| `test_matches_full` | Each step must attend over all cached keys including the new one, scaled by sqrt(d). |
| `test_cache_growth` | Start with zero-row arrays of shape (0, d) and append one row per step. |
| `test_first_token_is_own_value` | With one cached token the softmax weight is 1, so output = its value. |
| `test_full_causal_property` | Mask future keys with np.tril in the full version. |

## Worked solution

The reference solution is in `solution.py`. Explanation:

The full version builds all queries, keys and values and masks the future. The cached version
computes projections only for the new token, appends its key and value, and attends over every
cached row — exactly the keys a causal mask would allow — so both give identical outputs.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
