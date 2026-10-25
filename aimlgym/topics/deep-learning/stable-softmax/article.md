# Softmax

## Learning outcomes

After this lesson you can:

- Compute softmax along an axis
- Use the max-subtraction trick to avoid overflow
- Compute log-softmax stably

## Intuition
Softmax turns a vector of arbitrary scores (logits) into probabilities: exponentiate (all
positive), divide by the total (sum to 1). Bigger scores get exponentially more probability.

## Precise explanation
$$\text{softmax}(z)_i = \frac{e^{z_i}}{\sum_j e^{z_j}}.$$
**Shift invariance:** adding a constant $c$ to every $z_i$ doesn't change the result. Choose
$c = -\max_j z_j$ so the largest exponent is $e^0 = 1$ — no overflow, and at least one term in
the denominator is 1 (no division by zero).
**Log-softmax:** $\log\text{softmax}(z)_i = z_i - \text{logsumexp}(z)$ with
$\text{logsumexp}(z) = m + \log\sum_j e^{z_j - m}$, $m = \max z$. Computing `log(softmax(z))`
directly can give `log(0) = -inf` for very negative logits.

For a batch `(n, K)`, apply along `axis=-1` (each row separately) and use `keepdims=True`.

## Worked example
z = [1, 2, 3] → shifted [−2, −1, 0] → e = [0.135, 0.368, 1] → sum 1.503 → [0.090, 0.245, 0.665].
z = [1000, 1001] gives the same as [0, 1]: [0.269, 0.731].

## Common mistakes
* `np.exp(1000)` → inf → NaN probabilities.
* Normalising over the wrong axis (columns instead of rows).
* Forgetting `keepdims`, causing a broadcasting error.

## Why this matters
Softmax is the output layer of every classifier and the attention weights of transformers
(LM-07).

## Library implementation

`scipy.special.softmax` and `scipy.special.log_softmax` (and `torch.softmax` /
`torch.log_softmax`) implement the same max-subtraction trick along any axis.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
