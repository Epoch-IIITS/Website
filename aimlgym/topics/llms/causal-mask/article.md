# Causal and Padding Masks

## Learning outcomes

After this lesson you can:

- Build a lower-triangular causal mask
- Combine causal and padding masks
- Verify that outputs do not depend on future tokens

## Intuition
A language model predicting token t must not peek at tokens after t. The **causal mask** hides the
future: position t may attend only to positions 0..t. A **padding mask** hides filler tokens added to
make sequences in a batch the same length.

## Precise explanation
* Causal mask `M[i, j] = (j <= i)` — lower triangle including the diagonal:
  `np.tril(np.ones((T, T), bool))`.
* Padding mask for a batch with true lengths $L_b$: key position j is valid iff $j < L_b$, shape
  `(B, T)`; broadcast as `(B, 1, T)` over queries.
* Combined `(B, T, T)` = causal AND padding.
With masked scores set to −∞, changing a future token cannot change earlier outputs — testable!

|   | k0 | k1 | k2 |
|---|---|---|---|
| q0 | ✓ | ✗ | ✗ |
| q1 | ✓ | ✓ | ✗ |
| q2 | ✓ | ✓ | ✓ |

## Worked example
T = 3 → [[T, F, F], [T, T, F], [T, T, T]]; lengths [2] → padding [[T, T, F]].

## Common mistakes
* Upper instead of lower triangle (attending only to the future).
* Excluding the diagonal (a token can attend to itself).
* Rows of padding queries that become fully masked under both masks — we keep the causal diagonal
  so every row has at least one allowed key.

## Why this matters
Causal masking is what makes decoder-only transformers (GPT-style) autoregressive and enables
training on all positions of a sequence in parallel.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
