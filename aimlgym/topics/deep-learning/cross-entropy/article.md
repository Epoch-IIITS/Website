# Cross-Entropy Loss

## Learning outcomes

After this lesson you can:

- Compute softmax cross-entropy from logits and integer labels
- Derive its gradient softmax − one_hot
- Verify gradients numerically

## Intuition
If the true class is "cat", the loss should be small when the model gives "cat" high probability
and huge when it confidently says "dog". Cross-entropy is the negative log of the probability
assigned to the correct class.

## Precise explanation
For logits $z \in \mathbb{R}^{n\times K}$ and labels $y_i$:
$$L = -\frac1n\sum_i \log \text{softmax}(z_i)_{y_i}.$$
Compute it with log-softmax (DL-02) and pick the correct entries with fancy indexing (NP-09):
`-log_softmax(z)[np.arange(n), y].mean()`.
**Gradient** (the reason softmax + cross-entropy are paired):
$$\frac{\partial L}{\partial z} = \frac{1}{n}\big(\text{softmax}(z) - \text{one\_hot}(y)\big).$$
Binary log-loss (ML-11) is the K = 2 special case.

## Worked example
One sample, z = [2, 0, −1], y = 0: softmax ≈ [0.844, 0.114, 0.042]; L = −log 0.844 = 0.170;
gradient = [−0.156, 0.114, 0.042].

## Common mistakes
* Taking the log of probabilities that underflowed to 0.
* Using `P[:, y]` instead of `P[np.arange(n), y]`.
* Forgetting to average over the batch (gradient off by a factor n).

## Why this matters
Cross-entropy is the training loss of classifiers and of language models (LM-05 perplexity is
its exponential).

## Library implementation

`torch.nn.functional.cross_entropy(logits, labels)` combines log-softmax and the negative
log-likelihood exactly like your function (mean over the batch), and autograd's gradient equals
`(softmax - one_hot) / n`. The comparison runs when PyTorch is installed.

## References

- [Dive into Deep Learning](https://d2l.ai/) — Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola (`S013`)
- [CS231n: Backpropagation notes](https://cs231n.github.io/optimization-2/) — Stanford University CS231n (`S016`)
