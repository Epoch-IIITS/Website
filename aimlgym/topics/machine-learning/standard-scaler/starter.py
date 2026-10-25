import numpy as np


class StandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        # TODO
        return self

    def transform(self, X):
        # TODO
        pass

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        # TODO
        pass
