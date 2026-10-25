r"""Reference solution for NL-07 Bag-of-Words Vectors.

Counting all tokens once gives total frequencies for the `min_count` filter; sorting fixes the
column order. Vectorisation looks each token up and increments its column, skipping OOV words.
"""
from collections import Counter

import numpy as np


def build_vocab(docs, min_count=1):
    c = Counter(t for doc in docs for t in doc)
    words = sorted(w for w, k in c.items() if k >= min_count)
    return {w: i for i, w in enumerate(words)}


def vectorize(docs, vocab):
    X = np.zeros((len(docs), len(vocab)), dtype=int)
    for i, doc in enumerate(docs):
        for t in doc:
            j = vocab.get(t)
            if j is not None:
                X[i, j] += 1
    return X
