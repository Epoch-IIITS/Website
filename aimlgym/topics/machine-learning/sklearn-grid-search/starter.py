import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def tune_ridge(X, y, alphas, n_splits=5, seed=0):
    # TODO
    pass
