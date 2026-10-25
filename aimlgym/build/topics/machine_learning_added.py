"""Machine Learning steps added in the 2026-10 revision: the vocabulary of supervised learning
with baseline models, and polynomial features with over- and under-fitting."""

PROBLEMS = [
# ---------------------------------------------------------------- ml-baselines
{
"slug": "ml-baselines", "title": "Features, Labels and Baseline Models",
"difficulty": "beginner", "prereqs": ["axis-aggregations"], "packages": ["numpy"],
"objectives": ["Describe a dataset as a feature matrix X and a label vector y",
               "Write models as classes with fit and predict methods",
               "Build mean and majority-class baselines and explain why every model needs one",
               "Refuse to predict before fitting"],
"tags": ["supervised-learning", "features", "labels", "baselines", "fit-predict"],
"sources": ["S012", "S089"], "entry": "class MeanRegressor; class MajorityClassifier; mse(y_true, y_pred); accuracy(y_true, y_pred)",
"article": r'''
# Features, Labels and Baseline Models

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
''',
"statement": r'''
Implement with NumPy:

* `class MeanRegressor` — `fit(X, y)` stores `self.mean_ = float(mean of y)` and returns `self`;
  `predict(X)` returns a float array with one copy of the mean per row of `X`. Calling
  `predict` before `fit` raises `ValueError`.
* `class MajorityClassifier` — `fit` stores `self.label_`, the most frequent label (ties: the
  smallest label); `predict` returns an array of that label, one per row; `ValueError` before
  `fit`.
* `mse(y_true, y_pred)` and `accuracy(y_true, y_pred)` as floats; raise `ValueError` if the
  lengths differ or are 0.

`X` may be a list of lists or a 2-D array; only its number of rows matters to these baselines.
''',
"starter": r'''
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
''',
"hints": [
    "Before fitting, the attribute does not exist: check `hasattr(self, \"mean_\")` in `predict`.",
    "`labels, counts = np.unique(y, return_counts=True)`; `np.unique` sorts labels, so `labels[np.argmax(counts)]` picks the smallest on ties.",
    "`np.full(len(X), self.mean_)` repeats a value; MSE is `np.mean((y_true - y_pred) ** 2)`.",
],
"solution": r'''
import numpy as np


class MeanRegressor:
    def fit(self, X, y):
        self.mean_ = float(np.mean(np.asarray(y, dtype=float)))
        return self

    def predict(self, X):
        if not hasattr(self, "mean_"):
            raise ValueError("call fit before predict")
        return np.full(len(X), self.mean_)


class MajorityClassifier:
    def fit(self, X, y):
        labels, counts = np.unique(np.asarray(y), return_counts=True)
        self.label_ = labels[np.argmax(counts)]
        return self

    def predict(self, X):
        if not hasattr(self, "label_"):
            raise ValueError("call fit before predict")
        return np.full(len(X), self.label_)


def _check(y_true, y_pred):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    if len(y_true) != len(y_pred) or len(y_true) == 0:
        raise ValueError("inputs must be non-empty and the same length")
    return y_true, y_pred


def mse(y_true, y_pred):
    y_true, y_pred = _check(y_true, y_pred)
    return float(np.mean((y_true.astype(float) - y_pred.astype(float)) ** 2))


def accuracy(y_true, y_pred):
    y_true, y_pred = _check(y_true, y_pred)
    return float(np.mean(y_true == y_pred))
''',
"explanation": r'''
Each baseline learns a single value in `fit` and repeats it in `predict`, using the row count of
`X` so the output has one prediction per example. `np.unique` returns sorted labels, so taking
the first maximum count resolves ties toward the smallest label. Missing attributes signal an
unfitted model.
''',
"tests": r'''
import numpy as np

X_TRAIN = np.zeros((3, 2))
X_TEST = np.zeros((2, 2))


class TestBaselines(unittest.TestCase):
    def test_mean_regressor(self):
        m = S.MeanRegressor().fit(X_TRAIN, [3, 5, 10])
        self.assertEqual(m.mean_, 6.0)
        np.testing.assert_array_equal(m.predict(X_TEST), [6.0, 6.0])

    def test_fit_returns_self(self):
        m = S.MeanRegressor()
        self.assertIs(m.fit(X_TRAIN, [1, 2, 3]), m)
        c = S.MajorityClassifier()
        self.assertIs(c.fit(X_TRAIN, ["a", "b", "b"]), c)

    def test_predict_before_fit(self):
        for model in (S.MeanRegressor(), S.MajorityClassifier()):
            with self.assertRaises(ValueError):
                model.predict(X_TEST)

    def test_majority(self):
        c = S.MajorityClassifier().fit(X_TRAIN, ["a", "b", "b"])
        self.assertEqual(c.predict(X_TEST).tolist(), ["b", "b"])

    def test_majority_tie_smallest(self):
        c = S.MajorityClassifier().fit(np.zeros((4, 1)), [2, 1, 2, 1])
        self.assertEqual(c.label_, 1)

    def test_metrics(self):
        self.assertEqual(S.mse([4, 8], [6, 6]), 4.0)
        self.assertEqual(S.accuracy(["a", "b", "b", "c"], ["a", "b", "a", "a"]), 0.5)
        with self.assertRaises(ValueError):
            S.mse([1, 2], [1])
        with self.assertRaises(ValueError):
            S.accuracy([], [])

    def test_imbalanced_baseline_accuracy(self):
        y = np.array([0] * 95 + [1] * 5)
        c = S.MajorityClassifier().fit(np.zeros((100, 3)), y)
        self.assertEqual(S.accuracy(y, c.predict(np.zeros((100, 3)))), 0.95)
''',
"feedback": [
    ("test_mean_regressor", "Store the training mean in `self.mean_` and repeat it once per row of X."),
    ("test_fit_returns_self", "End `fit` with `return self`."),
    ("test_predict_before_fit", "Raise ValueError in `predict` if the model has not been fitted."),
    ("test_majority_tie_smallest", "Use `np.unique(..., return_counts=True)` and `np.argmax`, which picks the first (smallest) label on ties."),
    ("test_metrics", "Check that lengths match and are non-zero before computing."),
],
"library": {
"text": r'''
scikit-learn ships these baselines as `sklearn.dummy.DummyRegressor(strategy="mean")` and
`DummyClassifier(strategy="most_frequent")`, and the metrics as
`sklearn.metrics.mean_squared_error` and `accuracy_score`. Every scikit-learn estimator uses the
same `fit`/`predict` interface you just wrote, so later models can be swapped in without changing
the surrounding code. These comparisons run only when scikit-learn is installed.
''',
"optional": ["scikit-learn"],
"tests": r'''
try:
    from sklearn.dummy import DummyClassifier, DummyRegressor
    from sklearn.metrics import accuracy_score, mean_squared_error
except ImportError:
    DummyRegressor = None


@unittest.skipIf(DummyRegressor is None, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_dummy_regressor(self):
        y = [1.5, 2.0, 7.25, 4.0]
        ours = S.MeanRegressor().fit(np.zeros((4, 1)), y).predict(np.zeros((3, 1)))
        theirs = DummyRegressor(strategy="mean").fit(np.zeros((4, 1)), y).predict(np.zeros((3, 1)))
        np.testing.assert_allclose(ours, theirs)

    def test_dummy_classifier_and_metrics(self):
        y = [3, 1, 3, 1, 2]
        ours = S.MajorityClassifier().fit(np.zeros((5, 1)), y).predict(np.zeros((5, 1)))
        theirs = DummyClassifier(strategy="most_frequent").fit(np.zeros((5, 1)), y).predict(np.zeros((5, 1)))
        np.testing.assert_array_equal(ours, theirs)
        self.assertAlmostEqual(S.accuracy(y, ours), accuracy_score(y, theirs))
        self.assertAlmostEqual(S.mse([1, 2, 4], [2, 2, 2]), mean_squared_error([1, 2, 4], [2, 2, 2]))
''',
},
},
# ---------------------------------------------------------------- polynomial-overfitting
{
"slug": "polynomial-overfitting", "title": "Polynomial Features and Overfitting by Hand", "optional": True,
"difficulty": "intermediate", "prereqs": ["least-squares-line", "train-test-split"], "packages": ["numpy"],
"objectives": ["Turn one feature into polynomial features [1, x, x², …]",
               "Fit polynomial models with least squares",
               "Show that training error falls with degree while test error eventually rises",
               "Choose model complexity using held-out data"],
"tags": ["polynomial-regression", "overfitting", "underfitting", "model-selection", "bias-variance"],
"sources": ["S012", "S090", "S013"], "entry": "poly_features(x, degree); fit_poly(x, y, degree); predict_poly(coef, x); errors_by_degree(x_tr, y_tr, x_te, y_te, degrees); best_degree(errors)",
"article": r'''
# Polynomial Features and Overfitting

## Intuition
A straight line cannot follow a curve: it **underfits**. A polynomial of very high degree can pass
through every training point, wiggling wildly in between: it **overfits** — it memorises noise
and predicts new points badly. The right complexity sits in between, and the only honest way to
find it is to measure error on data the model did not train on.

## Precise explanation
* **Polynomial features**: for a single input $x$, build columns $[1, x, x^2, \dots, x^d]$. A
  *linear* model on these columns is a degree-$d$ polynomial in $x$ — so least squares still
  applies.
* **Fitting**: solve $\min_w \lVert Xw - y\rVert^2$ with `np.linalg.lstsq(X, y, rcond=None)`,
  which handles the case where columns are nearly dependent.
* **Training error never increases with degree**: each larger model contains the smaller one (set
  the extra coefficients to 0), so its best training fit is at least as good.
* **Test error** first falls (less underfitting), then rises (overfitting). Pick the degree with the
  lowest error on held-out data; [[k-fold-cv]] makes that choice more reliable.
* **Bias–variance**: simple models are biased (systematically wrong); complex models have high
  variance (very sensitive to which training points you happened to get).

## Worked example
Ten training points from $y = 1 + 2x - 3x^2$ plus small noise: degree 1 leaves a large training
error; degree 2 fits almost perfectly on both sets; degree 9 interpolates all ten training points
(training error ≈ 0) but its test error is far larger than degree 2's.

## Common mistakes
* Selecting the degree by training error — it always picks the largest degree.
* Using the test set to choose the degree and then reporting that same test error as final.
* Forgetting the constant column, which forces the curve through the origin.

## Why this matters
Every model has a complexity knob (tree depth, number of neighbours, network size, training
epochs). Recognising over- and underfitting from train/test errors is a core ML skill.
''',
"statement": r'''
Implement (`x` and `y` are 1-D arrays or lists):

1. `poly_features(x, degree)` → array of shape `(len(x), degree + 1)` with columns
   $x^0, x^1, \dots, x^{degree}$.
2. `fit_poly(x, y, degree)` → coefficient array (lowest power first) from
   `np.linalg.lstsq(poly_features(x, degree), y, rcond=None)`.
3. `predict_poly(coef, x)` → predictions $\sum_k c_k x^k$.
4. `errors_by_degree(x_tr, y_tr, x_te, y_te, degrees)` → dict degree → `(train_mse, test_mse)`
   as floats.
5. `best_degree(errors)` → the degree with the smallest **test** MSE (ties: the smaller degree).
''',
"starter": r'''
import numpy as np


def poly_features(x, degree):
    # TODO
    x = np.asarray(x, dtype=float)
    return x.reshape(-1, 1)


def fit_poly(x, y, degree):
    # TODO
    return np.zeros(degree + 1)


def predict_poly(coef, x):
    # TODO
    return np.zeros(len(x))


def errors_by_degree(x_tr, y_tr, x_te, y_te, degrees):
    # TODO
    return {}


def best_degree(errors):
    # TODO
    return min(errors)
''',
"hints": [
    "`np.column_stack([x ** k for k in range(degree + 1)])` builds the feature matrix.",
    "`coef, *_ = np.linalg.lstsq(X, y, rcond=None)`; predictions are `poly_features(x, len(coef) - 1) @ coef`.",
    "`min(errors, key=lambda d: (errors[d][1], d))` picks the lowest test error, then the smaller degree.",
],
"solution": r'''
import numpy as np


def poly_features(x, degree):
    x = np.asarray(x, dtype=float)
    return np.column_stack([x ** k for k in range(degree + 1)])


def fit_poly(x, y, degree):
    coef, *_ = np.linalg.lstsq(poly_features(x, degree), np.asarray(y, dtype=float), rcond=None)
    return coef


def predict_poly(coef, x):
    return poly_features(x, len(coef) - 1) @ coef


def _mse(y, yhat):
    return float(np.mean((np.asarray(y, dtype=float) - yhat) ** 2))


def errors_by_degree(x_tr, y_tr, x_te, y_te, degrees):
    out = {}
    for d in degrees:
        coef = fit_poly(x_tr, y_tr, d)
        out[d] = (_mse(y_tr, predict_poly(coef, x_tr)), _mse(y_te, predict_poly(coef, x_te)))
    return out


def best_degree(errors):
    return min(errors, key=lambda d: (errors[d][1], d))
''',
"explanation": r'''
Polynomial regression is linear regression on engineered features, so the same least-squares
solver fits every degree. Evaluating each fitted model on both the training and the held-out
points exposes the familiar pattern, and selection uses only the held-out error with a
deterministic tie-break.
''',
"tests": r'''
import numpy as np

X_TR = np.linspace(0, 1, 10)
NOISE = np.array([0.05, -0.05] * 5)
Y_TR = 1 + 2 * X_TR - 3 * X_TR ** 2 + NOISE
X_TE = np.linspace(0.03, 0.97, 9)
Y_TE = 1 + 2 * X_TE - 3 * X_TE ** 2


class TestPolynomial(unittest.TestCase):
    def test_features(self):
        F = S.poly_features([2.0, 3.0], 3)
        np.testing.assert_allclose(F, [[1, 2, 4, 8], [1, 3, 9, 27]])
        self.assertEqual(S.poly_features(X_TR, 0).shape, (10, 1))

    def test_exact_recovery(self):
        x = np.linspace(-1, 2, 7)
        coef = S.fit_poly(x, 1 + 2 * x - 3 * x ** 2, 2)
        np.testing.assert_allclose(coef, [1, 2, -3], atol=1e-9)

    def test_predict(self):
        np.testing.assert_allclose(S.predict_poly(np.array([1.0, 0.0, 2.0]), [0, 1, 2]), [1, 3, 9])

    def test_training_error_non_increasing(self):
        errs = S.errors_by_degree(X_TR, Y_TR, X_TE, Y_TE, range(0, 10))
        train = [errs[d][0] for d in range(10)]
        for a, b in zip(train, train[1:]):
            self.assertLessEqual(b, a + 1e-12)
        self.assertLess(errs[9][0], 1e-12)

    def test_overfitting_visible(self):
        errs = S.errors_by_degree(X_TR, Y_TR, X_TE, Y_TE, [1, 2, 9])
        self.assertGreater(errs[1][1], errs[2][1])
        self.assertGreater(errs[9][1], 10 * errs[2][1])

    def test_best_degree(self):
        errs = S.errors_by_degree(X_TR, Y_TR, X_TE, Y_TE, range(0, 10))
        self.assertEqual(S.best_degree(errs), 2)
        self.assertEqual(S.best_degree({3: (0.0, 1.0), 1: (0.5, 1.0), 2: (0.1, 2.0)}), 1)
''',
"feedback": [
    ("test_features", "Columns must be x**0, x**1, ..., x**degree in that order."),
    ("test_exact_recovery", "Fit with `np.linalg.lstsq(X, y, rcond=None)` on the polynomial features."),
    ("test_training_error_non_increasing", "Compute the training error on the training points with the coefficients fitted on them."),
    ("test_overfitting_visible", "Evaluate each model on the test points too; don't refit on them."),
    ("test_best_degree", "Choose by test error (the second value), breaking ties with the smaller degree."),
],
"library": {
"text": r'''
NumPy's `np.polyfit(x, y, degree)` fits the same polynomial (it returns the **highest** power
first), and scikit-learn builds it as a pipeline:
`make_pipeline(PolynomialFeatures(degree), LinearRegression())`. `PolynomialFeatures` is what
your `poly_features` does; `LinearRegression` solves the least-squares problem. Their scikit-learn
example "Underfitting vs. Overfitting" draws the same curves you computed. The tests compare
with `np.polyfit`, and with scikit-learn when it is installed.
''',
"optional": ["scikit-learn"],
"tests": r'''
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures
except ImportError:
    LinearRegression = None


class TestAgainstLibrary(unittest.TestCase):
    def test_matches_polyfit(self):
        np.testing.assert_allclose(S.fit_poly(X_TR, Y_TR, 3), np.polyfit(X_TR, Y_TR, 3)[::-1], atol=1e-8)

    @unittest.skipIf(LinearRegression is None, "scikit-learn not installed")
    def test_matches_sklearn_pipeline(self):
        model = make_pipeline(PolynomialFeatures(3), LinearRegression()).fit(X_TR.reshape(-1, 1), Y_TR)
        ours = S.predict_poly(S.fit_poly(X_TR, Y_TR, 3), X_TE)
        np.testing.assert_allclose(ours, model.predict(X_TE.reshape(-1, 1)), atol=1e-8)
''',
},
},
]
