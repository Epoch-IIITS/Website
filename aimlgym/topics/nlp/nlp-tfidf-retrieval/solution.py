r"""Reference solution for NL-10 Search with TfidfVectorizer and Cosine Similarity.

The index stores the fitted vectorizer and the document matrix. A query is transformed with the
same vocabulary and IDF; cosine similarity scores it against every document, and a stable sort
returns the best matches first.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_index(docs):
    if not docs:
        raise ValueError("need at least one document")
    vec = TfidfVectorizer()
    return vec, vec.fit_transform(docs)


def search(index, query, k=3):
    if k < 1:
        raise ValueError("k must be at least 1")
    vec, matrix = index
    scores = cosine_similarity(vec.transform([query]), matrix)[0]
    order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))[:k]
    return [(i, float(scores[i])) for i in order]
