"""Machine learning with scikit-learn (library revision, Phase 1).

Each library step is followed on the path by the from-scratch step it replaces, kept as an
optional deep dive: [[regression-metrics]], [[train-test-split]], [[standard-scaler]],
[[knn-classifier]], [[polynomial-overfitting]], [[k-fold-cv]], [[ridge-regression]], [[kmeans]].
"""

PROBLEMS = [
# ---------------------------------------------------------------- sklearn-estimator-api
{
"slug": "sklearn-estimator-api", "title": "The scikit-learn Estimator API",
"difficulty": "beginner", "prereqs": ["ml-baselines"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Use fit, predict and score on any scikit-learn estimator",
               "Copy an unfitted estimator with clone and read its settings with get_params",
               "Evaluate a regressor with sklearn.metrics (MSE, MAE, R²)"],
"tags": ["scikit-learn", "estimator-api", "regression-metrics", "baselines"],
"sources": ["S089", "S091"], "entry": "evaluate_regressor(model, X_train, y_train, X_test, y_test)",
"article": r'''
# The scikit-learn Estimator API

## Intuition
In [[ml-baselines]] you wrote a model that predicts the mean. scikit-learn ships hundreds of
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
`LinearRegression.fit` solves least squares, as you will by hand in [[least-squares-line]];
`DummyRegressor` is your mean baseline. The metric functions are the formulas implemented in
[[regression-metrics]], the optional deep dive after this step.

## Common mistakes
* Passing a 1-D `X` (`[1, 2, 3]`); use shape `(n, 1)` for one feature.
* Swapping the arguments of a metric: `r2_score(y_pred, y_true)` gives a different number.
* Reading `coef_` before calling `fit`.
* Fitting the caller's model in place and surprising them later — clone first.

## Why this matters
Pipelines, cross-validation and hyperparameter search in the coming steps all rely on this
contract: anything with `fit`/`predict`/`get_params` can be cloned, combined and evaluated.
''',
"statement": r'''
Write `evaluate_regressor(model, X_train, y_train, X_test, y_test)` that fits a **clone** of
`model` on the training data and returns
`{"model": fitted_clone, "predictions": list[float], "mse": float, "mae": float, "r2": float}`
computed on the test data with `sklearn.metrics`.

* The `model` passed in must stay unfitted (use `sklearn.base.clone`).
* Raise `ValueError` if `X_train` and `y_train` (or `X_test` and `y_test`) have different numbers
  of rows.

**Example**
```python
from sklearn.linear_model import LinearRegression
r = evaluate_regressor(LinearRegression(), [[1], [2], [3], [4]], [3, 5, 7, 9], [[5], [6]], [11, 14])
r["predictions"], r["mse"], r["mae"]     # ([11.0, 13.0], 0.5, 0.5)
```
''',
"starter": r'''
from sklearn.base import clone
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_regressor(model, X_train, y_train, X_test, y_test):
    # TODO: clone, fit, predict, measure
    pass
''',
"hints": [
    "Check `len(X_train) == len(y_train)` and the same for the test arrays.",
    "`fitted = clone(model).fit(X_train, y_train)`; `pred = fitted.predict(X_test)`.",
    "Metrics take `(y_true, y_pred)`; convert predictions with `[float(v) for v in pred]`.",
],
"solution": r'''
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
''',
"explanation": r'''
`clone` copies the settings but not the learned state, so fitting it leaves the caller's model
untouched. Any regressor works because the function relies only on `fit` and `predict`, and the
three metrics come from `sklearn.metrics` with the true values first.
''',
"tests": r'''
import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression


class TestEvaluateRegressor(unittest.TestCase):
    def test_linear_example(self):
        r = S.evaluate_regressor(LinearRegression(), [[1], [2], [3], [4]], [3, 5, 7, 9], [[5], [6]], [11, 14])
        self.assertEqual([round(v, 9) for v in r["predictions"]], [11.0, 13.0])
        self.assertAlmostEqual(r["mse"], 0.5)
        self.assertAlmostEqual(r["mae"], 0.5)

    def test_original_model_not_fitted(self):
        model = LinearRegression()
        r = S.evaluate_regressor(model, [[1], [2], [3]], [1, 2, 3], [[4]], [4])
        self.assertFalse(hasattr(model, "coef_"))
        self.assertIsNot(r["model"], model)
        self.assertTrue(hasattr(r["model"], "coef_"))

    def test_clone_keeps_settings(self):
        model = DummyRegressor(strategy="median")
        r = S.evaluate_regressor(model, [[0], [1], [2]], [1, 2, 10], [[3]], [2])
        self.assertEqual(r["model"].get_params()["strategy"], "median")
        self.assertEqual(r["predictions"], [2.0])

    def test_metrics_match_formulas(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(40, 2)); y = X @ np.array([1.5, -2.0]) + rng.normal(scale=0.3, size=40)
        r = S.evaluate_regressor(LinearRegression(), X[:30], y[:30], X[30:], y[30:])
        pred, yt = np.array(r["predictions"]), y[30:]
        self.assertAlmostEqual(r["mse"], float(np.mean((yt - pred) ** 2)), places=10)
        self.assertAlmostEqual(r["mae"], float(np.mean(np.abs(yt - pred))), places=10)
        self.assertAlmostEqual(r["r2"], 1 - np.sum((yt - pred) ** 2) / np.sum((yt - yt.mean()) ** 2), places=10)

    def test_mean_baseline_r2(self):
        r = S.evaluate_regressor(DummyRegressor(), [[0], [1], [2], [3]], [1, 2, 3, 6], [[4], [5]], [3, 3])
        self.assertEqual(r["predictions"], [3.0, 3.0])
        self.assertEqual(r["mse"], 0.0)

    def test_plain_floats_and_validation(self):
        r = S.evaluate_regressor(LinearRegression(), [[1], [2]], [1, 2], [[3], [4]], [3, 5])
        self.assertTrue(all(type(r[k]) is float for k in ("mse", "mae", "r2")))
        self.assertTrue(all(type(v) is float for v in r["predictions"]))
        with self.assertRaises(ValueError):
            S.evaluate_regressor(LinearRegression(), [[1], [2]], [1], [[3]], [3])
''',
"feedback": [
    ("test_linear_example", "Fit on the training data, predict the test rows, and pass (y_true, y_pred) to the metrics."),
    ("test_original_model_not_fitted", "Fit `clone(model)`, not `model` itself."),
    ("test_metrics_match_formulas", "Use mean_squared_error, mean_absolute_error and r2_score on the test set."),
    ("test_plain_floats_and_validation", "Convert results to float and check that X and y lengths match."),
],
},
# ---------------------------------------------------------------- sklearn-train-test-split
{
"slug": "sklearn-train-test-split", "title": "Splitting Data with scikit-learn",
"difficulty": "beginner", "prereqs": ["sklearn-estimator-api"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Split arrays with train_test_split, keeping rows paired",
               "Preserve class proportions with stratify",
               "Generate repeated stratified splits with StratifiedShuffleSplit"],
"tags": ["scikit-learn", "train-test-split", "stratification", "reproducibility"],
"sources": ["S012", "S089"], "entry": "split_data(X, y, test_size=0.25, seed=0, stratify=False)",
"article": r'''
# Splitting Data with scikit-learn

## Intuition
A model has to be judged on rows it never saw. scikit-learn's splitters shuffle once, keep each
row's features and label together, and can keep rare classes represented in both halves.

## Precise explanation
```python
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)
```

* Every array you pass is split with the **same** shuffled indices, so rows stay paired.
* `random_state` fixes the shuffle: the same number gives the same split every run.
* `stratify=y` splits each class separately so the class ratio is (nearly) the same in train and
  test. Use it for classification, especially with imbalanced classes.
* `StratifiedShuffleSplit(n_splits, test_size, random_state).split(X, y)` yields several
  independent stratified `(train_index, test_index)` pairs — useful for repeated evaluation.

## Worked example
With 8 negatives and 2 positives and `test_size=0.5, stratify=y`, the test set gets 4 negatives
and 1 positive. Without stratification a 5-row test set may contain no positives at all, and
accuracy on it says nothing about the rare class.

## What the library does inside
`train_test_split` draws one permutation of the row indices and slices it — exactly the
procedure in [[train-test-split]], the optional deep dive after this step. The stratified version
does that per class and merges the results.

## Common mistakes
* Calling it twice (once for X, once for y): the shuffles differ and the pairs break.
* Forgetting `random_state`, so the reported score changes on every run.
* Tuning on the test set; keep it for the final check and tune with cross-validation instead.

## Why this matters
Every evaluation in the rest of the course starts from an honest split; the capstone of this topic
uses a stratified split before any preprocessing.
''',
"statement": r'''
Write two functions.

1. `split_data(X, y, test_size=0.25, seed=0, stratify=False)` returns
   `(X_train, X_test, y_train, y_test)` using `train_test_split` with `random_state=seed`, and
   `stratify=y` when `stratify` is true.
2. `stratified_splits(X, y, n_splits=3, test_size=0.25, seed=0)` returns a list of
   `(train_index, test_index)` pairs (as Python lists of ints) from `StratifiedShuffleSplit`.

Raise `ValueError` in both if `X` and `y` have different lengths.

**Example**
```python
X = np.arange(20).reshape(10, 2); y = np.array([0] * 8 + [1] * 2)
Xtr, Xte, ytr, yte = split_data(X, y, test_size=0.5, seed=1, stratify=True)
sorted(yte.tolist())     # [0, 0, 0, 0, 1]
```
''',
"starter": r'''
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split


def split_data(X, y, test_size=0.25, seed=0, stratify=False):
    # TODO
    pass


def stratified_splits(X, y, n_splits=3, test_size=0.25, seed=0):
    # TODO
    pass
''',
"hints": [
    "Pass both arrays to one `train_test_split` call so they are shuffled together.",
    "`stratify=y if stratify else None`, `random_state=seed`.",
    "`for train, test in StratifiedShuffleSplit(n_splits=..., test_size=..., random_state=seed).split(X, y)`.",
],
"solution": r'''
from sklearn.model_selection import StratifiedShuffleSplit, train_test_split


def split_data(X, y, test_size=0.25, seed=0, stratify=False):
    if len(X) != len(y):
        raise ValueError("X and y must have the same length")
    return train_test_split(X, y, test_size=test_size, random_state=seed,
                            stratify=y if stratify else None)


def stratified_splits(X, y, n_splits=3, test_size=0.25, seed=0):
    if len(X) != len(y):
        raise ValueError("X and y must have the same length")
    splitter = StratifiedShuffleSplit(n_splits=n_splits, test_size=test_size, random_state=seed)
    return [([int(i) for i in train], [int(i) for i in test]) for train, test in splitter.split(X, y)]
''',
"explanation": r'''
One `train_test_split` call shuffles all arrays with the same permutation, so features and labels
stay aligned; `stratify` makes the split per class. `StratifiedShuffleSplit` yields index arrays,
which are converted to lists of plain ints.
''',
"tests": r'''
import numpy as np


class TestSplitData(unittest.TestCase):
    def test_stratified_ratio(self):
        X = np.arange(20).reshape(10, 2); y = np.array([0] * 8 + [1] * 2)
        Xtr, Xte, ytr, yte = S.split_data(X, y, test_size=0.5, seed=1, stratify=True)
        self.assertEqual(sorted(yte.tolist()), [0, 0, 0, 0, 1])
        self.assertEqual(sorted(ytr.tolist()), [0, 0, 0, 0, 1])

    def test_rows_stay_paired(self):
        X = np.arange(30).reshape(15, 2); y = X[:, 0] * 10
        Xtr, Xte, ytr, yte = S.split_data(X, y, seed=3)
        self.assertTrue(np.array_equal(ytr, Xtr[:, 0] * 10))
        self.assertTrue(np.array_equal(yte, Xte[:, 0] * 10))

    def test_sizes_and_disjoint(self):
        X = np.arange(40).reshape(20, 2); y = np.arange(20)
        Xtr, Xte, ytr, yte = S.split_data(X, y, test_size=0.25, seed=0)
        self.assertEqual((len(ytr), len(yte)), (15, 5))
        self.assertEqual(sorted(ytr.tolist() + yte.tolist()), list(range(20)))

    def test_reproducible(self):
        X = np.arange(40).reshape(20, 2); y = np.arange(20)
        a = S.split_data(X, y, seed=7)[3]
        b = S.split_data(X, y, seed=7)[3]
        c = S.split_data(X, y, seed=8)[3]
        self.assertTrue(np.array_equal(a, b))
        self.assertFalse(np.array_equal(a, c))

    def test_stratified_splits(self):
        X = np.zeros((12, 1)); y = np.array([0] * 9 + [1] * 3)
        splits = S.stratified_splits(X, y, n_splits=4, test_size=4, seed=0)
        self.assertEqual(len(splits), 4)
        for train, test in splits:
            self.assertEqual(len(test), 4)
            self.assertEqual(sorted(train + test), list(range(12)))
            self.assertEqual(sum(y[test]), 1)
            self.assertTrue(all(type(i) is int for i in train + test))

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.split_data(np.zeros((4, 1)), np.zeros(3))
        with self.assertRaises(ValueError):
            S.stratified_splits(np.zeros((4, 1)), np.zeros(3))
''',
"feedback": [
    ("test_stratified_ratio", "Pass stratify=y when stratify is true."),
    ("test_rows_stay_paired", "Split X and y in a single train_test_split call."),
    ("test_reproducible", "Use random_state=seed."),
    ("test_stratified_splits", "Convert StratifiedShuffleSplit's index arrays to lists of ints."),
],
},
# ---------------------------------------------------------------- sklearn-scaler-pipeline
{
"slug": "sklearn-scaler-pipeline", "title": "Scaling inside a Pipeline",
"difficulty": "beginner", "prereqs": ["sklearn-train-test-split"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Chain a StandardScaler and a model in a Pipeline",
               "Explain why the scaler must be fitted on training data only (leakage)",
               "Inspect a fitted step through named_steps"],
"tags": ["scikit-learn", "pipeline", "standardisation", "data-leakage"],
"sources": ["S012", "S089"], "entry": "train_and_predict(X_train, y_train, X_test)",
"article": r'''
# Scaling inside a Pipeline

## Intuition
Many models care about feature scale: a feature measured in metres and one in millimetres should
not get different influence just because of units. Standardising (subtract the mean, divide by
the standard deviation) fixes that — but the mean and standard deviation must come from the
**training** data only. A `Pipeline` makes that automatic.

## Precise explanation
```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
pipe.fit(X_train, y_train)    # scaler.fit_transform(X_train), then model.fit
pipe.predict(X_test)          # scaler.transform(X_test) with the TRAINING mean/std, then predict
```

* A pipeline is itself an estimator: it has `fit`, `predict`, `score`, `get_params`.
* Every step but the last is a **transformer** (`fit` + `transform`); the last can be any model.
* `pipe.named_steps["scale"].mean_` and `.scale_` are the statistics learned from training data
  (`scale_` uses the population standard deviation, ddof = 0).
* **Leakage**: fitting the scaler on all data before splitting lets test-set statistics shape
  training. The scores look better than the model will be on truly new data.

## Worked example
Train column [0, 2, 4] has mean 2 and standard deviation 1.633. A test value 6 becomes
(6 − 2)/1.633 = 2.45 — test values are scaled with training statistics, even though the test set
on its own has a different mean.

## What the library does inside
`StandardScaler` stores the column means and standard deviations in `fit` and applies them in
`transform` — the function you build in [[standard-scaler]], the optional deep dive after this
step. The pipeline just calls the steps in order.

## Common mistakes
* `StandardScaler().fit(X)` on the whole dataset before splitting (leakage).
* Calling `fit_transform` on the test set: it refits the scaler to test statistics.
* Reusing one pipeline object across experiments without cloning; the last fit overwrites it.

## Why this matters
Cross-validation and hyperparameter search refit the whole pipeline on each training fold, so
leakage is prevented everywhere — but only if preprocessing lives inside the pipeline.
''',
"statement": r'''
Write `train_and_predict(X_train, y_train, X_test)` that builds a **new** pipeline
`Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])`, fits it on the
training data and returns `(pipeline, predictions)` with predictions as a list of Python ints.

**Example**
```python
pipe, pred = train_and_predict([[0, 100], [1, 110], [2, 300], [3, 310]], [0, 0, 1, 1], [[0.5, 105], [2.5, 305]])
pred                                       # [0, 1]
pipe.named_steps["scale"].mean_.tolist()   # [1.5, 205.0]   (training statistics)
```
''',
"starter": r'''
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def train_and_predict(X_train, y_train, X_test):
    # TODO
    pass
''',
"hints": [
    "Create the pipeline inside the function so each call gets fresh steps.",
    "`pipe.fit(X_train, y_train)` fits the scaler and then the model.",
    "`[int(v) for v in pipe.predict(X_test)]`.",
],
"solution": r'''
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def train_and_predict(X_train, y_train, X_test):
    pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
    pipe.fit(X_train, y_train)
    return pipe, [int(v) for v in pipe.predict(X_test)]
''',
"explanation": r'''
Fitting the pipeline fits the scaler on the training rows only and trains the model on the scaled
rows; predicting transforms the test rows with the stored training statistics before the model
sees them. Building the pipeline inside the function keeps calls independent.
''',
"tests": r'''
import numpy as np
from sklearn.linear_model import LogisticRegression


class TestScaledPipeline(unittest.TestCase):
    def test_example(self):
        pipe, pred = S.train_and_predict([[0, 100], [1, 110], [2, 300], [3, 310]], [0, 0, 1, 1], [[0.5, 105], [2.5, 305]])
        self.assertEqual(pred, [0, 1])
        self.assertEqual(pipe.named_steps["scale"].mean_.tolist(), [1.5, 205.0])

    def test_scaler_uses_training_statistics(self):
        rng = np.random.default_rng(0)
        X_train = rng.normal(5, 2, size=(30, 3)); y_train = (X_train[:, 0] > 5).astype(int)
        X_test = rng.normal(50, 9, size=(10, 3))
        pipe, _ = S.train_and_predict(X_train, y_train, X_test)
        scaler = pipe.named_steps["scale"]
        self.assertTrue(np.allclose(scaler.mean_, X_train.mean(axis=0)))
        self.assertTrue(np.allclose(scaler.scale_, X_train.std(axis=0)))

    def test_matches_manual_scaling(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(40, 2)) * [1, 100]; y = (X[:, 0] + X[:, 1] / 100 > 0).astype(int)
        pipe, pred = S.train_and_predict(X[:30], y[:30], X[30:])
        mu, sd = X[:30].mean(axis=0), X[:30].std(axis=0)
        manual = LogisticRegression().fit((X[:30] - mu) / sd, y[:30]).predict((X[30:] - mu) / sd)
        self.assertEqual(pred, manual.tolist())

    def test_step_names(self):
        pipe, _ = S.train_and_predict([[0], [1], [2], [3]], [0, 0, 1, 1], [[1.5]])
        self.assertEqual(list(pipe.named_steps), ["scale", "model"])

    def test_new_pipeline_each_call(self):
        a, _ = S.train_and_predict([[0], [1], [2], [3]], [0, 0, 1, 1], [[1]])
        b, _ = S.train_and_predict([[10], [11], [12], [13]], [0, 0, 1, 1], [[11]])
        self.assertIsNot(a, b)
        self.assertEqual(a.named_steps["scale"].mean_.tolist(), [1.5])

    def test_plain_ints(self):
        _, pred = S.train_and_predict([[0], [1], [2], [3]], [0, 0, 1, 1], [[0], [3]])
        self.assertTrue(all(type(v) is int for v in pred))
''',
"feedback": [
    ("test_scaler_uses_training_statistics", "Fit the pipeline on the training data only; never on X_test."),
    ("test_step_names", "Name the steps 'scale' and 'model'."),
    ("test_new_pipeline_each_call", "Build the Pipeline inside the function."),
    ("test_plain_ints", "Convert predictions with int(...)."),
],
},
# ---------------------------------------------------------------- sklearn-knn
{
"slug": "sklearn-knn", "title": "k-Nearest Neighbours with scikit-learn",
"difficulty": "intermediate", "prereqs": ["sklearn-scaler-pipeline", "logistic-regression"],
"packages": ["numpy", "scikit-learn"],
"objectives": ["Fit KNeighborsClassifier inside a scaling pipeline",
               "Compare test accuracy across values of k",
               "Explain how k trades variance for bias"],
"tags": ["scikit-learn", "knn", "hyperparameters", "pipeline"],
"sources": ["S012", "S091"], "entry": "knn_accuracy_by_k(X_train, y_train, X_test, y_test, ks)",
"article": r'''
# k-Nearest Neighbours with scikit-learn

## Intuition
k-NN predicts the majority label among the k training points closest to a query. Small k follows
every quirk of the training data; large k smooths decisions until it predicts the majority
class everywhere. Distances mix features, so scaling matters.

## Precise explanation
```python
from sklearn.neighbors import KNeighborsClassifier
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
```

* `make_pipeline` names steps automatically (`"standardscaler"`, `"kneighborsclassifier"`).
* `n_neighbors` is k; `weights="distance"` lets closer neighbours count more; the default metric
  is Euclidean distance.
* `fit` just stores the (scaled) training data; the work happens in `predict`, which searches
  for neighbours with a tree or brute force.
* `accuracy_score(y_true, y_pred)` from `sklearn.metrics` is the share of correct predictions.

## Worked example
On two overlapping clusters, k = 1 might reach training accuracy 1.0 but test accuracy 0.80;
k = 7 might give 0.90 on test; k = n predicts the majority class and drops to the base rate.
Choosing k by the test score, as here, is acceptable for exploring — for a final choice, use
cross-validation ([[sklearn-cross-validation]]).

## What the library does inside
Your [[knn-classifier]] (the optional deep dive after this step) computes all distances and takes
the k smallest; scikit-learn does the same with faster neighbour search structures.

## Common mistakes
* Forgetting to scale: one large-range feature dominates the distance.
* Even k for two classes, which allows ties.
* Picking k on the test set and then reporting that same test score as final.

## Why this matters
k-NN is a strong baseline for small datasets and the idea behind nearest-neighbour search used by
retrieval systems later in the course.
''',
"statement": r'''
Write `knn_accuracy_by_k(X_train, y_train, X_test, y_test, ks)` returning
`{"accuracy": {k: float, ...}, "best_k": int}`.

* For each k, fit `make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))` on the
  training data and record test accuracy with `accuracy_score`.
* `best_k` is the k with the highest accuracy; ties go to the **smallest** k.
* Raise `ValueError` if `ks` is empty or any k is less than 1 or larger than the number of
  training rows.
''',
"starter": r'''
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def knn_accuracy_by_k(X_train, y_train, X_test, y_test, ks):
    # TODO
    pass
''',
"hints": [
    "Validate `ks` against `len(X_train)` first.",
    "Inside the loop build a new pipeline for each k, fit it and call `accuracy_score(y_test, pipe.predict(X_test))`.",
    "`best_k = min(ks, key=lambda k: (-accuracy[k], k))` picks the highest accuracy, then the smallest k.",
],
"solution": r'''
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def knn_accuracy_by_k(X_train, y_train, X_test, y_test, ks):
    if not ks or any(k < 1 or k > len(X_train) for k in ks):
        raise ValueError("each k must be between 1 and the number of training rows")
    accuracy = {}
    for k in ks:
        pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=k))
        pipe.fit(X_train, y_train)
        accuracy[k] = float(accuracy_score(y_test, pipe.predict(X_test)))
    best_k = min(ks, key=lambda k: (-accuracy[k], k))
    return {"accuracy": accuracy, "best_k": best_k}
''',
"explanation": r'''
Each k gets its own freshly fitted pipeline, so scaling statistics always come from the training
rows. The best k is chosen by sorting on negative accuracy and then on k, which resolves ties
towards the simpler, smaller neighbourhood.
''',
"tests": r'''
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def blobs(seed, n=40):
    rng = np.random.default_rng(seed)
    X = np.vstack([rng.normal(0, 1, size=(n, 2)), rng.normal(2.5, 1, size=(n, 2))]) * [1, 50]
    return X, np.array([0] * n + [1] * n)


class TestKnnByK(unittest.TestCase):
    def test_separable_points(self):
        X = [[0, 0], [0, 1], [1, 0], [10, 10], [10, 11], [11, 10]]
        y = [0, 0, 0, 1, 1, 1]
        r = S.knn_accuracy_by_k(X, y, [[0.5, 0.5], [10.5, 10.5]], [0, 1], [1, 3])
        self.assertEqual(r["accuracy"], {1: 1.0, 3: 1.0})
        self.assertEqual(r["best_k"], 1)

    def test_matches_manual_scaled_knn(self):
        X, y = blobs(0)
        Xte, yte = blobs(1, 20)
        r = S.knn_accuracy_by_k(X, y, Xte, yte, [5])
        mu, sd = X.mean(axis=0), X.std(axis=0)
        manual = KNeighborsClassifier(5).fit((X - mu) / sd, y).predict((Xte - mu) / sd)
        self.assertAlmostEqual(r["accuracy"][5], float(np.mean(manual == yte)))

    def test_huge_k_predicts_majority(self):
        X = [[0], [1], [2], [3], [4]]
        y = [0, 0, 0, 1, 1]
        r = S.knn_accuracy_by_k(X, y, [[4], [3.5]], [1, 1], [1, 5])
        self.assertEqual(r["accuracy"][5], 0.0)
        self.assertEqual(r["accuracy"][1], 1.0)
        self.assertEqual(r["best_k"], 1)

    def test_tie_prefers_smaller_k(self):
        X, y = blobs(2)
        r = S.knn_accuracy_by_k(X, y, X[:4], y[:4], [9, 3, 5])
        best = max(r["accuracy"].values())
        self.assertEqual(r["best_k"], min(k for k, a in r["accuracy"].items() if a == best))

    def test_float_accuracies(self):
        X, y = blobs(3)
        r = S.knn_accuracy_by_k(X, y, X, y, [1, 15])
        self.assertTrue(all(type(a) is float and 0 <= a <= 1 for a in r["accuracy"].values()))
        self.assertEqual(r["accuracy"][1], 1.0)

    def test_invalid_k(self):
        for ks in ([], [0], [100]):
            with self.assertRaises(ValueError):
                S.knn_accuracy_by_k([[0], [1]], [0, 1], [[0]], [0], ks)
''',
"feedback": [
    ("test_matches_manual_scaled_knn", "Scale inside the pipeline: make_pipeline(StandardScaler(), KNeighborsClassifier(k))."),
    ("test_tie_prefers_smaller_k", "On equal accuracy choose the smallest k."),
    ("test_float_accuracies", "Store float(accuracy_score(...)) for every k."),
    ("test_invalid_k", "Reject an empty list and any k outside 1..len(X_train)."),
],
},
# ---------------------------------------------------------------- sklearn-polynomial-validation
{
"slug": "sklearn-polynomial-validation", "title": "Polynomial Features and Validation Curves",
"difficulty": "intermediate", "prereqs": ["sklearn-knn", "linreg-gradient-descent"],
"packages": ["numpy", "scikit-learn"],
"objectives": ["Build polynomial models with PolynomialFeatures in a pipeline",
               "Compute training and validation error for each degree with validation_curve",
               "Recognise underfitting and overfitting in a validation curve"],
"tags": ["scikit-learn", "overfitting", "model-complexity", "validation-curve"],
"sources": ["S090", "S091"], "entry": "degree_curve(x, y, degrees, n_splits=5, seed=0)",
"article": r'''
# Polynomial Features and Validation Curves

## Intuition
A straight line cannot follow a curve (underfitting); a degree-15 polynomial follows every noisy
point (overfitting). Plot error against model complexity for both the data the model trained on
and data it did not: training error keeps falling, validation error falls and then rises. The
bottom of the validation curve is the complexity to choose.

## Precise explanation
```python
from sklearn.model_selection import KFold, validation_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

model = make_pipeline(PolynomialFeatures(include_bias=False), LinearRegression())
train, val = validation_curve(model, X, y, param_name="polynomialfeatures__degree",
                              param_range=[1, 2, 3], cv=KFold(5, shuffle=True, random_state=0),
                              scoring="neg_mean_squared_error")
```

* `PolynomialFeatures(degree=d)` turns a column x into x, x², …, xᵈ; `include_bias=False` leaves
  the constant to the linear model's intercept.
* In a pipeline, a step's parameter is addressed as `<step name>__<parameter>`.
* `validation_curve` returns arrays of shape `(len(param_range), n_folds)`: one score per
  setting and fold, for the training folds and the held-out fold.
* scikit-learn always **maximises** scores, so errors appear negated (`neg_mean_squared_error`);
  multiply by −1 to get MSE.

## Worked example
For y = x² plus noise: degree 1 has high error on both curves (underfit); degree 2 has the lowest
validation error; degrees 8–10 have tiny training error but larger validation error (overfit).

## What the library does inside
It repeats the experiment of [[polynomial-overfitting]] (the optional deep dive after this step)
for every degree on every fold, refitting a clone of the pipeline each time.

## Common mistakes
* Forgetting to negate `neg_mean_squared_error` and picking the *largest* error.
* Passing `param_name="degree"` instead of `"polynomialfeatures__degree"`.
* Using an unshuffled `KFold` on data sorted by x: each fold extrapolates.

## Why this matters
Validation curves are the standard picture for any complexity knob — tree depth, k in k-NN,
regularisation strength — and they motivate the cross-validation and search tools next.
''',
"statement": r'''
Write `degree_curve(x, y, degrees, n_splits=5, seed=0)` for one input feature `x` (a 1-D
sequence) returning `{"train_mse": list[float], "val_mse": list[float], "best_degree": int}`.

* Model: `make_pipeline(PolynomialFeatures(include_bias=False), LinearRegression())`.
* Use `validation_curve` with `param_name="polynomialfeatures__degree"`,
  `cv=KFold(n_splits, shuffle=True, random_state=seed)` and `scoring="neg_mean_squared_error"`.
* Each list holds the mean MSE over folds for each degree, in the order of `degrees`.
* `best_degree` has the smallest validation MSE (ties: the smaller degree).
* Raise `ValueError` if `degrees` is empty or `x` and `y` differ in length.
''',
"starter": r'''
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, validation_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def degree_curve(x, y, degrees, n_splits=5, seed=0):
    # TODO
    pass
''',
"hints": [
    "Reshape the feature to a column: `X = np.asarray(x, dtype=float).reshape(-1, 1)`.",
    "`train, val = validation_curve(model, X, y, param_name=..., param_range=degrees, cv=..., scoring=...)`.",
    "MSE per degree is `-scores.mean(axis=1)`; pick the degree with the smallest validation MSE.",
],
"solution": r'''
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, validation_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def degree_curve(x, y, degrees, n_splits=5, seed=0):
    if not degrees or len(x) != len(y):
        raise ValueError("need degrees and matching x and y")
    X = np.asarray(x, dtype=float).reshape(-1, 1)
    model = make_pipeline(PolynomialFeatures(include_bias=False), LinearRegression())
    train, val = validation_curve(model, X, np.asarray(y, dtype=float),
                                  param_name="polynomialfeatures__degree", param_range=list(degrees),
                                  cv=KFold(n_splits, shuffle=True, random_state=seed),
                                  scoring="neg_mean_squared_error")
    train_mse = [float(v) for v in -train.mean(axis=1)]
    val_mse = [float(v) for v in -val.mean(axis=1)]
    best = min(range(len(degrees)), key=lambda i: (val_mse[i], degrees[i]))
    return {"train_mse": train_mse, "val_mse": val_mse, "best_degree": int(degrees[best])}
''',
"explanation": r'''
`validation_curve` refits the pipeline for every degree and fold; averaging across folds and
negating the scores gives mean squared errors. The minimum of the validation curve is the degree
that generalises best on this data.
''',
"tests": r'''
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold


def quadratic(seed=0, n=40):
    rng = np.random.default_rng(seed)
    x = rng.uniform(-3, 3, n)
    return x, x ** 2 + rng.normal(scale=1.0, size=n)


class TestDegreeCurve(unittest.TestCase):
    def test_quadratic_best_degree(self):
        x, y = quadratic()
        r = S.degree_curve(x, y, [1, 2, 10])
        self.assertEqual(r["best_degree"], 2)

    def test_underfit_line(self):
        x, y = quadratic()
        r = S.degree_curve(x, y, [1, 2])
        self.assertGreater(r["val_mse"][0], 5 * r["val_mse"][1])
        self.assertGreater(r["train_mse"][0], 5 * r["train_mse"][1])

    def test_training_error_never_rises(self):
        x, y = quadratic(1)
        r = S.degree_curve(x, y, [1, 2, 3, 4, 5, 6])
        for a, b in zip(r["train_mse"], r["train_mse"][1:]):
            self.assertLessEqual(b, a + 1e-9)

    def test_degree_one_matches_manual_cv(self):
        x, y = quadratic(2)
        r = S.degree_curve(x, y, [1], n_splits=4, seed=5)
        errors = []
        for train, test in KFold(4, shuffle=True, random_state=5).split(x):
            model = LinearRegression().fit(x[train].reshape(-1, 1), y[train])
            errors.append(np.mean((model.predict(x[test].reshape(-1, 1)) - y[test]) ** 2))
        self.assertAlmostEqual(r["val_mse"][0], float(np.mean(errors)), places=9)

    def test_types_and_lengths(self):
        x, y = quadratic(3)
        r = S.degree_curve(list(x), list(y), [1, 2, 3])
        self.assertEqual((len(r["train_mse"]), len(r["val_mse"])), (3, 3))
        self.assertTrue(all(type(v) is float and v >= 0 for v in r["train_mse"] + r["val_mse"]))
        self.assertIs(type(r["best_degree"]), int)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.degree_curve([1, 2, 3], [1, 2, 3], [])
        with self.assertRaises(ValueError):
            S.degree_curve([1, 2, 3], [1, 2], [1])
''',
"feedback": [
    ("test_quadratic_best_degree", "Pick the degree with the smallest mean validation MSE."),
    ("test_underfit_line", "Negate the neg_mean_squared_error scores to get MSE."),
    ("test_degree_one_matches_manual_cv", "Use KFold(n_splits, shuffle=True, random_state=seed) and include_bias=False."),
    ("test_types_and_lengths", "Return plain floats in the order of degrees."),
],
},
# ---------------------------------------------------------------- sklearn-cross-validation
{
"slug": "sklearn-cross-validation", "title": "Cross-Validation with scikit-learn",
"difficulty": "intermediate", "prereqs": ["sklearn-polynomial-validation"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Estimate performance with cross_val_score and a shuffled KFold",
               "Use StratifiedKFold for classification",
               "Report the mean and spread of fold scores"],
"tags": ["scikit-learn", "cross-validation", "kfold", "evaluation"],
"sources": ["S012", "S091"], "entry": "cv_report(model, X, y, n_splits=5, seed=0, stratified=False, scoring=None)",
"article": r'''
# Cross-Validation with scikit-learn

## Intuition
One train/test split gives one noisy number. k-fold cross-validation splits the data into k
folds, trains on k − 1 of them and tests on the remaining one, k times. Every row is tested once,
and the spread of the k scores tells you how much to trust the mean.

## Precise explanation
```python
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score

cv = KFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(model, X, y, cv=cv)          # one score per fold
scores.mean(), scores.std()
```

* `cross_val_score` clones the model for each fold, so the model you pass is never fitted.
* `KFold(shuffle=True, random_state=...)` shuffles once before cutting folds; without `shuffle`
  the folds follow the row order, which is wrong for sorted data.
* `StratifiedKFold` keeps the class ratio in every fold — the right default for classification.
* `scoring` chooses the metric (`"accuracy"`, `"r2"`, `"neg_mean_squared_error"`, …); by default
  it is the estimator's own `score`.

## Worked example
Five fold accuracies [0.90, 0.85, 0.95, 0.80, 0.90] give 0.88 ± 0.05. A rival model at 0.89 ±
0.06 is not clearly better: the difference is smaller than the fold-to-fold spread.

## What the library does inside
The fold loop is the one you write in [[k-fold-cv]] (the optional deep dive after this step):
split the indices, fit a fresh model, score, repeat.

## Common mistakes
* Preprocessing (scaling, imputing) before cross-validation instead of inside a pipeline.
* Reporting the best fold instead of the mean.
* Comparing models on different fold splits; fix `random_state` so they see the same folds.

## Why this matters
Hyperparameter search ([[sklearn-grid-search]]) runs exactly this loop for every candidate
setting, and the capstone reports a cross-validated score next to the final test score.
''',
"statement": r'''
Write `cv_report(model, X, y, n_splits=5, seed=0, stratified=False, scoring=None)` returning
`{"scores": list[float], "mean": float, "std": float}`.

* Folds: `KFold(n_splits, shuffle=True, random_state=seed)`, or `StratifiedKFold` with the same
  arguments when `stratified` is true.
* Use `cross_val_score(model, X, y, cv=folds, scoring=scoring)`; `std` is the population standard
  deviation of the scores (NumPy's default).
* Raise `ValueError` if `n_splits < 2` or `X` and `y` differ in length.
''',
"starter": r'''
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score


def cv_report(model, X, y, n_splits=5, seed=0, stratified=False, scoring=None):
    # TODO
    pass
''',
"hints": [
    "Choose the splitter class from `stratified`, then build it with `shuffle=True, random_state=seed`.",
    "`scores = cross_val_score(model, X, y, cv=folds, scoring=scoring)`.",
    "Return `[float(s) for s in scores]`, `float(scores.mean())` and `float(scores.std())`.",
],
"solution": r'''
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score


def cv_report(model, X, y, n_splits=5, seed=0, stratified=False, scoring=None):
    if n_splits < 2 or len(X) != len(y):
        raise ValueError("need n_splits >= 2 and matching X and y")
    splitter = StratifiedKFold if stratified else KFold
    folds = splitter(n_splits=n_splits, shuffle=True, random_state=seed)
    scores = np.asarray(cross_val_score(model, X, y, cv=folds, scoring=scoring))
    return {"scores": [float(s) for s in scores], "mean": float(scores.mean()), "std": float(scores.std())}
''',
"explanation": r'''
The splitter defines the folds; `cross_val_score` clones and fits the model once per fold and
returns the held-out scores. The mean is the estimate and the standard deviation shows how much
it moves from fold to fold.
''',
"tests": r'''
import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import KFold, StratifiedKFold


def regression_data(seed=0, n=50):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 3))
    return X, X @ np.array([2.0, -1.0, 0.5]) + rng.normal(scale=0.5, size=n)


class TestCvReport(unittest.TestCase):
    def test_matches_manual_loop(self):
        X, y = regression_data()
        r = S.cv_report(LinearRegression(), X, y, n_splits=5, seed=1)
        manual = []
        for train, test in KFold(5, shuffle=True, random_state=1).split(X):
            manual.append(LinearRegression().fit(X[train], y[train]).score(X[test], y[test]))
        self.assertEqual(len(r["scores"]), 5)
        for a, b in zip(r["scores"], manual):
            self.assertAlmostEqual(a, b, places=10)

    def test_mean_and_std(self):
        X, y = regression_data(1)
        r = S.cv_report(LinearRegression(), X, y)
        self.assertAlmostEqual(r["mean"], float(np.mean(r["scores"])))
        self.assertAlmostEqual(r["std"], float(np.std(r["scores"])))

    def test_model_not_fitted(self):
        X, y = regression_data(2)
        model = LinearRegression()
        S.cv_report(model, X, y)
        self.assertFalse(hasattr(model, "coef_"))

    def test_stratified_folds(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(40, 2)); y = np.array([0] * 30 + [1] * 10)
        r = S.cv_report(LogisticRegression(), X, y, n_splits=5, seed=0, stratified=True, scoring="accuracy")
        manual = []
        for train, test in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
            self.assertEqual(int(y[test].sum()), 2)
            manual.append(LogisticRegression().fit(X[train], y[train]).score(X[test], y[test]))
        self.assertTrue(np.allclose(r["scores"], manual))

    def test_scoring_argument(self):
        X, y = regression_data(4)
        r = S.cv_report(LinearRegression(), X, y, scoring="neg_mean_squared_error")
        self.assertTrue(all(s <= 0 for s in r["scores"]))
        self.assertTrue(all(type(s) is float for s in r["scores"]))

    def test_invalid(self):
        X, y = regression_data()
        with self.assertRaises(ValueError):
            S.cv_report(LinearRegression(), X, y, n_splits=1)
        with self.assertRaises(ValueError):
            S.cv_report(LinearRegression(), X, y[:-1])
''',
"feedback": [
    ("test_matches_manual_loop", "Use KFold(n_splits, shuffle=True, random_state=seed) and cross_val_score."),
    ("test_stratified_folds", "Use StratifiedKFold when stratified is true."),
    ("test_scoring_argument", "Pass scoring through to cross_val_score."),
    ("test_invalid", "Reject n_splits < 2 and mismatched lengths."),
],
},
# ---------------------------------------------------------------- sklearn-column-transformer
{
"slug": "sklearn-column-transformer", "title": "Pipelines and ColumnTransformer",
"difficulty": "intermediate", "prereqs": ["sklearn-cross-validation"],
"packages": ["numpy", "pandas", "scikit-learn"],
"objectives": ["Preprocess numeric and categorical columns differently with ColumnTransformer",
               "Impute missing values and one-hot encode categories inside a pipeline",
               "Fit and predict directly on a pandas DataFrame"],
"tags": ["scikit-learn", "pipeline", "column-transformer", "one-hot-encoding", "imputation"],
"sources": ["S012", "S089"], "entry": "build_model(numeric, categorical)",
"article": r'''
# Pipelines and ColumnTransformer

## Intuition
Real tables mix numbers (area, age) and categories (city, plan), with gaps. Numbers need
imputing and scaling; categories need imputing and one-hot encoding. `ColumnTransformer` sends
each group of columns through its own mini-pipeline and glues the results together, and the
whole thing still fits and predicts like one model.

## Precise explanation
```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
categorical = make_pipeline(SimpleImputer(strategy="most_frequent"),
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False))
prep = ColumnTransformer([("num", numeric, ["area", "age"]), ("cat", categorical, ["city"])])
model = Pipeline([("prep", prep), ("model", LinearRegression())])
model.fit(df_train, y_train); model.predict(df_test)
```

* Columns are selected **by name** from a DataFrame; columns not listed are dropped.
* `SimpleImputer` learns the median (or most frequent value) on training data and fills gaps.
* `OneHotEncoder` makes one 0/1 column per category seen in training; `handle_unknown="ignore"`
  turns an unseen category into all zeros instead of an error.
* `prep.get_feature_names_out()` lists the output columns, e.g. `num__area`, `cat__city_Pune`.

## Worked example
Training cities [Pune, Delhi, Pune] become columns `cat__city_Delhi`, `cat__city_Pune`. A test
row with city Chennai becomes [0, 0] in those columns, and a missing area is filled with the
training median.

## What the library does inside
The imputers and encoders are fitted on the training rows during `fit` — the same "fit on train,
apply to test" rule as [[sklearn-scaler-pipeline]] — and the column outputs are concatenated side
by side, as `pd.concat(axis=1)` would.

## Common mistakes
* Encoding categories with `pd.get_dummies` on the full dataset (leakage and mismatched columns).
* Forgetting `handle_unknown="ignore"` and crashing on a new category in production.
* Passing a NumPy array when the transformer selects columns by name.

## Why this matters
This is how tabular models are built in practice; the house-price project idea and the capstone
both start from a ColumnTransformer.
''',
"statement": r'''
Write `build_model(numeric, categorical)` that returns an **unfitted**
`Pipeline([("prep", ColumnTransformer(...)), ("model", LinearRegression())])` where

* numeric columns go through `SimpleImputer(strategy="median")` then `StandardScaler()`
  (transformer name `"num"`),
* categorical columns go through `SimpleImputer(strategy="most_frequent")` then
  `OneHotEncoder(handle_unknown="ignore", sparse_output=False)` (transformer name `"cat"`).

Raise `ValueError` if both column lists are empty or a column appears in both.

**Example**
```python
model = build_model(["area"], ["city"]).fit(df, df["price"])
list(model.named_steps["prep"].get_feature_names_out())
# ['num__area', 'cat__city_Delhi', 'cat__city_Pune']
```
''',
"starter": r'''
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_model(numeric, categorical):
    # TODO
    pass
''',
"hints": [
    "Validate the two lists first (empty both, or overlapping names).",
    "Each branch is a `make_pipeline(imputer, transformer)`.",
    "`ColumnTransformer([(\"num\", numeric_pipe, numeric), (\"cat\", categorical_pipe, categorical)])`.",
],
"solution": r'''
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_model(numeric, categorical):
    if not numeric and not categorical:
        raise ValueError("need at least one column")
    if set(numeric) & set(categorical):
        raise ValueError("a column cannot be both numeric and categorical")
    numeric_pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
    categorical_pipe = make_pipeline(SimpleImputer(strategy="most_frequent"),
                                     OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    prep = ColumnTransformer([("num", numeric_pipe, list(numeric)), ("cat", categorical_pipe, list(categorical))])
    return Pipeline([("prep", prep), ("model", LinearRegression())])
''',
"explanation": r'''
Two small pipelines handle the column types; the ColumnTransformer applies each to its columns
and concatenates the outputs; the outer pipeline adds the model. Everything is learned in `fit`
from the training rows, so the same object can predict on new DataFrames safely.
''',
"tests": r'''
import numpy as np
import pandas as pd


def homes():
    return pd.DataFrame({
        "area": [50.0, 80.0, np.nan, 120.0, 65.0, 90.0],
        "age": [10.0, 5.0, 20.0, 2.0, np.nan, 8.0],
        "city": ["Pune", "Delhi", "Pune", "Delhi", np.nan, "Pune"],
        "price": [40.0, 75.0, 38.0, 120.0, 50.0, 80.0],
    })


class TestBuildModel(unittest.TestCase):
    def test_feature_names(self):
        df = homes()
        model = S.build_model(["area", "age"], ["city"]).fit(df, df["price"])
        self.assertEqual(list(model.named_steps["prep"].get_feature_names_out()),
                         ["num__area", "num__age", "cat__city_Delhi", "cat__city_Pune"])

    def test_unfitted_and_structure(self):
        model = S.build_model(["area"], ["city"])
        self.assertEqual(list(model.named_steps), ["prep", "model"])
        self.assertFalse(hasattr(model.named_steps["model"], "coef_"))

    def test_median_imputation_from_training(self):
        df = homes()
        model = S.build_model(["area"], []).fit(df, df["price"])
        imputer = model.named_steps["prep"].named_transformers_["num"][0]
        self.assertEqual(imputer.statistics_.tolist(), [80.0])

    def test_unknown_category_is_zeros(self):
        df = homes()
        model = S.build_model(["area"], ["city"]).fit(df, df["price"])
        new = pd.DataFrame({"area": [70.0], "age": [3.0], "city": ["Chennai"]})
        encoded = model.named_steps["prep"].transform(new)
        self.assertEqual(encoded[0, 1:].tolist(), [0.0, 0.0])
        self.assertEqual(model.predict(new).shape, (1,))

    def test_no_missing_after_transform(self):
        df = homes()
        model = S.build_model(["area", "age"], ["city"]).fit(df, df["price"])
        self.assertFalse(np.isnan(model.named_steps["prep"].transform(df)).any())

    def test_invalid(self):
        with self.assertRaises(ValueError):
            S.build_model([], [])
        with self.assertRaises(ValueError):
            S.build_model(["city"], ["city"])
''',
"feedback": [
    ("test_feature_names", "Name the transformers 'num' and 'cat' and keep the column order you were given."),
    ("test_median_imputation_from_training", "Numeric columns: SimpleImputer(strategy='median') then StandardScaler()."),
    ("test_unknown_category_is_zeros", "Use OneHotEncoder(handle_unknown='ignore', sparse_output=False)."),
    ("test_invalid", "Reject empty column lists and columns listed twice."),
],
},
# ---------------------------------------------------------------- sklearn-grid-search
{
"slug": "sklearn-grid-search", "title": "Regularisation and Hyperparameter Search",
"difficulty": "advanced", "prereqs": ["sklearn-column-transformer"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Regularise a linear model with Ridge and explain how alpha shrinks coefficients",
               "Search hyperparameters with GridSearchCV over a pipeline",
               "Read best_params_, best_score_ and cv_results_"],
"tags": ["scikit-learn", "regularisation", "ridge", "grid-search", "hyperparameters"],
"sources": ["S012", "S091"], "entry": "tune_ridge(X, y, alphas, n_splits=5, seed=0)",
"article": r'''
# Regularisation and Hyperparameter Search

## Intuition
A linear model with many features can fit noise with large, wobbly coefficients.
**Regularisation** adds a penalty for large coefficients: Ridge minimises
squared error + α·‖w‖². Larger α means smaller coefficients and a simpler model. Which α is best
is a question for cross-validation — and `GridSearchCV` asks it for every candidate.

## Precise explanation
```python
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, KFold

pipe = make_pipeline(StandardScaler(), Ridge())
search = GridSearchCV(pipe, {"ridge__alpha": [0.01, 0.1, 1, 10, 100]},
                      cv=KFold(5, shuffle=True, random_state=0), scoring="neg_mean_squared_error")
search.fit(X, y)
search.best_params_          # {'ridge__alpha': 1}
-search.best_score_          # mean validation MSE of the best setting
search.best_estimator_       # the pipeline refitted on ALL of X, y with the best alpha
search.cv_results_["mean_test_score"]   # one entry per candidate, in grid order
```

* Scale features before Ridge: the penalty treats all coefficients alike, so units matter.
* The classifier counterpart is `LogisticRegression(C=...)`, where **C = 1/α**: smaller C means
  *stronger* regularisation.
* Grids are usually logarithmic (0.01, 0.1, 1, 10, …) because the effect of α is multiplicative.
* `refit=True` (the default) retrains the best setting on all the data you passed.

## Worked example
With 30 features (only 3 useful) and 40 rows, α = 0.01 nearly reproduces least squares and overfits, α = 100
shrinks everything towards zero and underfits; a middle value such as α = 1–10 has the lowest
cross-validated MSE. The coefficient norm ‖w‖ falls steadily as α grows.

## What the library does inside
`Ridge` solves (XᵀX + αI)w = Xᵀy — the closed form in [[ridge-regression]], the optional deep dive
after this step. `GridSearchCV` is a loop of [[sklearn-cross-validation]] over every candidate.

## Common mistakes
* Searching on the test set, or reporting `best_score_` as the final test score.
* Forgetting the `<step>__` prefix in the grid keys.
* Reading a larger C as more regularisation in `LogisticRegression` (it is less).

## Why this matters
Almost every model has knobs. Searching them with cross-validation inside a pipeline is the
standard, leak-free way to choose them.
''',
"statement": r'''
Write `tune_ridge(X, y, alphas, n_splits=5, seed=0)` returning
`{"best_alpha": float, "best_mse": float, "mse_by_alpha": list[float], "coef_norms": list[float], "model": fitted_best}`.

* Search `make_pipeline(StandardScaler(), Ridge())` with `GridSearchCV` over `{"ridge__alpha": alphas}`,
  `cv=KFold(n_splits, shuffle=True, random_state=seed)`, `scoring="neg_mean_squared_error"`.
* `best_mse` and `mse_by_alpha` are positive mean validation MSEs (grid order).
* `coef_norms[i]` is the Euclidean norm of the Ridge coefficients when the pipeline with `alphas[i]`
  is fitted on all of `X, y`.
* `model` is `search.best_estimator_`.
* Raise `ValueError` if `alphas` is empty or contains a value ≤ 0.
''',
"starter": r'''
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def tune_ridge(X, y, alphas, n_splits=5, seed=0):
    # TODO
    pass
''',
"hints": [
    "Build the pipeline, then `GridSearchCV(pipe, {\"ridge__alpha\": list(alphas)}, cv=..., scoring=...)` and fit it.",
    "`-search.cv_results_[\"mean_test_score\"]` gives the MSE for every alpha in grid order.",
    "For the norms, fit `make_pipeline(StandardScaler(), Ridge(alpha=a))` on all data and take `np.linalg.norm(p[-1].coef_)`.",
],
"solution": r'''
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
''',
"explanation": r'''
`GridSearchCV` cross-validates the scaled Ridge pipeline for each alpha and refits the winner on
all the data. Negating the scores turns them into MSEs. Refitting each alpha on the full data shows
the shrinkage directly: the coefficient norm can only fall as the penalty grows.
''',
"tests": r'''
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def noisy(seed=0, n=40, d=30):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)); w = np.zeros(d); w[:3] = [3.0, -2.0, 1.5]
    return X, X @ w + rng.normal(scale=2.0, size=n)


class TestTuneRidge(unittest.TestCase):
    def test_norms_shrink(self):
        X, y = noisy()
        r = S.tune_ridge(X, y, [0.01, 0.1, 1, 10, 100])
        for a, b in zip(r["coef_norms"], r["coef_norms"][1:]):
            self.assertLess(b, a)

    def test_middle_alpha_wins(self):
        X, y = noisy()
        r = S.tune_ridge(X, y, [0.001, 3, 10000])
        self.assertEqual(r["best_alpha"], 3.0)
        self.assertAlmostEqual(r["best_mse"], min(r["mse_by_alpha"]))

    def test_mse_matches_cross_val_score(self):
        X, y = noisy(1)
        r = S.tune_ridge(X, y, [0.5, 5], n_splits=4, seed=2)
        for alpha, mse in zip([0.5, 5], r["mse_by_alpha"]):
            scores = cross_val_score(make_pipeline(StandardScaler(), Ridge(alpha=alpha)), X, y,
                                     cv=KFold(4, shuffle=True, random_state=2), scoring="neg_mean_squared_error")
            self.assertAlmostEqual(mse, float(-scores.mean()), places=9)

    def test_best_model_refit_on_all_data(self):
        X, y = noisy(2)
        r = S.tune_ridge(X, y, [0.1, 1, 10])
        ref = make_pipeline(StandardScaler(), Ridge(alpha=r["best_alpha"])).fit(X, y)
        self.assertTrue(np.allclose(r["model"].predict(X), ref.predict(X)))

    def test_types(self):
        X, y = noisy(3)
        r = S.tune_ridge(X, y, [1, 10])
        self.assertIs(type(r["best_alpha"]), float)
        self.assertTrue(all(type(v) is float and v > 0 for v in r["mse_by_alpha"] + r["coef_norms"]))

    def test_invalid(self):
        X, y = noisy()
        for alphas in ([], [1, 0], [-1]):
            with self.assertRaises(ValueError):
                S.tune_ridge(X, y, alphas)
''',
"feedback": [
    ("test_norms_shrink", "Fit a scaled Ridge(alpha=a) on all data for each alpha and take the coefficient norm."),
    ("test_mse_matches_cross_val_score", "Use KFold(n_splits, shuffle=True, random_state=seed) and negate the scores."),
    ("test_best_model_refit_on_all_data", "Return search.best_estimator_, which GridSearchCV refits on all data."),
    ("test_invalid", "Alphas must be a non-empty list of positive numbers."),
],
},
# ---------------------------------------------------------------- sklearn-trees-forests
{
"slug": "sklearn-trees-forests", "title": "Decision Trees and Random Forests",
"difficulty": "advanced", "prereqs": ["decision-stump-gini", "sklearn-grid-search"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Train a DecisionTreeClassifier and limit its depth",
               "Train a RandomForestClassifier and read feature_importances_",
               "Explain why averaging many randomised trees reduces variance"],
"tags": ["scikit-learn", "decision-trees", "random-forest", "ensembles", "feature-importance"],
"sources": ["S012", "S089"], "entry": "compare_tree_forest(X_train, y_train, X_test, y_test, max_depth=None, n_estimators=100, seed=0)",
"article": r'''
# Decision Trees and Random Forests

## Intuition
Your decision stump ([[decision-stump-gini]]) asked one question. A **decision tree** keeps
asking: split, then split each side, until the leaves are pure or a depth limit stops it. A deep
tree memorises the training set. A **random forest** trains many trees, each on a bootstrap
sample with random subsets of features at each split, and lets them vote: the individual errors
partly cancel.

## Precise explanation
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train)
tree.get_depth(), tree.get_n_leaves()
forest = RandomForestClassifier(n_estimators=200, random_state=0).fit(X_train, y_train)
forest.feature_importances_        # one value per feature, summing to 1
```

* Trees need **no scaling**: a split compares one feature with a threshold.
* `max_depth`, `min_samples_leaf` and `max_features` limit complexity; with no limits, a tree
  reaches 100% training accuracy whenever no two identical rows disagree.
* `feature_importances_` is the total impurity decrease contributed by each feature, averaged
  over trees and normalised to sum to 1. It is biased towards features with many split points;
  [[permutation-importance]] (later) is a more reliable check.
* `random_state` fixes the bootstrap samples and feature choices, making results reproducible.

## Worked example
On data where only feature 0 matters plus label noise, an unlimited tree scores 1.00 on training
and about 0.80 on test; a 200-tree forest scores about 0.90 on test, and feature 0 receives most of
the importance.

## What the library does inside
Each split chooses the feature and threshold with the lowest weighted Gini impurity — your stump's
search, applied recursively. The forest repeats that on bootstrap samples, like [[bootstrap-ci]]
resamples data, and averages the trees' class probabilities.

## Common mistakes
* Judging a deep tree by its training accuracy.
* Treating impurity-based importances as causal effects.
* Comparing a tree and a forest trained with different random states or data.

## Why this matters
Forests and boosted trees ([[sklearn-gradient-boosting]]) are the strongest general-purpose models
for tabular data, and the usual baseline before trying neural networks.
''',
"statement": r'''
Write `compare_tree_forest(X_train, y_train, X_test, y_test, max_depth=None, n_estimators=100, seed=0)`
returning
`{"tree_train_accuracy", "tree_test_accuracy", "forest_test_accuracy", "tree_depth", "top_feature", "importances"}`.

* Tree: `DecisionTreeClassifier(max_depth=max_depth, random_state=seed)`.
* Forest: `RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=seed)`.
* Accuracies are floats; `tree_depth` is `tree.get_depth()`; `importances` is the forest's
  `feature_importances_` as a list of floats; `top_feature` is the index of the largest one.
* Raise `ValueError` if `n_estimators < 1`.
''',
"starter": r'''
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


def compare_tree_forest(X_train, y_train, X_test, y_test, max_depth=None, n_estimators=100, seed=0):
    # TODO
    pass
''',
"hints": [
    "Fit both models with the same `random_state=seed`.",
    "`model.score(X, y)` is accuracy for classifiers.",
    "`importances = [float(v) for v in forest.feature_importances_]`; `top_feature = importances.index(max(importances))`.",
],
"solution": r'''
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier


def compare_tree_forest(X_train, y_train, X_test, y_test, max_depth=None, n_estimators=100, seed=0):
    if n_estimators < 1:
        raise ValueError("n_estimators must be at least 1")
    tree = DecisionTreeClassifier(max_depth=max_depth, random_state=seed).fit(X_train, y_train)
    forest = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                    random_state=seed).fit(X_train, y_train)
    importances = [float(v) for v in forest.feature_importances_]
    return {"tree_train_accuracy": float(tree.score(X_train, y_train)),
            "tree_test_accuracy": float(tree.score(X_test, y_test)),
            "forest_test_accuracy": float(forest.score(X_test, y_test)),
            "tree_depth": int(tree.get_depth()), "top_feature": importances.index(max(importances)),
            "importances": importances}
''',
"explanation": r'''
Both models are fitted with the same seed and depth limit, so the comparison isolates the effect
of averaging. `score` gives accuracy, `get_depth` shows how far the single tree grew, and the
forest's normalised impurity importances identify the feature it relied on most.
''',
"tests": r'''
import numpy as np


def signal_and_noise(seed, n=300, flip=0.15):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 5))
    y = (X[:, 0] + 0.3 * X[:, 1] > 0).astype(int)
    noise = rng.random(n) < flip
    return X, np.where(noise, 1 - y, y)


class TestTreeForest(unittest.TestCase):
    def test_unlimited_tree_memorises(self):
        X, y = signal_and_noise(0)
        Xt, yt = signal_and_noise(1)
        r = S.compare_tree_forest(X, y, Xt, yt)
        self.assertEqual(r["tree_train_accuracy"], 1.0)
        self.assertLess(r["tree_test_accuracy"], 0.9)

    def test_forest_beats_single_tree(self):
        X, y = signal_and_noise(2)
        Xt, yt = signal_and_noise(3, n=1000)
        r = S.compare_tree_forest(X, y, Xt, yt, n_estimators=200)
        self.assertGreater(r["forest_test_accuracy"], r["tree_test_accuracy"])

    def test_depth_limit(self):
        X, y = signal_and_noise(4)
        r = S.compare_tree_forest(X, y, X, y, max_depth=2)
        self.assertLessEqual(r["tree_depth"], 2)
        self.assertLess(r["tree_train_accuracy"], 1.0)

    def test_importances(self):
        X, y = signal_and_noise(5)
        r = S.compare_tree_forest(X, y, X, y, n_estimators=50)
        self.assertEqual(r["top_feature"], 0)
        self.assertEqual(len(r["importances"]), 5)
        self.assertAlmostEqual(sum(r["importances"]), 1.0)

    def test_reproducible(self):
        X, y = signal_and_noise(6)
        a = S.compare_tree_forest(X, y, X[:50], y[:50], n_estimators=30, seed=4)
        b = S.compare_tree_forest(X, y, X[:50], y[:50], n_estimators=30, seed=4)
        self.assertEqual(a, b)

    def test_invalid(self):
        X, y = signal_and_noise(7, n=20)
        with self.assertRaises(ValueError):
            S.compare_tree_forest(X, y, X, y, n_estimators=0)
''',
"feedback": [
    ("test_unlimited_tree_memorises", "With max_depth=None the tree grows until its leaves are pure."),
    ("test_depth_limit", "Pass max_depth to both models."),
    ("test_importances", "Use the forest's feature_importances_ as floats and the index of the largest."),
    ("test_reproducible", "Use random_state=seed for both models."),
],
},
# ---------------------------------------------------------------- sklearn-gradient-boosting
{
"slug": "sklearn-gradient-boosting", "title": "Gradient Boosting",
"difficulty": "advanced", "prereqs": ["sklearn-trees-forests"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Train HistGradientBoostingClassifier and explain how boosting adds trees",
               "Track validation log-loss as trees are added",
               "Choose the number of boosting iterations from a validation curve"],
"tags": ["scikit-learn", "gradient-boosting", "ensembles", "early-stopping", "log-loss"],
"sources": ["S012", "S091"], "entry": "boosting_curve(X_train, y_train, X_val, y_val, max_iter=100, learning_rate=0.1, seed=0)",
"article": r'''
# Gradient Boosting

## Intuition
A forest grows trees independently and averages them. **Boosting** grows them one after another:
each new small tree is trained to correct the mistakes of the ensemble so far, and its vote is
scaled down by a learning rate. Early trees fix big errors; later ones fine-tune — and eventually
start fitting noise.

## Precise explanation
For classification, the model keeps a score F(x) whose sigmoid is P(y = 1). Each iteration fits
a regression tree to the **gradient of the log-loss** (how much each prediction should move) and
adds `learning_rate × tree` to F. That is gradient descent ([[linreg-gradient-descent]]) where
each step is a tree.

```python
from sklearn.ensemble import HistGradientBoostingClassifier

model = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1,
                                       early_stopping=False, random_state=0).fit(X, y)
for proba in model.staged_predict_proba(X_val):   # after 1 tree, 2 trees, ...
    ...
```

* "Hist" means features are bucketed into at most 255 bins first, which makes training fast and
  lets the model handle missing values natively.
* `max_iter` is the number of trees; `learning_rate` trades speed for smoothness; `max_depth`
  or `max_leaf_nodes` keep each tree small.
* `early_stopping=True` holds out part of the training data and stops when the validation loss
  stops improving; here we switch it off to see the whole curve.
* `log_loss(y_true, proba)` from `sklearn.metrics` measures probabilistic predictions; lower is better.

## Worked example
With learning rate 0.3 on noisy data, validation log-loss might fall from 0.62 after one tree to
0.35 after 20, then creep back up to 0.40 by 200 trees while training loss keeps falling. The best
number of iterations is near 20.

## What the library does inside
Each tree is grown greedily like the trees in [[sklearn-trees-forests]], but on the binned features
and against gradients rather than class labels.

## Common mistakes
* A large learning rate with many trees: fast overfitting.
* Choosing `max_iter` by the test score; use a separate validation set or early stopping.
* Expecting identical results across library versions; compare trends, not exact numbers.

## Why this matters
Gradient-boosted trees win most tabular competitions and power many production systems in
ranking, fraud detection and forecasting.
''',
"statement": r'''
Write `boosting_curve(X_train, y_train, X_val, y_val, max_iter=100, learning_rate=0.1, seed=0)`
for binary labels, returning
`{"train_loss": list[float], "val_loss": list[float], "best_iteration": int, "val_accuracy": float}`.

* Fit `HistGradientBoostingClassifier(max_iter=max_iter, learning_rate=learning_rate,
  early_stopping=False, random_state=seed)` on the training data.
* `train_loss[i]` and `val_loss[i]` are `log_loss` after `i + 1` trees, computed from
  `staged_predict_proba` (pass `labels=[0, 1]`).
* `best_iteration` is the 1-based iteration with the lowest validation loss (earliest on ties);
  `val_accuracy` is the final model's accuracy on the validation set.
* Raise `ValueError` if `max_iter < 1` or `learning_rate <= 0`.
''',
"starter": r'''
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss


def boosting_curve(X_train, y_train, X_val, y_val, max_iter=100, learning_rate=0.1, seed=0):
    # TODO
    pass
''',
"hints": [
    "Validate the arguments, then fit the classifier with `early_stopping=False`.",
    "`[float(log_loss(y_val, p, labels=[0, 1])) for p in model.staged_predict_proba(X_val)]`.",
    "`best_iteration = val_loss.index(min(val_loss)) + 1`.",
],
"solution": r'''
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import log_loss


def boosting_curve(X_train, y_train, X_val, y_val, max_iter=100, learning_rate=0.1, seed=0):
    if max_iter < 1 or learning_rate <= 0:
        raise ValueError("need max_iter >= 1 and learning_rate > 0")
    model = HistGradientBoostingClassifier(max_iter=max_iter, learning_rate=learning_rate,
                                           early_stopping=False, random_state=seed)
    model.fit(X_train, y_train)
    train_loss = [float(log_loss(y_train, p, labels=[0, 1])) for p in model.staged_predict_proba(X_train)]
    val_loss = [float(log_loss(y_val, p, labels=[0, 1])) for p in model.staged_predict_proba(X_val)]
    return {"train_loss": train_loss, "val_loss": val_loss,
            "best_iteration": val_loss.index(min(val_loss)) + 1,
            "val_accuracy": float(model.score(X_val, y_val))}
''',
"explanation": r'''
`staged_predict_proba` replays the ensemble one tree at a time, so a single fit yields the whole
loss curve. Training loss keeps falling as trees are added, while validation loss bottoms out;
its minimum marks how many trees to keep.
''',
"tests": r'''
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier


def noisy_moons(seed, n=300):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4))
    y = ((X[:, 0] ** 2 + X[:, 1] > 0.5).astype(int))
    flip = rng.random(n) < 0.2
    return X, np.where(flip, 1 - y, y)


class TestBoostingCurve(unittest.TestCase):
    def test_curve_lengths(self):
        X, y = noisy_moons(0)
        Xv, yv = noisy_moons(1)
        r = S.boosting_curve(X, y, Xv, yv, max_iter=30)
        self.assertEqual((len(r["train_loss"]), len(r["val_loss"])), (30, 30))

    def test_training_loss_falls(self):
        X, y = noisy_moons(2)
        r = S.boosting_curve(X, y, X[:50], y[:50], max_iter=60, learning_rate=0.3)
        self.assertLess(r["train_loss"][-1], 0.6 * r["train_loss"][0])
        self.assertLess(r["train_loss"][-1], r["train_loss"][len(r["train_loss"]) // 2])

    def test_validation_overfits_late(self):
        X, y = noisy_moons(3)
        Xv, yv = noisy_moons(4, n=600)
        r = S.boosting_curve(X, y, Xv, yv, max_iter=200, learning_rate=0.5)
        self.assertLess(r["best_iteration"], 200)
        self.assertGreater(r["val_loss"][-1], min(r["val_loss"]))
        self.assertEqual(r["val_loss"][r["best_iteration"] - 1], min(r["val_loss"]))

    def test_final_accuracy(self):
        X, y = noisy_moons(5)
        Xv, yv = noisy_moons(6)
        r = S.boosting_curve(X, y, Xv, yv, max_iter=40, seed=1)
        ref = HistGradientBoostingClassifier(max_iter=40, early_stopping=False, random_state=1).fit(X, y)
        self.assertAlmostEqual(r["val_accuracy"], float(ref.score(Xv, yv)))
        self.assertGreater(r["val_accuracy"], 0.65)

    def test_types(self):
        X, y = noisy_moons(7, n=80)
        r = S.boosting_curve(X, y, X, y, max_iter=5)
        self.assertTrue(all(type(v) is float for v in r["train_loss"] + r["val_loss"]))
        self.assertIs(type(r["best_iteration"]), int)

    def test_invalid(self):
        X, y = noisy_moons(8, n=40)
        with self.assertRaises(ValueError):
            S.boosting_curve(X, y, X, y, max_iter=0)
        with self.assertRaises(ValueError):
            S.boosting_curve(X, y, X, y, learning_rate=0)
''',
"feedback": [
    ("test_curve_lengths", "Use staged_predict_proba to get one probability set per tree."),
    ("test_validation_overfits_late", "best_iteration is the 1-based position of the smallest validation loss."),
    ("test_final_accuracy", "Fit with early_stopping=False and random_state=seed; score the validation set."),
    ("test_invalid", "Reject max_iter < 1 and learning_rate <= 0."),
],
},
# ---------------------------------------------------------------- sklearn-roc-pr
{
"slug": "sklearn-roc-pr", "title": "Thresholds, ROC and Precision–Recall Curves",
"difficulty": "advanced", "prereqs": ["sklearn-gradient-boosting", "classification-metrics"],
"packages": ["numpy", "scikit-learn"],
"objectives": ["Summarise a classifier's scores with ROC AUC and average precision",
               "Read precision and recall at every threshold with precision_recall_curve",
               "Choose a decision threshold that meets a recall target"],
"tags": ["scikit-learn", "roc-auc", "precision-recall", "thresholds", "imbalanced-data"],
"sources": ["S091", "S012"], "entry": "threshold_report(y_true, scores, min_recall)",
"article": r'''
# Thresholds, ROC and Precision–Recall Curves

## Intuition
A classifier outputs a score; you turn it into "yes" when the score passes a **threshold**. A
lower threshold catches more positives (higher recall) but raises more false alarms (lower
precision). Curves show every threshold at once, and the right threshold depends on what a miss
costs compared with a false alarm.

## Precise explanation
* **ROC curve**: true-positive rate (recall) against false-positive rate as the threshold falls.
  `roc_auc_score(y, scores)` is the area under it: the probability that a random positive scores
  higher than a random negative (ties count half). 1.0 is perfect ranking; 0.5 is chance.
* **Precision–recall curve**: precision against recall. `average_precision_score` summarises it.
  On imbalanced data (1% fraud) PR is more informative: ROC AUC can look excellent while
  precision is poor.
* `precision_recall_curve(y, scores)` returns `precision, recall, thresholds`; `precision[i]` and
  `recall[i]` belong to predicting positive when `score >= thresholds[i]` (the arrays have one
  extra final point, precision 1 and recall 0, with no threshold).

```python
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score
precision, recall, thresholds = precision_recall_curve(y, scores)
```

## Worked example
Scores [0.9, 0.8, 0.7, 0.6, 0.4, 0.2] for labels [1, 1, 0, 1, 0, 0]: thresholds 0.9, 0.8, 0.7, 0.6
give recall 1/3, 2/3, 2/3, 1 and precision 1, 1, 2/3, 3/4. To guarantee recall ≥ 0.9, the highest
usable threshold is 0.6, with precision 0.75. Eight of the nine positive–negative pairs are
ordered correctly, so ROC AUC = 8/9.

## What the library does inside
It sorts by score once and sweeps the threshold down, updating true- and false-positive counts —
the confusion-matrix counts from [[classification-metrics]] at every cut.

## Common mistakes
* Always using 0.5 as the threshold, whatever the costs.
* Reporting only accuracy on imbalanced data.
* Passing predicted labels instead of scores or probabilities to `roc_auc_score`.
* Choosing the threshold on the test set and then reporting test precision as unbiased.

## Why this matters
Medical screening, fraud and spam filters all pick thresholds from these curves; the spam/fraud
project idea at the end of this topic is built around them.
''',
"statement": r'''
Write `threshold_report(y_true, scores, min_recall)` for binary labels returning
`{"roc_auc": float, "average_precision": float, "threshold": float, "precision": float, "recall": float}`.

* `threshold` is the **highest** threshold from `precision_recall_curve` whose recall is at least
  `min_recall`; `precision` and `recall` are the values at that threshold.
* Raise `ValueError` if `y_true` does not contain both classes, lengths differ, or `min_recall`
  is not in (0, 1].

**Example**
```python
threshold_report([1, 1, 0, 1, 0, 0], [0.9, 0.8, 0.7, 0.6, 0.4, 0.2], 0.9)
# {'roc_auc': 0.888..., 'average_precision': 0.916..., 'threshold': 0.6, 'precision': 0.75, 'recall': 1.0}
```
''',
"starter": r'''
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score


def threshold_report(y_true, scores, min_recall):
    # TODO
    pass
''',
"hints": [
    "Validate: `set(y_true) == {0, 1}`, equal lengths, `0 < min_recall <= 1`.",
    "`precision, recall, thresholds = precision_recall_curve(y_true, scores)`; only the first `len(thresholds)` points have thresholds.",
    "Among indices i with `recall[i] >= min_recall`, take the one with the largest `thresholds[i]`.",
],
"solution": r'''
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score


def threshold_report(y_true, scores, min_recall):
    if len(y_true) != len(scores) or set(y_true) != {0, 1}:
        raise ValueError("need matching lengths and both classes")
    if not 0 < min_recall <= 1:
        raise ValueError("min_recall must be in (0, 1]")
    precision, recall, thresholds = precision_recall_curve(y_true, scores)
    ok = [i for i in range(len(thresholds)) if recall[i] >= min_recall]
    best = max(ok, key=lambda i: thresholds[i])
    return {"roc_auc": float(roc_auc_score(y_true, scores)),
            "average_precision": float(average_precision_score(y_true, scores)),
            "threshold": float(thresholds[best]), "precision": float(precision[best]),
            "recall": float(recall[best])}
''',
"explanation": r'''
The two summary scores rank the classifier independently of any threshold. To meet a recall
target with as few false alarms as possible, pick the highest threshold that still reaches the
target: the lowest threshold always has recall 1, so a valid choice always exists.
''',
"tests": r'''
import itertools
import numpy as np


def pairwise_auc(y, s):
    pos = [v for v, t in zip(s, y) if t == 1]
    neg = [v for v, t in zip(s, y) if t == 0]
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p, n in itertools.product(pos, neg))
    return wins / (len(pos) * len(neg))


class TestThresholdReport(unittest.TestCase):
    def test_example(self):
        r = S.threshold_report([1, 1, 0, 1, 0, 0], [0.9, 0.8, 0.7, 0.6, 0.4, 0.2], 0.9)
        self.assertAlmostEqual(r["roc_auc"], 8 / 9)
        self.assertEqual(r["threshold"], 0.6)
        self.assertAlmostEqual(r["precision"], 0.75)
        self.assertEqual(r["recall"], 1.0)

    def test_lower_target_allows_higher_threshold(self):
        r = S.threshold_report([1, 1, 0, 1, 0, 0], [0.9, 0.8, 0.7, 0.6, 0.4, 0.2], 0.6)
        self.assertEqual(r["threshold"], 0.8)
        self.assertEqual(r["precision"], 1.0)

    def test_auc_is_pairwise_ranking(self):
        rng = np.random.default_rng(0)
        y = rng.integers(0, 2, 60); s = np.round(rng.random(60) + 0.3 * y, 2)
        r = S.threshold_report(y.tolist(), s.tolist(), 0.5)
        self.assertAlmostEqual(r["roc_auc"], pairwise_auc(y.tolist(), s.tolist()), places=10)

    def test_perfect_ranking(self):
        r = S.threshold_report([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9], 1.0)
        self.assertEqual((r["roc_auc"], r["average_precision"]), (1.0, 1.0))
        self.assertEqual((r["threshold"], r["precision"]), (0.8, 1.0))

    def test_recall_target_met(self):
        rng = np.random.default_rng(1)
        y = rng.integers(0, 2, 80); s = rng.random(80) + 0.5 * y
        for target in (0.5, 0.8, 0.95):
            r = S.threshold_report(y.tolist(), s.tolist(), target)
            predicted = s >= r["threshold"]
            self.assertGreaterEqual(predicted[y == 1].mean(), target)
            self.assertAlmostEqual(r["precision"], y[predicted].mean())

    def test_invalid(self):
        for args in [([1, 1], [0.2, 0.3], 0.5), ([0, 1], [0.1], 0.5), ([0, 1], [0.1, 0.9], 0)]:
            with self.assertRaises(ValueError):
                S.threshold_report(*args)
''',
"feedback": [
    ("test_example", "Pick the highest threshold whose recall still reaches min_recall."),
    ("test_auc_is_pairwise_ranking", "roc_auc_score takes scores, not thresholded labels."),
    ("test_recall_target_met", "precision[i], recall[i] belong to thresholds[i]; ignore the final extra point."),
    ("test_invalid", "Require both classes, equal lengths and 0 < min_recall <= 1."),
],
},
# ---------------------------------------------------------------- sklearn-kmeans
{
"slug": "sklearn-kmeans", "title": "k-Means and Silhouette Scores",
"difficulty": "advanced", "prereqs": ["sklearn-roc-pr"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Cluster data with KMeans and read labels_, cluster_centers_ and inertia_",
               "Compare numbers of clusters with inertia and silhouette scores",
               "Make clustering reproducible with n_init and random_state"],
"tags": ["scikit-learn", "clustering", "kmeans", "silhouette", "unsupervised"],
"sources": ["S012", "S091"], "entry": "choose_k(X, ks, seed=0)",
"article": r'''
# k-Means and Silhouette Scores

## Intuition
k-means places k centres and assigns every point to the nearest one, then moves each centre to
the mean of its points, repeating until nothing changes. The hard part is choosing k: more
clusters always fit tighter, so you need a score that also rewards clusters being far apart.

## Precise explanation
```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
km.labels_, km.cluster_centers_, km.inertia_
silhouette_score(X, km.labels_)
```

* **Inertia** is the sum of squared distances from points to their centre. It never increases as
  k grows (with enough restarts), so the "elbow" where it stops dropping quickly is only a hint.
* **Silhouette** for one point: (b − a)/max(a, b), where a is the mean distance to its own cluster
  and b the mean distance to the nearest other cluster. The average lies in [−1, 1]; higher means
  compact, well-separated clusters. It needs at least 2 clusters.
* k-means can stop at a poor local optimum; `n_init=10` runs ten random starts and keeps the
  lowest inertia. `random_state` makes those starts reproducible.
* Scale features first: k-means uses Euclidean distance.

## Worked example
Three well-separated blobs: inertia drops sharply from k = 2 to k = 3 and slowly afterwards; the
silhouette is highest at k = 3 (about 0.7) and lower at k = 2 and k = 4.

## What the library does inside
Lloyd's algorithm from [[kmeans]] (the optional deep dive after this step), with "k-means++"
starting centres that are spread out, several restarts, and vectorised distance computations.

## Common mistakes
* Interpreting cluster numbers as meaningful (label 0 in one run may be label 2 in another).
* Choosing k by inertia alone, which always prefers more clusters.
* Clustering unscaled features with very different ranges.

## Why this matters
Clustering segments customers, groups documents and initialises other models; silhouette analysis
is the standard sanity check when no labels exist.
''',
"statement": r'''
Write `choose_k(X, ks, seed=0)` returning
`{"inertia": list[float], "silhouette": list[float], "best_k": int, "labels": list[int]}`.

* For each k in `ks`, fit `KMeans(n_clusters=k, n_init=10, random_state=seed)` and record
  `inertia_` and `silhouette_score(X, labels_)`.
* `best_k` has the highest silhouette (ties: smaller k); `labels` are that model's labels.
* Raise `ValueError` if `ks` is empty or any k is less than 2 or at least the number of rows.
''',
"starter": r'''
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def choose_k(X, ks, seed=0):
    # TODO
    pass
''',
"hints": [
    "Validate `ks` against `len(X)`: silhouette needs 2 ≤ k < n.",
    "Keep each fitted model so you can return the best one's `labels_`.",
    "`best = max(range(len(ks)), key=lambda i: (silhouette[i], -ks[i]))`.",
],
"solution": r'''
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def choose_k(X, ks, seed=0):
    if not ks or any(k < 2 or k >= len(X) for k in ks):
        raise ValueError("each k must satisfy 2 <= k < number of rows")
    models, inertia, silhouette = [], [], []
    for k in ks:
        km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(X)
        models.append(km)
        inertia.append(float(km.inertia_))
        silhouette.append(float(silhouette_score(X, km.labels_)))
    best = max(range(len(ks)), key=lambda i: (silhouette[i], -ks[i]))
    return {"inertia": inertia, "silhouette": silhouette, "best_k": int(ks[best]),
            "labels": [int(v) for v in models[best].labels_]}
''',
"explanation": r'''
Each k gets ten seeded restarts and keeps the best; inertia measures tightness and the silhouette
balances tightness against separation. Selecting the highest silhouette (smaller k on ties) gives a
reproducible choice, and the labels come from that same fitted model.
''',
"tests": r'''
import numpy as np
from sklearn.cluster import KMeans


def three_blobs(seed=0, n=40):
    rng = np.random.default_rng(seed)
    centres = np.array([[0, 0], [6, 0], [3, 6]])
    return np.vstack([rng.normal(c, 0.6, size=(n, 2)) for c in centres])


class TestChooseK(unittest.TestCase):
    def test_three_blobs(self):
        r = S.choose_k(three_blobs(), [2, 3, 4, 5])
        self.assertEqual(r["best_k"], 3)
        self.assertEqual(len(set(r["labels"])), 3)

    def test_inertia_decreases(self):
        r = S.choose_k(three_blobs(1), [2, 3, 4, 5])
        for a, b in zip(r["inertia"], r["inertia"][1:]):
            self.assertLess(b, a)

    def test_matches_kmeans(self):
        X = three_blobs(2)
        r = S.choose_k(X, [3], seed=5)
        km = KMeans(n_clusters=3, n_init=10, random_state=5).fit(X)
        self.assertAlmostEqual(r["inertia"][0], float(km.inertia_))
        self.assertEqual(r["labels"], km.labels_.tolist())

    def test_silhouette_range(self):
        r = S.choose_k(three_blobs(3), [2, 3, 6])
        self.assertTrue(all(-1 <= s <= 1 for s in r["silhouette"]))
        self.assertGreater(max(r["silhouette"]), 0.5)

    def test_types(self):
        r = S.choose_k(three_blobs(4), [2, 3])
        self.assertTrue(all(type(v) is float for v in r["inertia"] + r["silhouette"]))
        self.assertTrue(all(type(v) is int for v in r["labels"]))
        self.assertEqual(len(r["labels"]), 120)

    def test_invalid(self):
        X = three_blobs(n=2)
        for ks in ([], [1], [6]):
            with self.assertRaises(ValueError):
                S.choose_k(X, ks)
''',
"feedback": [
    ("test_three_blobs", "Pick the k with the highest silhouette score."),
    ("test_matches_kmeans", "Use KMeans(n_clusters=k, n_init=10, random_state=seed)."),
    ("test_types", "Return floats for scores and ints for labels."),
    ("test_invalid", "Every k must satisfy 2 <= k < len(X)."),
],
},
# ---------------------------------------------------------------- ml-capstone
{
"slug": "ml-capstone", "title": "Capstone: an End-to-End Tabular Model",
"difficulty": "advanced", "prereqs": ["sklearn-kmeans", "sklearn-column-transformer"],
"packages": ["numpy", "pandas", "scikit-learn"],
"objectives": ["Combine a stratified split, a ColumnTransformer and a classifier in one pipeline",
               "Tune the model with cross-validated grid search on the training set only",
               "Report a baseline, the cross-validated score and the final test scores"],
"tags": ["scikit-learn", "end-to-end", "pipeline", "grid-search", "evaluation"],
"sources": ["S012", "S091"], "entry": "end_to_end(df, target, numeric, categorical, seed=0)",
"article": r'''
# Capstone: an End-to-End Tabular Model

## Intuition
Everything in this topic fits into one recipe. Split once and lock the test set away. Build all
preprocessing into a pipeline. Tune with cross-validation on the training part only. Compare with
a baseline. Then — once — evaluate on the test set.

## Precise explanation
```python
X, y = df.drop(columns=[target]), df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=0)

prep = ColumnTransformer([...])                                       # [[sklearn-column-transformer]]
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])
search = GridSearchCV(pipe, {"model__C": [0.01, 0.1, 1, 10]},
                      cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="roc_auc")
search.fit(X_train, y_train)                                          # never sees the test set

baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
```

| Number | Comes from | Answers |
|---|---|---|
| baseline accuracy | `DummyClassifier` on test | what "doing nothing" scores |
| cross-validated AUC | `search.best_score_` | how good the chosen setting is, estimated on training data |
| test accuracy and AUC | `search.best_estimator_` on test | the honest final estimate |

## Worked example
For a churn table with 40% churners, the majority baseline has 0.60 accuracy. A tuned logistic
pipeline reaching 0.80 accuracy and 0.85 AUC on the test set is a real improvement; one at 0.61
accuracy is not, however good its training score.

## Common mistakes
* Preprocessing before splitting (leakage) or tuning on the test set.
* Reporting accuracy without the baseline on imbalanced data.
* Looking at test results, changing the model, and looking again — the test set is then a
  validation set.

## Why this matters
This is the workflow behind the house-price and spam/fraud project ideas, and the model you can
serve with FastAPI in "Serve your model".
''',
"statement": r'''
Write `end_to_end(df, target, numeric, categorical, seed=0)` for a binary 0/1 target column,
returning
`{"best_C": float, "cv_auc": float, "test_accuracy": float, "test_auc": float, "baseline_accuracy": float, "model": fitted_pipeline}`.

1. `train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)` where `X` is every
   column except the target.
2. Preprocess numeric columns with median imputation and scaling, categorical columns with
   most-frequent imputation and `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`.
3. Model `LogisticRegression(max_iter=1000)` named `"model"`; search `{"model__C": [0.01, 0.1, 1, 10]}`
   with `StratifiedKFold(5, shuffle=True, random_state=seed)` and `scoring="roc_auc"` on the training data.
4. Test accuracy and AUC come from the best estimator; the baseline is
   `DummyClassifier(strategy="most_frequent")` fitted on the training data, scored on the test data.

Raise `ValueError` if the target column is missing or not binary.
''',
"starter": r'''
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def end_to_end(df, target, numeric, categorical, seed=0):
    # TODO
    pass
''',
"hints": [
    "Check `target in df.columns` and that its values are exactly {0, 1}; split before anything is fitted.",
    "Build the ColumnTransformer as in the previous step and wrap it with the model in a Pipeline.",
    "Use `search.best_estimator_.predict_proba(X_test)[:, 1]` for the test AUC.",
],
"solution": r'''
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def end_to_end(df, target, numeric, categorical, seed=0):
    if target not in df.columns or set(df[target].unique()) != {0, 1}:
        raise ValueError("target must be a binary 0/1 column of df")
    X, y = df.drop(columns=[target]), df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=seed)
    prep = ColumnTransformer([
        ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), list(numeric)),
        ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                              OneHotEncoder(handle_unknown="ignore", sparse_output=False)), list(categorical)),
    ])
    pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])
    search = GridSearchCV(pipe, {"model__C": [0.01, 0.1, 1, 10]},
                          cv=StratifiedKFold(5, shuffle=True, random_state=seed), scoring="roc_auc")
    search.fit(X_train, y_train)
    best = search.best_estimator_
    baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
    return {"best_C": float(search.best_params_["model__C"]), "cv_auc": float(search.best_score_),
            "test_accuracy": float(best.score(X_test, y_test)),
            "test_auc": float(roc_auc_score(y_test, best.predict_proba(X_test)[:, 1])),
            "baseline_accuracy": float(baseline.score(X_test, y_test)), "model": best}
''',
"explanation": r'''
The split happens first, so the grid search, imputers, scaler and encoder only ever see training
rows. The search picks C by cross-validated AUC and refits on the whole training set; the test set
is used exactly once, next to a majority-class baseline that shows what the scores mean.
''',
"tests": r'''
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def churn(seed=0, n=400):
    rng = np.random.default_rng(seed)
    tenure = rng.integers(1, 60, n).astype(float)
    charges = rng.normal(70, 20, n)
    plan = rng.choice(["basic", "plus", "pro"], n)
    logit = 2.0 - 0.1 * tenure + 0.05 * (charges - 70) + np.where(plan == "basic", 1.5, 0.0)
    churned = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    tenure[rng.random(n) < 0.05] = np.nan
    return pd.DataFrame({"tenure": tenure, "charges": charges, "plan": plan, "churned": churned})


class TestEndToEnd(unittest.TestCase):
    def test_beats_baseline(self):
        r = S.end_to_end(churn(), "churned", ["tenure", "charges"], ["plan"])
        self.assertGreater(r["test_auc"], 0.75)
        self.assertGreater(r["test_accuracy"], r["baseline_accuracy"])

    def test_baseline_is_majority_share(self):
        df = churn(1)
        r = S.end_to_end(df, "churned", ["tenure", "charges"], ["plan"], seed=3)
        _, _, y_train, y_test = train_test_split(df.drop(columns=["churned"]), df["churned"],
                                                 test_size=0.25, stratify=df["churned"], random_state=3)
        majority = int(y_train.mean() >= 0.5)
        self.assertAlmostEqual(r["baseline_accuracy"], float((y_test == majority).mean()))

    def test_grid_choice(self):
        r = S.end_to_end(churn(2), "churned", ["tenure", "charges"], ["plan"])
        self.assertIn(r["best_C"], [0.01, 0.1, 1.0, 10.0])
        self.assertGreater(r["cv_auc"], 0.7)

    def test_model_handles_new_rows(self):
        r = S.end_to_end(churn(3), "churned", ["tenure", "charges"], ["plan"])
        new = pd.DataFrame({"tenure": [np.nan, 50.0], "charges": [95.0, 40.0], "plan": ["enterprise", "pro"]})
        proba = r["model"].predict_proba(new)[:, 1]
        self.assertEqual(proba.shape, (2,))
        self.assertGreater(proba[0], proba[1])

    def test_reproducible(self):
        a = S.end_to_end(churn(4), "churned", ["tenure", "charges"], ["plan"], seed=1)
        b = S.end_to_end(churn(4), "churned", ["tenure", "charges"], ["plan"], seed=1)
        self.assertEqual({k: v for k, v in a.items() if k != "model"}, {k: v for k, v in b.items() if k != "model"})

    def test_invalid_target(self):
        df = churn(5)
        with self.assertRaises(ValueError):
            S.end_to_end(df, "missing", ["tenure"], ["plan"])
        with self.assertRaises(ValueError):
            S.end_to_end(df.assign(churned=df["charges"]), "churned", ["tenure"], ["plan"])
''',
"feedback": [
    ("test_beats_baseline", "Tune with GridSearchCV on the training split, then score the best estimator on the test split."),
    ("test_baseline_is_majority_share", "Split with test_size=0.25, stratify=y, random_state=seed before fitting anything."),
    ("test_model_handles_new_rows", "Impute and use OneHotEncoder(handle_unknown='ignore') inside the pipeline."),
    ("test_invalid_target", "Raise ValueError if the target column is missing or not 0/1."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "house-price-predictor", "title": "House-Price Predictor",
"tags": ["regression", "pipelines", "feature-engineering"],
"brief": r'''
Build a model that estimates house prices from a table of homes, and an error analysis that shows
where it is wrong. Someone pricing a home should be able to see the estimate, a typical error, and
which kinds of homes the model struggles with.
''',
"uses": ["sklearn-estimator-api", "sklearn-train-test-split", "sklearn-cross-validation", "sklearn-column-transformer"],
"milestones": [
    "Load the data with pandas, look at missing values and the distribution of prices.",
    "Split once into train and test, and fit a mean baseline and a LinearRegression pipeline.",
    "Build a ColumnTransformer for numeric and categorical columns and compare models with 5-fold cross-validation.",
    "Try predicting log(price) and engineered features (age of house, price per room) and keep what helps.",
    "Evaluate once on the test set and list the 20 largest errors to look for patterns.",
],
"stretch": [
    "Tune a Ridge or gradient-boosting model with GridSearchCV.",
    "Report a prediction interval (for example from quantile regression) instead of a single number.",
    "Save the pipeline with joblib and load it in a separate script.",
],
"data": r'''
* California housing (20,640 districts, numeric features): `sklearn.datasets.fetch_california_housing()`
  downloads it the first time — see the
  [dataset page](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html).
* Ames house prices with many categorical columns: the
  [Kaggle competition data](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)
  (free account needed).
''',
"setup": r'''
```bash
pip install numpy pandas scikit-learn
python train.py
```
Keep notebooks for exploration, but put the final pipeline in a script you can rerun from scratch.
''',
},
{
"kind": "project", "slug": "spam-fraud-classifier", "title": "Spam or Fraud Classifier",
"tags": ["classification", "imbalanced-data", "thresholds"],
"brief": r'''
Build a classifier for a problem where the interesting class is rare — spam messages or fraudulent
transactions — and choose a decision threshold that reflects real costs: a missed fraud is
expensive, but so is blocking a real customer.
''',
"uses": ["classification-metrics", "sklearn-gradient-boosting", "sklearn-roc-pr", "ml-capstone"],
"milestones": [
    "Load the data, measure the class imbalance and fit a majority-class baseline.",
    "Train a logistic regression pipeline and a gradient-boosting model with stratified cross-validation.",
    "Compare them with ROC AUC and average precision, and plot both curves.",
    "Choose a threshold from the precision–recall curve on validation data for a target recall.",
    "Report the confusion matrix and the cost per 1,000 cases at that threshold on the test set.",
],
"stretch": [
    "Try class_weight='balanced' and compare it with moving the threshold.",
    "For SMS spam, turn the messages into TF-IDF features (see the NLP topic).",
    "Check how the precision changes if fraud becomes twice as rare after deployment.",
],
"data": r'''
* [SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) (UCI): 5,574
  labelled text messages, about 13% spam.
* Synthetic transactions: `sklearn.datasets.make_classification(n_samples=20000, weights=[0.98, 0.02], random_state=0)`
  ([documentation](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_classification.html)).
''',
"setup": r'''
```bash
pip install numpy pandas scikit-learn matplotlib
python fraud.py
```
''',
},
{
"kind": "project", "slug": "serve-your-model", "title": "Serve Your Model with FastAPI",
"tags": ["deployment", "fastapi", "model-serving"],
"brief": r'''
Put a trained scikit-learn pipeline behind a small web API, so other programs can send a JSON row
and get a prediction back — with input validation, a health check and tests, as a real service
would have.
''',
"uses": ["ml-capstone", "fastapi-routes", "pydantic-bodies", "response-models", "api-testing"],
"milestones": [
    "Train and save a pipeline from the capstone or house-price project with joblib.",
    "Create a FastAPI app that loads the model once at start-up and exposes GET /health.",
    "Add POST /predict with a Pydantic model describing one input row; return the prediction and probability.",
    "Reject bad input (missing fields, negative values) with clear 422 errors.",
    "Write TestClient tests for a valid request, an invalid one and the health check.",
],
"stretch": [
    "Accept a batch of rows in one request.",
    "Log each prediction with a timestamp and add GET /stats with simple counts.",
    "Package the service in a Dockerfile.",
],
"data": r'''
Use the model and data from the capstone (synthetic churn data you generate) or from the
house-price project. See [model persistence](https://scikit-learn.org/stable/model_persistence.html)
for saving pipelines.
''',
"setup": r'''
```bash
pip install fastapi uvicorn scikit-learn joblib pandas httpx
uvicorn app:app --reload
```
Then open http://127.0.0.1:8000/docs to try the endpoints. See
[running a server manually](https://fastapi.tiangolo.com/deployment/manually/).
''',
},
]
