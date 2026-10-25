# Temperature

## Learning outcomes

After this lesson you can:

- Convert logits to probabilities with temperature
- Measure distribution sharpness with entropy
- Explain the T → 0 and T → ∞ limits

## Intuition
Temperature is a "creativity knob". Dividing logits by T before softmax sharpens (T < 1) or
flattens (T > 1) the distribution. Low T → confident, repetitive text; high T → diverse, sometimes
nonsensical text.

## Precise explanation
$$p_i(T) = \frac{e^{z_i/T}}{\sum_j e^{z_j/T}},\qquad T > 0.$$
* T = 1: ordinary softmax.
* T → 0: all mass on the argmax (greedy decoding, LM-04).
* T → ∞: uniform.
Ranking of tokens never changes — only how peaked the distribution is.
**Entropy** $H(p) = -\sum p_i \log p_i$ (nats; terms with $p_i = 0$ contribute 0) measures
spread: 0 for one-hot, $\log V$ for uniform. Entropy increases with T.

## Worked example
z = [2, 1, 0]: T = 1 → [0.665, 0.245, 0.090]; T = 0.5 → [0.867, 0.117, 0.016];
T = 10 → ≈ [0.367, 0.332, 0.301].

## Common mistakes
* Multiplying instead of dividing by T.
* Allowing T = 0 (division by zero) — treat greedy decoding separately.
* Computing entropy with `log(0)` → NaN.

## Why this matters
Temperature is a standard generation setting in LLM APIs and interacts with top-k/top-p
filtering (LM-13).

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) — Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi (`S021`)
