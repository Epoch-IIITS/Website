r"""Reference solution for ML-02 The scikit-learn Estimator API.

`clone` copies the settings but not the learned state, so fitting it leaves the caller's model
untouched. Any regressor works because the function relies only on `fit` and `predict`, and the
three metrics come from `sklearn.metrics` with the true values first.
"""
from sklearn.base import clone
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_regressor(model, X_train, y_train, X_test, y_test):
    if len(X_train) != len(y_train) or len(X_test) != len(y_test):
        raise ValueError("X and y must have the same number of rows")
    fitted = clone(model).fit(X_train, y_train)
    pred = fitted.predict(X_test)
    return {"model": fitted, "predictions": [float(v) for v in pred],
            "mse": float(mean_squared_error(y_test, pred)),
            "mae": float(mean_absolute_error(y_test, pred)),
            "r2": float(r2_score(y_test, pred))}
