r"""Reference solution for NL-09 TF-IDF.

Document frequency counts non-zero entries per column; smoothed IDF follows. Broadcasting
multiplies each column by its IDF, and rows are scaled to unit length, with empty rows left as
zeros via a guarded division.
"""
import numpy as np


def tfidf(counts):
    C = np.asarray(counts, dtype=float)
    if C.ndim != 2 or (C < 0).any():
        raise ValueError("counts must be a non-negative 2-D array")
    n = C.shape[0]
    df = (C > 0).sum(axis=0)
    idf = np.log((1 + n) / (1 + df)) + 1.0
    W = C * idf
    norms = np.linalg.norm(W, axis=1, keepdims=True)
    W = np.divide(W, norms, out=np.zeros_like(W), where=norms > 0)
    return W, idf
