r"""Reference solution for NL-04 Stopwords and Word Counts.

A set makes stopword checks constant time. `Counter` tallies the remaining tokens and an explicit
sort key gives a stable, deterministic ranking independent of token order.
"""
from collections import Counter


def remove_stopwords(tokens, stopwords):
    sw = set(stopwords)
    return [t for t in tokens if t not in sw]


def top_words(tokens, n, stopwords=()):
    if n < 1:
        raise ValueError("n must be >= 1")
    counts = Counter(remove_stopwords(tokens, stopwords))
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
