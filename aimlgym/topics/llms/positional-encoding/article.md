# Sinusoidal Positional Encoding

## Learning outcomes

After this lesson you can:

- Implement the sinusoidal encoding from the Transformer paper
- Explain why attention needs positional information
- Check bounded values and relative-position structure

## Intuition
Attention treats its inputs as a *set*: shuffle the tokens and each output is just shuffled too.
To know word order, we add a position-dependent vector to each token embedding.

## Precise explanation (Vaswani et al., 2017)
For position $p$ and dimension index $i$ (with $d$ even):
$$PE[p, 2i] = \sin\!\left(\frac{p}{10000^{2i/d}}\right),\qquad PE[p, 2i+1] = \cos\!\left(\frac{p}{10000^{2i/d}}\right).$$
Each pair of dimensions is a sine/cosine at a different frequency, from fast (i = 0) to very slow.
Values lie in [−1, 1]. For any offset k, $PE[p+k]$ is a fixed linear function (a rotation per
frequency pair) of $PE[p]$, which helps attention reason about relative positions. Many modern LLMs
use learned or rotary (RoPE) encodings instead; the sinusoidal version is the classic starting point.

## Worked example
p = 0: all sines 0, all cosines 1 → [0, 1, 0, 1, …]. p = 1, d = 4: frequencies 1 and 1/100 →
[sin 1, cos 1, sin 0.01, cos 0.01] = [0.841, 0.540, 0.010, 1.000].

## Common mistakes
* Using $i$ instead of $2i$ in the exponent.
* Interleaving incorrectly (sin on odd dimensions).
* Integer division producing zeros.

## Why this matters
Without positional information "dog bites man" and "man bites dog" look identical to a transformer.

## References

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Ashish Vaswani et al. (`S019`)
- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
