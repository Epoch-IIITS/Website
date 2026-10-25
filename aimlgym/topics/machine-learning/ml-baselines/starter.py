import numpy as np


class MeanRegressor:
    def fit(self, X, y):
        # TODO: store self.mean_
        return self

    def predict(self, X):
        # TODO
        return np.zeros(len(X))


class MajorityClassifier:
    def fit(self, X, y):
        # TODO: store self.label_ (ties -> smallest label)
        return self

    def predict(self, X):
        # TODO
        return np.array([])


def mse(y_true, y_pred):
    # TODO
    return 0.0


def accuracy(y_true, y_pred):
    # TODO
    return 0.0
