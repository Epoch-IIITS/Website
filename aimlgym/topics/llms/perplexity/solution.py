r"""Reference solution for LM-05 Perplexity.

The average negative log-probability is the per-token cross-entropy; exponentiating gives
perplexity. Zero probabilities make the log undefined, so infinity is returned explicitly.
"""
import math


def avg_nll(token_probs):
    if not token_probs:
        raise ValueError("need at least one probability")
    if any(not 0 <= p <= 1 for p in token_probs):
        raise ValueError("probabilities must be in [0, 1]")
    if any(p == 0 for p in token_probs):
        return math.inf
    return -sum(math.log(p) for p in token_probs) / len(token_probs)


def perplexity(token_probs):
    nll = avg_nll(token_probs)
    return math.inf if math.isinf(nll) else math.exp(nll)
