# The scikit-learn Estimator API

## Learning outcomes

After this lesson you can:

- Use fit, predict and score on any scikit-learn estimator
- Copy an unfitted estimator with clone and read its settings with get_params
- Evaluate a regressor with sklearn.metrics (MSE, MAE, R²)

## Intuition
In ML-01 you wrote a model that predicts the mean. scikit-learn ships hundreds of
models, and they all speak the same small language: **fit** on training data, **predict** on new
data, **score** to evaluate. Learn the language once and you can swap a baseline for a linear
model or a forest by changing one line.

## Precise explanation
An **estimator** is an object configured by its constructor arguments (hyperparameters) and
trained by `fit`:

```python
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression

model = LinearRegression()          # settings only; nothing learned yet
model.fit(X_train, y_train)         # learns coef_ and intercept_, returns the model itself
y_pred = model.predict(X_test)      # NumPy array of predictions
model.score(X_test, y_test)         # R² for regressors, accuracy for classifiers
```

* `X` is 2-D with shape `(n_samples, n_features)`; `y` is 1-D.
* Learned attributes end in an underscore (`coef_`, `intercept_`); they exist only after `fit`.
* `model.get_params()` returns the constructor settings as a dict; `clone(model)` from
  `sklearn.base` returns a **new, unfitted** estimator with the same settings. Cloning before
  fitting means a caller's object is never changed behind their back.
* `sklearn.metrics` has the evaluation functions: `mean_squared_error`, `mean_absolute_error`,
  `r2_score`. Each takes `(y_true, y_pred)` in that order.

| Metric | Formula | Perfect | Mean baseline |
|---|---|---|---|
| MSE | mean((y − ŷ)²) | 0 | variance of y |
| MAE | mean(\|y − ŷ\|) | 0 | — |
| R² | 1 − SSE / SST | 1 | 0 on the data it was fitted to |

## Worked example
```python
X_train = np.array([[1.0], [2.0], [3.0], [4.0]]); y_train = np.array([3.0, 5.0, 7.0, 9.0])
model = LinearRegression().fit(X_train, y_train)
model.coef_, model.intercept_     # (array([2.]), 1.0): y = 2x + 1
model.predict(np.array([[5.0]]))  # array([11.])
DummyRegressor(strategy="mean").fit(X_train, y_train).predict(np.array([[5.0]]))   # array([6.])
```

## What the library does inside
`LinearRegression.fit` solves least squares, as you will by hand in ML-09;
`DummyRegressor` is your mean baseline. The metric functions are the formulas implemented in
ML-03, the optional deep dive after this step.

## Common mistakes
* Passing a 1-D `X` (`[1, 2, 3]`); use shape `(n, 1)` for one feature.
* Swapping the arguments of a metric: `r2_score(y_pred, y_true)` gives a different number.
* Reading `coef_` before calling `fit`.
* Fitting the caller's model in place and surprising them later — clone first.

## Why this matters
Pipelines, cross-validation and hyperparameter search in the coming steps all rely on this
contract: anything with `fit`/`predict`/`get_params` can be cloned, combined and evaluated.

## References

- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
