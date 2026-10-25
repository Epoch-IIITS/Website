r"""Reference solution for NL-05 Character n-grams with CountVectorizer.

`char_wb` pads every word with spaces and counts the n-grams inside it. Fitting both strings in one
vectorizer guarantees that their count vectors share columns, so the cosine similarity compares like
with like.
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def char_ngrams(texts, n_min=2, n_max=3):
    if n_min < 1 or n_min > n_max:
        raise ValueError("need 1 <= n_min <= n_max")
    vec = CountVectorizer(analyzer="char_wb", ngram_range=(n_min, n_max))
    X = vec.fit_transform(texts)
    return [str(f) for f in vec.get_feature_names_out()], X.toarray().tolist()


def char_similarity(a, b, n=3):
    if n < 1:
        raise ValueError("n must be at least 1")
    X = CountVectorizer(analyzer="char_wb", ngram_range=(n, n)).fit_transform([a, b])
    return float(cosine_similarity(X[0], X[1])[0, 0])
