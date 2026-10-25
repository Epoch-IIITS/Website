# Features, Labels and Baseline Models

## Learning outcomes

After this lesson you can:

- Describe a dataset as a feature matrix X and a label vector y
- Write models as classes with fit and predict methods
- Build mean and majority-class baselines and explain why every model needs one
- Refuse to predict before fitting

## Intuition
Supervised learning means learning a rule from examples whose answers are known. Each example is
described by numbers called **features** (size, age, word counts...) and has a **label** (the
answer: a price, or a class such as "spam"). Before building a clever model, ask: how well does
a model that ignores the features do? That is the **baseline**, and any real model must beat it.

## Precise explanation
* **Feature matrix** `X` has shape `(n_samples, n_features)`: one row per example.
  **Labels** `y` have shape `(n_samples,)`.
* **Regression** predicts numbers; **classification** predicts categories.
* A **model** is an object with two methods (the convention scikit-learn uses):
  * `fit(X, y)` learns from training data and returns `self`;
  * `predict(X)` returns one prediction per row of `X`.
  Learned values are stored in attributes ending with `_`, e.g. `self.mean_`.
* **Mean regressor**: always predicts the training mean of `y`. It is the best constant
  prediction under squared error.
* **Majority classifier**: always predicts the most common training label. With 95% "not spam",
  it already scores 95% accuracy — a warning that accuracy alone can mislead.
* **Mean squared error**: $\frac1n\sum (y_i - \hat y_i)^2$; **accuracy**: fraction of correct
  predictions.

## Worked example
Training labels `[3, 5, 10]` → mean 6. Predicting 6 for test labels `[4, 8]` gives
MSE $((4-6)^2 + (8-6)^2)/2 = 4$. Labels `["a", "b", "b"]` → majority `"b"`.

## Common mistakes
* Computing the baseline on the test set (it must be fitted on training data only).
* Returning a single number from `predict` instead of one prediction per row.
* Forgetting `return self` from `fit`, which breaks `Model().fit(X, y).predict(X)`.

## Why this matters
Every model in this topic follows this `fit`/`predict` interface, and comparing against a
baseline is the first sanity check of any experiment.

## Library implementation

scikit-learn ships these baselines as `sklearn.dummy.DummyRegressor(strategy="mean")` and
`DummyClassifier(strategy="most_frequent")`, and the metrics as
`sklearn.metrics.mean_squared_error` and `accuracy_score`. Every scikit-learn estimator uses the
same `fit`/`predict` interface you just wrote, so later models can be swapped in without changing
the surrounding code. These comparisons run only when scikit-learn is installed.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
