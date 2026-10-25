r"""Reference solution for NL-15 A Text Classification Pipeline.

The pipeline learns the vocabulary and the weights together from raw text. For a binary model each
coefficient belongs to one word or word pair; sorting them shows the phrases that most strongly
indicate each class.
"""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def train_text_classifier(texts, labels, C=1.0):
    if len(texts) != len(labels) or len(set(labels)) < 2:
        raise ValueError("need matching texts and labels with at least two classes")
    pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
                     ("clf", LogisticRegression(C=C, max_iter=1000))])
    return pipe.fit(texts, labels)


def top_features(pipe, n=5):
    names = pipe.named_steps["tfidf"].get_feature_names_out()
    weights = pipe.named_steps["clf"].coef_[0]
    order = np.argsort(weights, kind="stable")
    return {"positive": [str(names[i]) for i in order[::-1][:n]],
            "negative": [str(names[i]) for i in order[:n]]}
