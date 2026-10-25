# Top-k and Nucleus Sampling

## Learning outcomes

After this lesson you can:

- Restrict sampling to the top-k tokens
- Implement nucleus (top-p) filtering
- Sample deterministically from a distribution with inverse-CDF

## Intuition
Sampling from the full distribution occasionally picks absurd low-probability tokens. Truncating to
the most likely candidates keeps diversity while cutting off the unreliable tail.

## Precise explanation
* **Top-k:** keep the k most probable tokens (ties → lower index), zero the rest, renormalise.
* **Top-p (nucleus; Holtzman et al., 2019):** sort probabilities descending and keep the smallest
  prefix whose cumulative probability is **≥ p**; renormalise. The nucleus adapts: small when the
  model is confident, large when it is unsure. Always keep at least one token.
* **Sampling with a uniform number u ∈ [0, 1):** return the first index whose cumulative probability
  exceeds u (inverse CDF). Passing u explicitly makes tests deterministic; in practice
  `u = rng.random()`.

## Worked example
p = [0.5, 0.2, 0.15, 0.1, 0.05]; top-k 2 → [0.714, 0.286, 0, 0, 0]. top-p 0.8 → cumulative
0.5, 0.7, 0.85 ≥ 0.8 → keep 3 → [0.588, 0.235, 0.176, 0, 0]. sample(u = 0.6) on the original p → index 1
(cumulative 0.5 ≤ 0.6 < 0.7).

## Common mistakes
* Forgetting to renormalise.
* Off-by-one in top-p: include the token that crosses the threshold.
* Sorting and then returning probabilities in sorted order (they must stay aligned with the vocabulary).

## Why this matters
Top-k, top-p and temperature (LM-03) are the knobs exposed by LLM APIs and libraries.

## References

- [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) — Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi (`S021`)
- [LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) — Hugging Face (`S022`)
