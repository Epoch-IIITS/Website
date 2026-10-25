r"""Reference solution for ML-19 Regularisation and Hyperparameter Search.

`GridSearchCV` cross-validates the scaled Ridge pipeline for each alpha and refits the winner on
all the data. Negating the scores turns them into MSEs. Refitting each alpha on the full data shows
the shrinkage directly: the coefficient norm can only fall as the penalty grows.
"""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def tune_ridge(X, y, alphas, n_splits=5, seed=0):
    if not alphas or any(a <= 0 for a in alphas):
        raise ValueError("alphas must be positive")
    pipe = make_pipeline(StandardScaler(), Ridge())
    search = GridSearchCV(pipe, {"ridge__alpha": list(alphas)},
                          cv=KFold(n_splits, shuffle=True, random_state=seed),
                          scoring="neg_mean_squared_error")
    search.fit(X, y)
    norms = []
    for a in alphas:
        fitted = make_pipeline(StandardScaler(), Ridge(alpha=a)).fit(X, y)
        norms.append(float(np.linalg.norm(fitted[-1].coef_)))
    return {"best_alpha": float(search.best_params_["ridge__alpha"]), "best_mse": float(-search.best_score_),
            "mse_by_alpha": [float(v) for v in -search.cv_results_["mean_test_score"]],
            "coef_norms": norms, "model": search.best_estimator_}
