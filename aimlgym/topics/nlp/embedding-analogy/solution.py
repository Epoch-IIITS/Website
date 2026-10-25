r"""Reference solution for NL-18 Word Embedding Analogies.

A shared ranking helper scores candidates by cosine with a target vector, excluding given words,
and sorts by score then name. Similarity search uses the word's own vector; analogies use the
3CosAdd offset vector.
"""
import numpy as np


def _cos(u, v):
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu == 0 or nv == 0:
        return 0.0
    return float(u @ v / (nu * nv))


def _rank(target, emb, exclude):
    scored = [(w, _cos(target, v)) for w, v in emb.items() if w not in exclude]
    return sorted(scored, key=lambda t: (-t[1], t[0]))


def most_similar(word, emb, k=3):
    if word not in emb:
        raise KeyError(word)
    return _rank(emb[word], emb, {word})[:k]


def analogy(a, b, c, emb):
    for w in (a, b, c):
        if w not in emb:
            raise KeyError(w)
    ranked = _rank(emb[b] - emb[a] + emb[c], emb, {a, b, c})
    if not ranked:
        raise ValueError("no candidate words")
    return ranked[0][0]
