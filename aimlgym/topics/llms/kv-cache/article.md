# The KV Cache

## Learning outcomes

After this lesson you can:

- Cache keys and values of past tokens
- Compute attention for one new token at a time
- Prove the cached result equals full causal attention

## Intuition
When generating token 100, a naive loop recomputes keys and values for tokens 1–99 — which haven't
changed. Store them once and only compute the new token's query, key and value each step.

## Precise explanation
With causal attention, the output at position t depends only on $q_t$ and $k_{0..t}, v_{0..t}$.
Each step:
1. $q_t = x_tW_q$, $k_t = x_tW_k$, $v_t = x_tW_v$.
2. Append $k_t, v_t$ to the cache (shapes grow `(t+1, d)`).
3. $o_t = \text{softmax}(q_tK^\top/\sqrt d)\,V$ using all cached rows.
Total work for T steps drops from $O(T^3)$-ish recomputation to $O(T^2)$, at the cost of memory
that grows linearly with context length — the reason long-context LLM serving is memory-bound.
Correctness check: stacking the $o_t$ must equal full causal attention over the whole sequence.

## Worked example
After 3 steps the cache holds 3 key rows and 3 value rows; step 4 computes 1 query, 1 key, 1 value
and attends over 4 rows.

## Common mistakes
* Recomputing keys of old tokens with new weights or new inputs.
* Forgetting the √d scale.
* Letting the new token attend only to the past (it must include itself).

## Why this matters
KV caching is a core optimisation in LLM inference servers.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
