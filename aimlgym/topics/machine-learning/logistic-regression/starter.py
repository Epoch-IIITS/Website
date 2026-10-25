import numpy as np


def sigmoid(z):
    # TODO
    pass


def log_loss(y, p, eps=1e-12):
    # TODO
    pass


class LogisticRegression:
    def __init__(self, lr=0.1, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.w_ = None
        self.b_ = None
        self.history_ = []

    def fit(self, X, y):
        # TODO
        return self

    def predict_proba(self, X):
        # TODO
        pass

    def predict(self, X, threshold=0.5):
        # TODO
        pass
