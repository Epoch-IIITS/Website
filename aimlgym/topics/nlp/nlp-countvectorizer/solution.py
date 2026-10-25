r"""Reference solution for NL-03 Counting Words with Counter and CountVectorizer.

`Counter` accumulates token frequencies across all texts; sorting on negative count and then the
word gives a deterministic top-k. `CountVectorizer` learns the vocabulary and produces one count row
per document; its feature names are already in column order.
"""
import re
from collections import Counter

from sklearn.feature_extraction.text import CountVectorizer


def top_words(texts, k, stop_words=()):
    if not texts or k < 1:
        raise ValueError("need texts and k >= 1")
    stop = set(stop_words)
    counts = Counter()
    for text in texts:
        counts.update(t for t in re.findall(r"[a-z']+", text.lower()) if t not in stop)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def count_matrix(texts, stop_words=None, min_df=1):
    if not texts:
        raise ValueError("need at least one text")
    vec = CountVectorizer(stop_words=stop_words, min_df=min_df)
    X = vec.fit_transform(texts)
    return [str(w) for w in vec.get_feature_names_out()], X.toarray().tolist()
