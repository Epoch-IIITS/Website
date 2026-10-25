# Next-Token Prediction

## Learning outcomes

After this lesson you can:

- Frame language modelling as next-token prediction
- Apply add-k smoothing
- Return a full distribution over the vocabulary

## Intuition
An LLM is, at its core, a function that maps a context to a probability distribution over the next
token. A bigram model is the simplest such function: the context is just the previous token.

## Precise explanation
With bigram counts $C(\text{prev}, w)$ (NL-08) and vocabulary size $V$, **add-k smoothing** gives
$$P(w\mid\text{prev}) = \frac{C(\text{prev}, w) + k}{\sum_{w'} C(\text{prev}, w') + kV}.$$
* k = 0 is the MLE (zero probability for unseen pairs, undefined for unseen contexts).
* k = 1 is Laplace smoothing; smaller k (0.1, 0.01) usually works better.
* An unseen context gets the uniform distribution $1/V$.
Every distribution must sum to 1 over the whole vocabulary — the same contract an LLM's softmax
output satisfies.

## Worked example
Counts after "like": tea 1, coffee 1; V = 4 ({tea, coffee, i, like}); k = 1:
P(tea) = 2/6, P(coffee) = 2/6, P(i) = 1/6, P(like) = 1/6.

## Common mistakes
* Adding k to the numerator but forgetting kV in the denominator.
* Returning only seen words (the distribution must cover the vocabulary).
* Using a vocabulary that differs between training and evaluation.

## Why this matters
Perplexity (LM-05), sampling (LM-13) and beam search (LM-14) all consume exactly this kind of
next-token distribution.

## References

- [Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/) — Dan Jurafsky, James H. Martin (`S017`)
