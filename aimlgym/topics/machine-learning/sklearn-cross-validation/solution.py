r"""Reference solution for ML-16 Cross-Validation with scikit-learn.

The splitter defines the folds; `cross_val_score` clones and fits the model once per fold and
returns the held-out scores. The mean is the estimate and the standard deviation shows how much
it moves from fold to fold.
"""
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score


def cv_report(model, X, y, n_splits=5, seed=0, stratified=False, scoring=None):
    if n_splits < 2 or len(X) != len(y):
        raise ValueError("need n_splits >= 2 and matching X and y")
    splitter = StratifiedKFold if stratified else KFold
    folds = splitter(n_splits=n_splits, shuffle=True, random_state=seed)
    scores = np.asarray(cross_val_score(model, X, y, cv=folds, scoring=scoring))
    return {"scores": [float(s) for s in scores], "mean": float(scores.mean()), "std": float(scores.std())}
