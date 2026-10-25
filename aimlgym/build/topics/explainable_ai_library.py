"""Explainable AI with sklearn.inspection (library revision, Phase 6).

The library steps are followed by the NumPy versions they replace on the required path, kept as
optional deep dives: [[partial-dependence]] and [[permutation-importance]].
"""

PROBLEMS = [
# ---------------------------------------------------------------- xai-partial-dependence
{
"slug": "xai-partial-dependence", "title": "Partial Dependence with sklearn.inspection",
"difficulty": "intermediate", "prereqs": ["ice-curve", "sklearn-trees-forests"], "packages": ["numpy", "scikit-learn"],
"objectives": ["Compute partial dependence and ICE curves with sklearn.inspection.partial_dependence",
               "Control the grid with grid_resolution and percentiles",
               "Read the average effect of one feature from the curve"],
"tags": ["scikit-learn", "explainability", "partial-dependence", "ice"],
"sources": ["S012", "S091"], "entry": "pd_curve(model, X, feature, grid_resolution=20, kind=\"average\")",
"article": r'''
# Partial Dependence with sklearn.inspection

## Intuition
An ICE curve ([[ice-curve]]) shows how one prediction changes as one feature is varied. Averaging the
ICE curves over the dataset gives the **partial dependence**: the model's average response to that
feature, with the other features left as they are in the data.

## Precise explanation
```python
from sklearn.inspection import partial_dependence

result = partial_dependence(model, X, features=[0], grid_resolution=20, kind="average")
result["grid_values"][0]       # the feature values tried
result["average"][0]           # mean prediction at each grid value
partial_dependence(model, X, features=[0], kind="individual")["individual"][0]   # (n_samples, n_grid) ICE curves
```

* The grid spans the 5th to 95th percentile of the feature by default (`percentiles=(0.05, 0.95)`),
  so extreme outliers do not stretch it; `grid_resolution` caps the number of points (fewer if the
  feature has fewer unique values).
* `kind="both"` returns averages and individual curves together. For most models the average is the
  mean of the ICE curves ("brute" method); for tree ensembles `kind="average"` uses a faster
  "recursion" method that can differ slightly from averaging the individual curves.
* It works with any fitted estimator, including pipelines; for classifiers it uses predicted
  probabilities (or the decision function) of the positive class.
* For a linear model the partial dependence is a straight line whose slope is the coefficient (in the
  original units). Curved or step-shaped curves reveal non-linear effects.
* Partial dependence assumes the varied feature is not strongly correlated with the others — otherwise
  it averages over impossible combinations.

## Worked example
For y = 2x₀ + x₁² and a linear-regression pipeline, the partial dependence of feature 0 rises with
slope ≈ 2; for a random forest trained on the same data, the curve for feature 1 is U-shaped.

## What the library does inside
For every grid value it sets the feature to that value in a copy of `X`, predicts, and averages —
the procedure of [[partial-dependence]] (the optional deep dive after this step), with a faster
recursion method for tree ensembles.

## Common mistakes
* Reading a flat average curve as "no effect" when ICE curves cancel out (some up, some down).
* Ignoring correlated features.
* Using the `"values"` key from old scikit-learn versions; it is now `"grid_values"`.

## Why this matters
Partial dependence plots are the standard global explanation for tabular models; the house-price
explanation project idea uses them.
''',
"statement": r'''
Write `pd_curve(model, X, feature, grid_resolution=20, kind="average")` returning
`{"grid": list[float], "values": ...}` from `partial_dependence(model, X, features=[feature],
grid_resolution=grid_resolution, kind=kind)`:

* `kind="average"`: `values` is the list of average predictions (one per grid value);
* `kind="individual"`: `values` is a list of ICE curves, one list per row of `X`.

Raise `ValueError` for another kind or a feature index outside the columns of `X`.
''',
"starter": r'''
import numpy as np
from sklearn.inspection import partial_dependence


def pd_curve(model, X, feature, grid_resolution=20, kind="average"):
    # TODO
    pass
''',
"hints": [
    "Validate `kind in (\"average\", \"individual\")` and `0 <= feature < X.shape[1]`.",
    "`result = partial_dependence(model, X, features=[feature], grid_resolution=grid_resolution, kind=kind)`.",
    "`result[\"grid_values\"][0]` and `result[kind][0]`; convert with `.tolist()`.",
],
"solution": r'''
import numpy as np
from sklearn.inspection import partial_dependence


def pd_curve(model, X, feature, grid_resolution=20, kind="average"):
    X = np.asarray(X)
    if kind not in ("average", "individual"):
        raise ValueError("kind must be 'average' or 'individual'")
    if not 0 <= feature < X.shape[1]:
        raise ValueError("feature index out of range")
    result = partial_dependence(model, X, features=[feature], grid_resolution=grid_resolution, kind=kind)
    return {"grid": [float(v) for v in result["grid_values"][0]], "values": result[kind][0].tolist()}
''',
"explanation": r'''
`partial_dependence` builds the grid from the feature's central percentiles, predicts with the feature
replaced by each grid value, and either averages over rows (partial dependence) or keeps every row's
curve (ICE). The function returns the grid and the requested curves as plain lists.
''',
"tests": r'''
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def data(seed=0, n=300):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 3))
    return X, 2 * X[:, 0] + X[:, 1] ** 2 + rng.normal(scale=0.1, size=n)


class TestPdCurve(unittest.TestCase):
    def test_linear_slope(self):
        X, y = data()
        model = make_pipeline(StandardScaler(), LinearRegression()).fit(X, y)
        r = S.pd_curve(model, X, 0, grid_resolution=5)
        slopes = np.diff(r["values"]) / np.diff(r["grid"])
        self.assertTrue(np.allclose(slopes, model[-1].coef_[0] / model[0].scale_[0]))
        self.assertAlmostEqual(slopes[0], 2.0, delta=0.1)

    def test_u_shape_for_forest(self):
        X, y = data(1)
        model = RandomForestRegressor(50, random_state=0).fit(X, y)
        values = S.pd_curve(model, X, 1, grid_resolution=9)["values"]
        self.assertLess(values[4], values[0])
        self.assertLess(values[4], values[-1])

    def test_grid_within_percentiles(self):
        X, y = data(2)
        r = S.pd_curve(LinearRegression().fit(X, y), X, 0, grid_resolution=7)
        self.assertEqual(len(r["grid"]), 7)
        self.assertEqual(r["grid"], sorted(r["grid"]))
        lo, hi = np.percentile(X[:, 0], [2, 8]), np.percentile(X[:, 0], [92, 98])
        self.assertTrue(lo[0] <= r["grid"][0] <= lo[1] and hi[0] <= r["grid"][-1] <= hi[1])

    def test_individual_curves_average(self):
        X, y = data(3, n=60)
        model = make_pipeline(PolynomialFeatures(2), LinearRegression()).fit(X, y)
        ice = S.pd_curve(model, X, 0, grid_resolution=4, kind="individual")
        avg = S.pd_curve(model, X, 0, grid_resolution=4)
        self.assertEqual((len(ice["values"]), len(ice["values"][0])), (60, 4))
        self.assertTrue(np.allclose(np.mean(ice["values"], axis=0), avg["values"]))

    def test_types(self):
        X, y = data(4, n=40)
        r = S.pd_curve(LinearRegression().fit(X, y), X, 2, grid_resolution=3)
        self.assertTrue(all(type(v) is float for v in r["grid"] + r["values"]))

    def test_invalid(self):
        X, y = data(5, n=20)
        model = LinearRegression().fit(X, y)
        with self.assertRaises(ValueError):
            S.pd_curve(model, X, 3)
        with self.assertRaises(ValueError):
            S.pd_curve(model, X, 0, kind="both")
''',
"feedback": [
    ("test_linear_slope", "Use partial_dependence with features=[feature] and kind='average'."),
    ("test_grid_within_percentiles", "Return result['grid_values'][0] as the grid."),
    ("test_individual_curves_average", "For kind='individual' return result['individual'][0]."),
    ("test_invalid", "Reject unknown kinds and out-of-range feature indices."),
],
},
# ---------------------------------------------------------------- xai-permutation-importance
{
"slug": "xai-permutation-importance", "title": "Permutation Importance with sklearn.inspection",
"difficulty": "intermediate", "prereqs": ["xai-partial-dependence"], "packages": ["numpy", "pandas", "scikit-learn"],
"objectives": ["Measure feature importance with permutation_importance on held-out data",
               "Apply it to a whole pipeline so importances refer to the original columns",
               "Report the mean and spread over repeats"],
"tags": ["scikit-learn", "explainability", "feature-importance", "permutation-importance"],
"sources": ["S012", "S091"], "entry": "importance_table(model, X, y, n_repeats=10, seed=0, scoring=None)",
"article": r'''
# Permutation Importance with sklearn.inspection

## Intuition
How much does a model rely on a feature? Shuffle that feature's column — breaking its link with the
target while keeping its distribution — and see how much the score drops. A big drop means the model
needed the feature; no drop means it did not.

## Precise explanation
```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0, scoring="r2")
result.importances_mean        # mean score drop per feature
result.importances_std         # spread over the repeats
```

* Compute it on **held-out** data: on training data an overfitted model looks dependent on noise.
* Passing the **pipeline** (preprocessing + model) and a DataFrame gives importances for the original
  columns, even when a ColumnTransformer expands categories into many encoded columns.
* `n_repeats` shuffles each column several times; report mean ± standard deviation. Importances near
  zero (or slightly negative) mean "not used".
* Correlated features share importance: shuffling one leaves the other to carry the information, so
  both can look unimportant.
* Unlike tree `feature_importances_`, it works for any model and any scorer.

## Worked example
For y = 3·x₀ + 0.5·x₁ + noise, with x₂ pure noise, the importances on a test set are roughly
x₀ ≫ x₁ > 0 ≈ x₂.

## What the library does inside
For each feature and repeat it permutes the column with a seeded generator, re-scores the model and
subtracts from the baseline score — the loop of [[permutation-importance]] (the optional deep dive
after this step).

## Common mistakes
* Computing importances on the training set.
* Reading importance as causal effect or as the direction of the effect (use partial dependence).
* Dropping two correlated features because each looked unimportant alone.

## Why this matters
Permutation importance is the standard model-agnostic check of what a model relies on; it often
exposes leakage features that are "too important".
''',
"statement": r'''
Write `importance_table(model, X, y, n_repeats=10, seed=0, scoring=None)` for a fitted model (or
pipeline) and a pandas DataFrame `X`, returning a list of `(column, mean, std)` tuples sorted by mean
importance descending (ties by column name), using
`permutation_importance(model, X, y, n_repeats=n_repeats, random_state=seed, scoring=scoring)`.

Raise `ValueError` if `n_repeats < 1` or `X` is not a DataFrame.
''',
"starter": r'''
import pandas as pd
from sklearn.inspection import permutation_importance


def importance_table(model, X, y, n_repeats=10, seed=0, scoring=None):
    # TODO
    pass
''',
"hints": [
    "Check `isinstance(X, pd.DataFrame)` and the repeat count.",
    "`result = permutation_importance(model, X, y, n_repeats=n_repeats, random_state=seed, scoring=scoring)`.",
    "Zip `X.columns`, `result.importances_mean` and `result.importances_std`, then sort by `(-mean, column)`.",
],
"solution": r'''
import pandas as pd
from sklearn.inspection import permutation_importance


def importance_table(model, X, y, n_repeats=10, seed=0, scoring=None):
    if not isinstance(X, pd.DataFrame) or n_repeats < 1:
        raise ValueError("need a DataFrame and n_repeats >= 1")
    result = permutation_importance(model, X, y, n_repeats=n_repeats, random_state=seed, scoring=scoring)
    rows = [(str(c), float(m), float(s)) for c, m, s in zip(X.columns, result.importances_mean, result.importances_std)]
    return sorted(rows, key=lambda row: (-row[1], row[0]))
''',
"explanation": r'''
The function shuffles each original column of the DataFrame several times, measures the drop in score
of the whole pipeline, and reports the mean and spread per column, most important first.
''',
"tests": r'''
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def frame(seed, n=300):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({"x0": rng.normal(size=n), "x1": rng.normal(size=n), "noise": rng.normal(size=n),
                      "city": rng.choice(["a", "b", "c"], n)})
    y = 3 * X["x0"] + 0.5 * X["x1"] + X["city"].map({"a": 0.0, "b": 2.0, "c": -2.0}) + rng.normal(scale=0.1, size=n)
    return X, y


def pipeline():
    prep = ColumnTransformer([("num", "passthrough", ["x0", "x1", "noise"]),
                              ("cat", OneHotEncoder(sparse_output=False), ["city"])])
    return Pipeline([("prep", prep), ("model", LinearRegression())])


class TestImportanceTable(unittest.TestCase):
    def test_order(self):
        X, y = frame(0)
        Xt, yt = frame(1)
        table = S.importance_table(pipeline().fit(X, y), Xt, yt)
        self.assertEqual([row[0] for row in table][:2], ["x0", "city"])
        self.assertEqual(table[-1][0], "noise")

    def test_original_columns(self):
        X, y = frame(2)
        table = S.importance_table(pipeline().fit(X, y), X, y, n_repeats=3)
        self.assertEqual(sorted(row[0] for row in table), ["city", "noise", "x0", "x1"])

    def test_noise_near_zero(self):
        X, y = frame(3)
        Xt, yt = frame(4)
        noise = {r[0]: r for r in S.importance_table(pipeline().fit(X, y), Xt, yt)}["noise"]
        self.assertLess(abs(noise[1]), 0.01)

    def test_matches_library(self):
        X, y = frame(5)
        model = pipeline().fit(X, y)
        table = S.importance_table(model, X, y, n_repeats=4, seed=2, scoring="r2")
        ref = permutation_importance(model, X, y, n_repeats=4, random_state=2, scoring="r2")
        means = dict(zip(X.columns, ref.importances_mean))
        for column, mean, std in table:
            self.assertAlmostEqual(mean, float(means[column]))

    def test_types_and_reproducible(self):
        X, y = frame(6, n=80)
        model = pipeline().fit(X, y)
        a = S.importance_table(model, X, y, n_repeats=3, seed=1)
        self.assertEqual(a, S.importance_table(model, X, y, n_repeats=3, seed=1))
        self.assertTrue(all(type(m) is float and type(s) is float for _, m, s in a))

    def test_invalid(self):
        X, y = frame(7, n=20)
        model = pipeline().fit(X, y)
        with self.assertRaises(ValueError):
            S.importance_table(model, X.to_numpy(), y)
        with self.assertRaises(ValueError):
            S.importance_table(model, X, y, n_repeats=0)
''',
"feedback": [
    ("test_order", "Sort rows by mean importance, largest first."),
    ("test_original_columns", "Pass the whole pipeline and the DataFrame so rows are original columns."),
    ("test_matches_library", "Use permutation_importance with random_state=seed and the given scoring."),
    ("test_invalid", "Require a DataFrame and n_repeats >= 1."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "explain-house-prices", "title": "Explain Your House-Price Model",
"tags": ["explainability", "reporting", "shap"],
"brief": r'''
Write an explanation report for the house-price model from the Machine Learning project: which
features matter, how each one moves the price, why one particular house got its estimate, and where
the explanations disagree.
''',
"uses": ["xai-partial-dependence", "xai-permutation-importance", "exact-shapley", "lime-local", "counterfactual-search"],
"milestones": [
    "Load your trained pipeline and a held-out test set.",
    "Rank features with permutation importance (mean ± std) and plot the top ten.",
    "Plot partial dependence and ICE curves for the three most important features.",
    "Explain five individual predictions with SHAP values and compare them with LIME-style local fits.",
    "Write a one-page report: findings, surprising effects, and the limits of each method.",
],
"stretch": [
    "Find counterfactuals: the smallest change that moves a house into a different price band.",
    "Check whether correlated features (rooms and area) split their importance.",
    "Build a small web page that shows the explanation for any house id.",
],
"data": r'''
Use the house-price project's data (California housing or Ames). The [SHAP library](https://shap.readthedocs.io/en/latest/)
computes Shapley values efficiently for tree models; it is not part of the graded course because it
needs compiled dependencies.
''',
"setup": r'''
```bash
pip install scikit-learn pandas matplotlib shap
python explain.py
```
''',
},
]
