r"""Reference solution for NL-17 PPMI Co-occurrence Matrix.

Counting walks a symmetric window inside each sentence, skipping the centre and out-of-vocabulary
tokens (which still keep their positions). PPMI converts counts to joint and marginal probabilities
and takes log2 only where counts are positive, clipping negatives to zero.
"""
import numpy as np


def cooccurrence(sentences, vocab, window=2):
    if window < 1:
        raise ValueError("window must be >= 1")
    V = len(vocab)
    C = np.zeros((V, V), dtype=int)
    for s in sentences:
        for i, w in enumerate(s):
            if w not in vocab:
                continue
            for j in range(max(0, i - window), min(len(s), i + window + 1)):
                if j != i and s[j] in vocab:
                    C[vocab[w], vocab[s[j]]] += 1
    return C


def ppmi(C):
    C = np.asarray(C, dtype=float)
    N = C.sum()
    if N == 0:
        raise ValueError("empty co-occurrence matrix")
    P = C / N
    pw = P.sum(axis=1, keepdims=True)
    pc = P.sum(axis=0, keepdims=True)
    denom = pw * pc
    pmi = np.zeros_like(P)
    mask = C > 0
    np.log2(P / np.where(denom > 0, denom, 1.0), out=pmi, where=mask)
    return np.maximum(pmi, 0.0)
