r"""Reference solution for NL-11 Cosine Similarity Retrieval.

Normalising rows turns dot products into cosines; zero rows remain zero so their cosines are 0.
The query's scores against all documents are ranked with a stable descending sort.
"""
import numpy as np


def _normalise_rows(M):
    M = np.asarray(M, dtype=float)
    n = np.linalg.norm(M, axis=1, keepdims=True)
    return np.divide(M, n, out=np.zeros_like(M), where=n > 0)


def cosine_matrix(A, B):
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    if A.shape[1] != B.shape[1]:
        raise ValueError("dimension mismatch")
    return _normalise_rows(A) @ _normalise_rows(B).T


def search(query_vec, doc_matrix, k):
    D = np.atleast_2d(doc_matrix)
    if not 1 <= k <= D.shape[0]:
        raise ValueError("k out of range")
    scores = cosine_matrix(np.atleast_2d(query_vec), D)[0]
    order = np.argsort(-scores, kind="stable")[:k]
    return [(int(i), float(scores[i])) for i in order]
