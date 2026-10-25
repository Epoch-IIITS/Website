r"""Reference solution for NL-14 Multinomial Naive Bayes Text Classifier.

Training reduces to counting: class frequencies give priors, and smoothed per-class term counts
give word probabilities, all stored as logs. Prediction is a matrix product of counts with log
probabilities plus log priors, normalised with log-sum-exp; argmax picks the most probable class.
"""
import numpy as np


class MultinomialNB:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        X = np.asarray(X, dtype=float)
        y = np.asarray(y)
        self.classes_ = np.unique(y)
        V = X.shape[1]
        priors, flp = [], []
        for c in self.classes_:
            Xc = X[y == c]
            priors.append(np.log(len(Xc) / len(X)))
            Nc = Xc.sum(axis=0)
            flp.append(np.log((Nc + self.alpha) / (Nc.sum() + self.alpha * V)))
        self.class_log_prior_ = np.array(priors)
        self.feature_log_prob_ = np.array(flp)
        return self

    def predict_log_proba(self, X):
        J = np.asarray(X, dtype=float) @ self.feature_log_prob_.T + self.class_log_prior_
        m = J.max(axis=1, keepdims=True)
        return J - (m + np.log(np.exp(J - m).sum(axis=1, keepdims=True)))

    def predict(self, X):
        return self.classes_[self.predict_log_proba(X).argmax(axis=1)]
