r"""Reference solution for NL-08 Bigram Counts with Sentence Markers.

Each padded sentence contributes its consecutive pairs; the first token of every pair is also
counted as a context. The MLE probability divides the pair count by the context count, so
probabilities for a context sum to one.
"""
from collections import Counter


def bigram_counts(sentences):
    bigrams, contexts = Counter(), Counter()
    for sent in sentences:
        toks = ["<s>"] + list(sent) + ["</s>"]
        for a, b in zip(toks, toks[1:]):
            bigrams[(a, b)] += 1
            contexts[a] += 1
    return {"bigrams": bigrams, "contexts": contexts}


def bigram_prob(w_prev, w, counts):
    ctx = counts["contexts"].get(w_prev, 0)
    if ctx == 0:
        raise KeyError(w_prev)
    return counts["bigrams"].get((w_prev, w), 0) / ctx
