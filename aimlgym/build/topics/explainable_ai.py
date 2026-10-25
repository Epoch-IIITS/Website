"""Problem definitions for the explainable ai topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- linear-contributions
{
"slug": "linear-contributions", "title": "Linear Model Contributions",
"difficulty": "beginner", "prereqs": ["least-squares-line"], "packages": ["numpy"],
"objectives": ["Attribute a linear prediction to features relative to a baseline",
               "Verify that contributions sum to prediction − baseline prediction",
               "Explain why the baseline choice matters"],
"tags": ["feature-attribution", "linear-models", "baseline", "local-explanation"],
"sources": ["S024"], "entry": "contributions(w, b, x, baseline)",
"article": r'''
# Explaining a Linear Prediction

## Intuition
A linear model is a weighted sum, so its prediction splits naturally into one piece per feature.
But "feature 2 contributed +30" only makes sense *relative to something*: compared with an average
customer, a zero input, or last month's value.

## Precise explanation
For $f(x) = w\cdot x + b$ and a **baseline** (reference) input $x'$ (often the training mean):
$$\phi_j = w_j\,(x_j - x'_j),\qquad \sum_j \phi_j = f(x) - f(x').$$
The second property — contributions add up exactly to the difference from the baseline prediction —
is called **efficiency** (or local accuracy). Using $\phi_j = w_jx_j$ (baseline 0) is a special case
and can be misleading when 0 is not a meaningful input (age 0, temperature 0 K).
Interpretation also depends on feature scale: standardised features make $w_j$ comparable.

## Worked example
w = [2, −1], b = 5, x = [3, 4], baseline = mean [1, 1]: φ = [4, −3]; f(x) = 7, f(x′) = 6,
sum φ = 1 = 7 − 6 ✓.

## Common mistakes
* Reporting $w_j$ alone as "importance" for one prediction (ignores the input value).
* Forgetting the baseline: contributions then do not add up to anything interpretable.
* Comparing weights of unscaled features.

## Why this matters
This is the simplest *exact* attribution; Shapley values ([[exact-shapley]]) reduce to exactly this formula for
linear models with independent features.
''',
"statement": r'''
Write `contributions(w, b, x, baseline)` returning a dict
`{"phi": array, "prediction": float, "baseline_prediction": float}` for a linear model. Raise
`ValueError` if lengths differ.

**Example**
```python
r = contributions(np.array([2., -1.]), 5.0, np.array([3., 4.]), np.array([1., 1.]))
r["phi"], r["prediction"], r["baseline_prediction"]   # ([4., -3.], 7.0, 6.0)
```
''',
"starter": r'''
import numpy as np


def contributions(w, b, x, baseline):
    pass
''',
"hints": [
    "Convert all inputs with `np.asarray(..., float)` and compare shapes.",
    "`phi = w * (x - baseline)`.",
    "`prediction = float(w @ x + b)`; baseline prediction similarly.",
],
"solution": r'''
import numpy as np


def contributions(w, b, x, baseline):
    w, x, base = (np.asarray(a, dtype=float) for a in (w, x, baseline))
    if not (w.shape == x.shape == base.shape):
        raise ValueError("w, x and baseline must have the same shape")
    return {"phi": w * (x - base), "prediction": float(w @ x + b),
            "baseline_prediction": float(w @ base + b)}
''',
"explanation": r'''
Each feature's contribution is its weight times its deviation from the baseline; by linearity these
sum exactly to the change in prediction relative to the baseline input.
''',
"tests": r'''
import numpy as np

class TestLinearContrib(unittest.TestCase):
    def test_example(self):
        r = S.contributions(np.array([2., -1.]), 5.0, np.array([3., 4.]), np.array([1., 1.]))
        np.testing.assert_allclose(r["phi"], [4., -3.])
        self.assertEqual((r["prediction"], r["baseline_prediction"]), (7.0, 6.0))

    def test_efficiency(self):
        rng = np.random.default_rng(0)
        w, x, base = rng.normal(size=6), rng.normal(size=6), rng.normal(size=6)
        r = S.contributions(w, 0.3, x, base)
        self.assertAlmostEqual(r["phi"].sum(), r["prediction"] - r["baseline_prediction"])

    def test_at_baseline_zero(self):
        r = S.contributions(np.array([1., 2.]), 0.0, np.array([5., 5.]), np.array([5., 5.]))
        np.testing.assert_allclose(r["phi"], 0)

    def test_zero_weight_zero_contrib(self):
        r = S.contributions(np.array([0., 3.]), 0.0, np.array([100., 1.]), np.array([0., 0.]))
        self.assertEqual(r["phi"][0], 0.0)

    def test_baseline_matters(self):
        w, x = np.array([1.0]), np.array([10.0])
        a = S.contributions(w, 0, x, np.array([0.0]))["phi"][0]
        b = S.contributions(w, 0, x, np.array([9.0]))["phi"][0]
        self.assertNotEqual(a, b)

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.contributions(np.ones(2), 0, np.ones(3), np.ones(2))
''',
"feedback": [
    ("test_efficiency", "Contributions must be w * (x − baseline) so they sum to f(x) − f(baseline)."),
    ("test_example", "Return prediction and baseline_prediction as floats including the bias."),
    ("test_at_baseline_zero", "At the baseline every contribution is zero."),
    ("test_mismatch", "Validate that all vectors have the same length."),
],
},
# ---------------------------------------------------------------- top-k-attributions
{
"slug": "top-k-attributions", "title": "Ranking Attributions",
"difficulty": "beginner", "prereqs": ["linear-contributions"], "packages": ["numpy"],
"objectives": ["Rank features by absolute attribution", "Report direction (sign) and share of total effect",
               "Produce a deterministic, human-readable explanation"],
"tags": ["feature-attribution", "ranking", "explanations", "reporting"],
"sources": ["S024"], "entry": "top_attributions(names, phi, k=3)",
"article": r'''
# Presenting Attributions

## Intuition
An explanation with 300 numbers explains nothing. Show the few features that moved the prediction
most, with their direction ("raised"/"lowered") and how much of the total effect they account for.

## Precise explanation
Given attributions $\phi_j$ (e.g. from [[linear-contributions]], [[exact-shapley]]):
* rank by $|\phi_j|$ descending (ties → feature name ascending, for determinism);
* direction: "+" if $\phi_j > 0$, "−" if $\phi_j < 0$, "0" otherwise;
* share $= |\phi_j| / \sum_i |\phi_i|$ (0 if all attributions are 0).
Sorting by absolute value matters: a large negative effect is as important as a large positive one.

## Worked example
names [age, income, debt], φ = [0.5, −2.0, 1.5] → ranking income (−, 0.5), debt (+, 0.375),
age (+, 0.125).

## Common mistakes
* Sorting by signed value (hides strong negative effects).
* Shares computed from signed sums (can divide by ~0).
* Non-deterministic order for ties.

## Why this matters
Explanations are for people; clear, stable presentation is part of building trustworthy systems
(Molnar's book discusses human-friendly explanations).
''',
"statement": r'''
Write `top_attributions(names, phi, k=3)` returning a list of up to `k` tuples
`(name, value, direction, share)` ranked as above, `value` and `share` floats, `direction` one of
`"+"`, `"-"`, `"0"`. Raise `ValueError` if lengths differ or `k < 1`.

**Example**
```python
top_attributions(["age", "income", "debt"], np.array([0.5, -2.0, 1.5]), k=2)
# [('income', -2.0, '-', 0.5), ('debt', 1.5, '+', 0.375)]
```
''',
"starter": r'''
import numpy as np


def top_attributions(names, phi, k=3):
    return []
''',
"hints": [
    "`total = np.abs(phi).sum()`.",
    "Sort indices with key `(-abs(phi[i]), names[i])`.",
    "Direction via comparisons with 0; share = abs / total (0 if total is 0).",
],
"solution": r'''
import numpy as np


def top_attributions(names, phi, k=3):
    phi = np.asarray(phi, dtype=float)
    if len(names) != len(phi):
        raise ValueError("names and phi must have the same length")
    if k < 1:
        raise ValueError("k must be >= 1")
    total = float(np.abs(phi).sum())
    order = sorted(range(len(phi)), key=lambda i: (-abs(phi[i]), names[i]))
    out = []
    for i in order[:k]:
        v = float(phi[i])
        d = "+" if v > 0 else "-" if v < 0 else "0"
        out.append((names[i], v, d, abs(v) / total if total else 0.0))
    return out
''',
"explanation": r'''
Ranking uses absolute values with an alphabetical tie-break; each entry reports the signed value,
its direction and its share of the total absolute effect.
''',
"tests": r'''
import numpy as np

N = ["age", "income", "debt"]

class TestTopAttr(unittest.TestCase):
    def test_example(self):
        self.assertEqual(S.top_attributions(N, np.array([0.5, -2.0, 1.5]), k=2),
                         [("income", -2.0, "-", 0.5), ("debt", 1.5, "+", 0.375)])

    def test_shares_sum(self):
        r = S.top_attributions(N, np.array([0.5, -2.0, 1.5]), k=3)
        self.assertAlmostEqual(sum(t[3] for t in r), 1.0)

    def test_ties_alphabetical(self):
        r = S.top_attributions(["b", "a", "c"], np.array([1.0, -1.0, 0.5]))
        self.assertEqual([t[0] for t in r], ["a", "b", "c"])

    def test_zero(self):
        r = S.top_attributions(["x", "y"], np.array([0.0, 0.0]))
        self.assertEqual(r, [("x", 0.0, "0", 0.0), ("y", 0.0, "0", 0.0)])

    def test_k_larger(self):
        self.assertEqual(len(S.top_attributions(N, np.array([1., 2., 3.]), k=10)), 3)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.top_attributions(N, np.array([1.0]))
        with self.assertRaises(ValueError):
            S.top_attributions(N, np.ones(3), k=0)
''',
"feedback": [
    ("test_example", "Rank by absolute value; keep the signed value in the output."),
    ("test_ties_alphabetical", "Break ties on |phi| by name ascending."),
    ("test_zero", "When all attributions are 0, shares are 0 and direction is '0'."),
    ("test_shares_sum", "share = |phi_j| / Σ|phi|."),
],
},
# ---------------------------------------------------------------- decision-path
{
"slug": "decision-path", "title": "Tracing a Decision Path",
"difficulty": "beginner", "prereqs": ["decision-stump-gini"], "packages": [],
"objectives": ["Traverse a tree model represented as nested dicts", "Record each condition tested",
               "Generate a rule-style explanation"],
"tags": ["decision-trees", "interpretable-models", "rules", "intrinsic-explanations"],
"sources": ["S024"], "entry": "predict_with_path(tree, x, feature_names)",
"article": r'''
# Decision Paths: Explanations for Free

## Intuition
A decision tree is interpretable by construction: the explanation of a prediction is the list of
questions asked on the way to the leaf. "Income ≤ 30k → yes; debt > 5k → yes → reject."

## Precise explanation
Represent a tree as nested dicts:
* internal node: `{"feature": j, "threshold": t, "left": node, "right": node}` — go **left** if
  $x_j \le t$ (as in [[decision-stump-gini]]), else right;
* leaf: `{"value": v}`.
The path is the sequence of (feature, operator, threshold) conditions satisfied. This is an
**intrinsic** explanation (the model *is* the explanation), unlike post-hoc methods ([[partial-dependence]]+). Deep
trees produce long paths that are no longer easy to read — interpretability depends on size.

```mermaid
flowchart TD
  A{"income ≤ 30?"} -- yes --> B{"debt ≤ 5?"}
  A -- no --> L1["approve"]
  B -- yes --> L2["approve"]
  B -- no --> L3["reject"]
```

## Worked example
x = {income 25, debt 8}: income ≤ 30 ✓ → debt ≤ 5 ✗ → "reject"; path
["income <= 30", "debt > 5"].

## Common mistakes
* Inconsistent `<=` vs `<` with the training convention.
* Losing the right-branch condition (it should read "> t").
* Mutating the tree while traversing.

## Why this matters
Rule-style explanations are what many regulated domains (credit, healthcare) expect; trees are also
used as global surrogates ([[surrogate-fidelity]]).
''',
"statement": r'''
Write `predict_with_path(tree, x, feature_names)` returning `(value, path)` where `path` is a list of
strings `"<name> <= <t>"` or `"<name> > <t>"` (threshold formatted with `str(t)`). Raise `ValueError`
if a node is malformed (neither a leaf nor a valid internal node).

**Example**
```python
tree = {"feature": 0, "threshold": 30, "left": {"feature": 1, "threshold": 5,
        "left": {"value": "approve"}, "right": {"value": "reject"}}, "right": {"value": "approve"}}
predict_with_path(tree, [25, 8], ["income", "debt"])
# ('reject', ['income <= 30', 'debt > 5'])
```
''',
"starter": r'''
def predict_with_path(tree, x, feature_names):
    return None, []
''',
"hints": [
    "Loop `while 'value' not in node`.",
    "Compare `x[node['feature']] <= node['threshold']`.",
    "Append `f\"{name} <= {t}\"` or `f\"{name} > {t}\"` then move to the child.",
],
"solution": r'''
def predict_with_path(tree, x, feature_names):
    node, path = tree, []
    while "value" not in node:
        if not all(k in node for k in ("feature", "threshold", "left", "right")):
            raise ValueError("malformed node")
        j, t = node["feature"], node["threshold"]
        name = feature_names[j]
        if x[j] <= t:
            path.append(f"{name} <= {t}")
            node = node["left"]
        else:
            path.append(f"{name} > {t}")
            node = node["right"]
    return node["value"], path
''',
"explanation": r'''
The loop walks from the root to a leaf, recording the condition satisfied at each internal node
using the same `<=` convention as training. The leaf's value is the prediction.
''',
"tests": r'''
TREE = {"feature": 0, "threshold": 30, "left": {"feature": 1, "threshold": 5,
        "left": {"value": "approve"}, "right": {"value": "reject"}}, "right": {"value": "approve"}}
NAMES = ["income", "debt"]

class TestPath(unittest.TestCase):
    def test_reject(self):
        self.assertEqual(S.predict_with_path(TREE, [25, 8], NAMES), ("reject", ["income <= 30", "debt > 5"]))

    def test_right_branch(self):
        self.assertEqual(S.predict_with_path(TREE, [31, 100], NAMES), ("approve", ["income > 30"]))

    def test_boundary_left(self):
        self.assertEqual(S.predict_with_path(TREE, [30, 5], NAMES)[1], ["income <= 30", "debt <= 5"])

    def test_leaf_root(self):
        self.assertEqual(S.predict_with_path({"value": 1.5}, [0], ["a"]), (1.5, []))

    def test_float_threshold(self):
        t = {"feature": 0, "threshold": 2.5, "left": {"value": 0}, "right": {"value": 1}}
        self.assertEqual(S.predict_with_path(t, [3.0], ["x"]), (1, ["x > 2.5"]))

    def test_malformed(self):
        with self.assertRaises(ValueError):
            S.predict_with_path({"feature": 0, "left": {"value": 1}}, [0], ["a"])

    def test_tree_unchanged(self):
        import copy
        t = copy.deepcopy(TREE)
        S.predict_with_path(t, [25, 1], NAMES)
        self.assertEqual(t, TREE)
''',
"feedback": [
    ("test_boundary_left", "Go left when x_j <= threshold (inclusive)."),
    ("test_right_branch", "Right-branch conditions read 'name > t'."),
    ("test_malformed", "Raise ValueError when a node lacks feature/threshold/left/right and isn't a leaf."),
    ("test_leaf_root", "A tree that is just a leaf has an empty path."),
],
},
# ---------------------------------------------------------------- ice-curve
{
"slug": "ice-curve", "title": "Individual Conditional Expectation",
"difficulty": "beginner", "prereqs": ["linear-contributions"], "packages": ["numpy"],
"objectives": ["Vary one feature of one instance over a grid", "Query a black-box model in batch",
               "Read local effects from an ICE curve"],
"tags": ["ice", "model-agnostic", "what-if", "local-explanation"],
"sources": ["S024"], "entry": "ice_curve(predict, x, feature, grid)",
"article": r'''
# Individual Conditional Expectation (ICE)

## Intuition
"What would the model predict for *this* person if only their age changed?" Keep everything else
fixed, sweep one feature over a range, and plot the prediction. That curve is an ICE curve.

## Precise explanation
For a model `predict(X) -> (n,)`, an instance $x$, feature $j$ and grid values $g_1..g_m$:
build $m$ copies of $x$, set column $j$ to $g_k$ in copy $k$, and predict all copies in **one batch**.
Black-box: only predictions are needed, not model internals (**model-agnostic**). Caveat: if
features are correlated, some grid points create unrealistic inputs (e.g. 5 rooms in a 20 m² flat).

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="150" viewBox="0 0 260 150" role="img" aria-label="Three ICE curves for three instances, one rising, one flat and one rising then falling">
<title>ICE curves</title>
<line x1="25" y1="130" x2="250" y2="130" stroke="#999"/><line x1="25" y1="130" x2="25" y2="10" stroke="#999"/>
<polyline points="30,110 80,95 130,70 180,50 230,30" fill="none" stroke="#1f77b4" stroke-width="2"/>
<polyline points="30,80 80,80 130,79 180,80 230,80" fill="none" stroke="#2ca02c" stroke-width="2"/>
<polyline points="30,120 80,90 130,60 180,85 230,110" fill="none" stroke="#d62728" stroke-width="2"/>
<text x="120" y="146" font-size="11">feature value</text>
</svg>

*Figure (original): each line is one instance; different shapes reveal interactions that an average
(PDP, [[partial-dependence]]) would hide.*

## Worked example
predict(X) = X[:,0]·X[:,1]; x = [2, 3]; vary feature 0 over [0, 1, 2] → [0, 3, 6]
(slope = 3 = this instance's x₁ value).

## Common mistakes
* Modifying the original instance in place.
* Calling the model once per grid point in a Python loop (slow for real models).
* Interpreting ICE as causal effects in the real world.

## Why this matters
ICE curves are the building block of partial dependence ([[partial-dependence]]) and a practical "what-if" tool.
''',
"statement": r'''
Write `ice_curve(predict, x, feature, grid)` returning a NumPy array of predictions, one per grid
value, computed with a **single** call to `predict` on an `(len(grid), d)` matrix. `x` must not be
modified. Raise `ValueError` if `feature` is out of range or `grid` is empty.

**Example**
```python
predict = lambda X: X[:, 0] * X[:, 1]
ice_curve(predict, np.array([2., 3.]), 0, [0, 1, 2])   # [0., 3., 6.]
```
''',
"starter": r'''
import numpy as np


def ice_curve(predict, x, feature, grid):
    pass
''',
"hints": [
    "`X = np.tile(x, (len(grid), 1))`.",
    "`X[:, feature] = grid`.",
    "`return np.asarray(predict(X), dtype=float)`.",
],
"solution": r'''
import numpy as np


def ice_curve(predict, x, feature, grid):
    x = np.asarray(x, dtype=float)
    grid = np.asarray(grid, dtype=float)
    if grid.size == 0:
        raise ValueError("grid must be non-empty")
    if not 0 <= feature < x.shape[0]:
        raise ValueError("feature index out of range")
    X = np.tile(x, (grid.size, 1))
    X[:, feature] = grid
    return np.asarray(predict(X), dtype=float)
''',
"explanation": r'''
Tiling creates independent copies of the instance, one per grid value, so the original stays intact.
Overwriting a single column and predicting the whole matrix gives the ICE curve in one model call.
''',
"tests": r'''
import numpy as np

class TestICE(unittest.TestCase):
    def test_example(self):
        f = lambda X: X[:, 0] * X[:, 1]
        np.testing.assert_allclose(S.ice_curve(f, np.array([2., 3.]), 0, [0, 1, 2]), [0, 3, 6])

    def test_single_call(self):
        calls = []
        def f(X):
            calls.append(X.shape); return X.sum(axis=1)
        S.ice_curve(f, np.array([1., 2., 3.]), 2, [0, 5, 10, 15])
        self.assertEqual(calls, [(4, 3)])

    def test_no_mutation(self):
        x = np.array([1., 2.])
        S.ice_curve(lambda X: X[:, 0], x, 0, [9, 9])
        np.testing.assert_array_equal(x, [1., 2.])

    def test_other_features_fixed(self):
        seen = {}
        def f(X):
            seen["X"] = X.copy(); return X[:, 0]
        S.ice_curve(f, np.array([7., 8., 9.]), 1, [0, 1])
        np.testing.assert_array_equal(seen["X"][:, [0, 2]], [[7, 9], [7, 9]])

    def test_flat_for_unused_feature(self):
        r = S.ice_curve(lambda X: 2 * X[:, 0], np.array([1., 1.]), 1, np.linspace(-5, 5, 11))
        np.testing.assert_allclose(r, 2.0)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.ice_curve(lambda X: X[:, 0], np.array([1.]), 3, [1])
        with self.assertRaises(ValueError):
            S.ice_curve(lambda X: X[:, 0], np.array([1.]), 0, [])
''',
"feedback": [
    ("test_single_call", "Build one (len(grid), d) matrix and call predict once."),
    ("test_no_mutation", "Tile copies of x; never write into x."),
    ("test_other_features_fixed", "Only the chosen column changes."),
    ("test_errors", "Validate the feature index and non-empty grid."),
],
},
# ---------------------------------------------------------------- partial-dependence
{
"slug": "partial-dependence", "title": "Partial Dependence by Hand", "optional": True,
"difficulty": "intermediate", "prereqs": ["ice-curve"], "packages": ["numpy"],
"objectives": ["Average ICE curves over a dataset to get partial dependence",
               "Centre curves at the first grid point", "Detect interactions via ICE spread"],
"tags": ["pdp", "partial-dependence", "global-explanation", "model-agnostic"],
"sources": ["S024", "S012"], "entry": "partial_dependence(predict, X, feature, grid); ice_spread(predict, X, feature, grid)",
"article": r'''
# Partial Dependence Plots

## Intuition
An ICE curve shows one instance; the **partial dependence** (PD) curve averages ICE curves over the
whole dataset — the model's average response to a feature, marginalising the others.

## Precise explanation
$$\text{PD}_j(g) = \frac1n\sum_{i=1}^{n} f(x_i \text{ with } x_{ij} := g).$$
Vectorised: for each grid value, set column j of a copy of X to g and average predictions (or build
one big `(m·n, d)` batch). **Centred** PD subtracts the value at the first grid point, so curves start
at 0. If ICE curves have very different shapes (large spread after centring), the feature
**interacts** with others and the PD average hides it.
scikit-learn's `inspection.partial_dependence` implements the same estimator.

## Worked example
f(X) = X₀·X₁, data X₁ ∈ {−1, +1} (mean 0): every ICE curve has slope ±1, the PD curve is flat (0) —
a pure interaction that PD alone would misread as "no effect".

## Common mistakes
* Averaging features instead of predictions.
* Extrapolating the grid far outside the data.
* Reading PD causally.

## Why this matters
PD plots are the most common global explanation for tabular models.
''',
"statement": r'''
Implement:
* `partial_dependence(predict, X, feature, grid)` → array of average predictions per grid value.
* `ice_spread(predict, X, feature, grid)` → float: the mean over grid points of the standard deviation
  (population) across instances of **centred** ICE curves (each curve minus its value at `grid[0]`).
Raise `ValueError` for empty `X`/`grid` or an invalid feature.

**Example**
```python
f = lambda X: X[:, 0] * X[:, 1]
X = np.array([[0., -1.], [0., 1.]])
partial_dependence(f, X, 0, [0, 1, 2])   # [0., 0., 0.]
ice_spread(f, X, 0, [0, 1, 2])           # 1.0  (curves 0,-1,-2 and 0,1,2)
```
''',
"starter": r'''
import numpy as np


def partial_dependence(predict, X, feature, grid):
    pass


def ice_spread(predict, X, feature, grid):
    pass
''',
"hints": [
    "Write `_ice_matrix` returning shape `(n, m)`: for each grid value g, copy X, set column, predict.",
    "PD = `ice.mean(axis=0)`.",
    "Centred: `ice - ice[:, [0]]`; spread = `centred.std(axis=0).mean()`.",
],
"solution": r'''
import numpy as np


def _ice_matrix(predict, X, feature, grid):
    X = np.asarray(X, dtype=float)
    grid = np.asarray(grid, dtype=float)
    if X.ndim != 2 or X.shape[0] == 0 or grid.size == 0:
        raise ValueError("X and grid must be non-empty")
    if not 0 <= feature < X.shape[1]:
        raise ValueError("feature index out of range")
    cols = []
    for g in grid:
        Xg = X.copy()
        Xg[:, feature] = g
        cols.append(np.asarray(predict(Xg), dtype=float))
    return np.column_stack(cols)


def partial_dependence(predict, X, feature, grid):
    return _ice_matrix(predict, X, feature, grid).mean(axis=0)


def ice_spread(predict, X, feature, grid):
    ice = _ice_matrix(predict, X, feature, grid)
    centred = ice - ice[:, [0]]
    return float(centred.std(axis=0).mean())
''',
"explanation": r'''
The helper builds the full ICE matrix (instances × grid values). Averaging over instances gives PD;
centring each ICE curve and measuring the spread across instances quantifies heterogeneity that
signals interactions.
''',
"tests": r'''
import numpy as np

F = lambda X: X[:, 0] * X[:, 1]

class TestPDP(unittest.TestCase):
    def test_interaction_flat(self):
        X = np.array([[0., -1.], [0., 1.]])
        np.testing.assert_allclose(S.partial_dependence(F, X, 0, [0, 1, 2]), 0)

    def test_spread(self):
        X = np.array([[0., -1.], [0., 1.]])
        self.assertAlmostEqual(S.ice_spread(F, X, 0, [0, 1, 2]), 1.0)

    def test_additive_no_spread(self):
        g = lambda X: 3 * X[:, 0] + X[:, 1] ** 2
        X = np.random.default_rng(0).normal(size=(20, 2))
        self.assertAlmostEqual(S.ice_spread(g, X, 0, np.linspace(-1, 1, 5)), 0.0)

    def test_linear_pd(self):
        g = lambda X: 2 * X[:, 0] + X[:, 1]
        X = np.array([[5., 1.], [6., 3.]])
        np.testing.assert_allclose(S.partial_dependence(g, X, 0, [0, 1]), [2, 4])

    def test_matches_ice_average(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(7, 3)); grid = [-1, 0, 2]
        h = lambda X: np.tanh(X[:, 0] * X[:, 2]) + X[:, 1]
        exp = []
        for gv in grid:
            Xg = X.copy(); Xg[:, 2] = gv; exp.append(h(Xg).mean())
        np.testing.assert_allclose(S.partial_dependence(h, X, 2, grid), exp)

    def test_no_mutation(self):
        X = np.array([[1., 2.]])
        S.partial_dependence(F, X, 1, [7, 8])
        np.testing.assert_array_equal(X, [[1., 2.]])

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.partial_dependence(F, np.zeros((0, 2)), 0, [1])
''',
"feedback": [
    ("test_interaction_flat", "PD averages predictions over instances with the feature fixed at each grid value."),
    ("test_spread", "Centre each ICE curve at grid[0], then take the std across instances and average over the grid."),
    ("test_additive_no_spread", "Additive effects give parallel ICE curves, hence zero spread."),
    ("test_no_mutation", "Copy X before overwriting the feature column."),
],
},
# ---------------------------------------------------------------- permutation-importance
{
"slug": "permutation-importance", "title": "Permutation Feature Importance by Hand", "optional": True,
"difficulty": "intermediate", "prereqs": ["partial-dependence", "sklearn-estimator-api"], "packages": ["numpy"],
"objectives": ["Measure importance as the score drop after permuting a feature",
               "Repeat permutations with a seeded generator and report mean/std", "Interpret near-zero and negative importances"],
"tags": ["permutation-importance", "global-explanation", "model-agnostic"],
"sources": ["S024", "S012"], "entry": "permutation_importance(predict, X, y, score, n_repeats=5, seed=0)",
"article": r'''
# Permutation Feature Importance

## Intuition
If shuffling a feature's column (destroying its relationship with the target) makes the model much
worse, the model relied on that feature. If nothing changes, the feature didn't matter *to this
model*.

## Precise explanation
1. Baseline score $s_0 = \text{score}(y, f(X))$ (higher = better, e.g. R² or accuracy).
2. For each feature $j$ and repeat $r$: permute column j (rows shuffled with
   `rng.permutation(n)`), compute $s_{j,r}$.
3. Importance $I_j = s_0 - \text{mean}_r\, s_{j,r}$, with standard deviation across repeats.
Use **one** generator `default_rng(seed)`, iterating features in order and repeats inside.
Small negative values mean "no importance" (noise). Correlated features share importance — permuting
one can be compensated by the other. Computing on held-out data measures importance for
*generalisation*.

## Worked example
y = 3x₀ + noise, x₁ pure noise, linear model: permuting x₀ drops R² from ≈1 to ≈−1; permuting x₁ ≈ 0.

## Common mistakes
* Re-fitting the model after permuting (that is drop-column importance, a different method).
* Permuting all features at once.
* Reporting a single permutation without variability.

## Why this matters
Model-agnostic, cheap and widely used (scikit-learn `permutation_importance`); it also connects to the
permutation test idea from [[permutation-test]].
''',
"statement": r'''
Write `permutation_importance(predict, X, y, score, n_repeats=5, seed=0)` returning a dict
`{"baseline": float, "mean": array(d), "std": array(d)}` following the recipe above (`score(y_true,
y_pred)` returns a float; `X` must not be modified). Raise `ValueError` if `n_repeats < 1`.

**Example**
```python
r = permutation_importance(lambda X: 3 * X[:, 0], X, y, r2_score, n_repeats=5, seed=0)
r["mean"][0] > 1.0 and abs(r["mean"][1]) < 1e-12    # True (model ignores feature 1)
```
''',
"starter": r'''
import numpy as np


def permutation_importance(predict, X, y, score, n_repeats=5, seed=0):
    pass
''',
"hints": [
    "`base = score(y, predict(X))`; `rng = np.random.default_rng(seed)`.",
    "For each j, r: `Xp = X.copy(); Xp[:, j] = X[rng.permutation(n), j]`.",
    "Collect drops `base - score(y, predict(Xp))`; take mean and std per feature.",
],
"solution": r'''
import numpy as np


def permutation_importance(predict, X, y, score, n_repeats=5, seed=0):
    if n_repeats < 1:
        raise ValueError("n_repeats must be >= 1")
    X = np.asarray(X, dtype=float)
    n, d = X.shape
    base = float(score(y, predict(X)))
    rng = np.random.default_rng(seed)
    drops = np.zeros((d, n_repeats))
    for j in range(d):
        for r in range(n_repeats):
            Xp = X.copy()
            Xp[:, j] = X[rng.permutation(n), j]
            drops[j, r] = base - float(score(y, predict(Xp)))
    return {"baseline": base, "mean": drops.mean(axis=1), "std": drops.std(axis=1)}
''',
"explanation": r'''
The baseline score is computed once. Each feature is permuted on a fresh copy of X, which breaks
its link with y while keeping its marginal distribution; the average drop in score across repeats is
the importance and the spread shows its uncertainty.
''',
"tests": r'''
import numpy as np

def r2(y, p):
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()

rng0 = np.random.default_rng(42)
X = rng0.normal(size=(200, 2))
Y = 3 * X[:, 0] + rng0.normal(0, 0.1, 200)
MODEL = lambda X: 3 * X[:, 0]

class TestPermImp(unittest.TestCase):
    def test_relevant_vs_irrelevant(self):
        r = S.permutation_importance(MODEL, X, Y, r2, n_repeats=5, seed=0)
        self.assertGreater(r["mean"][0], 1.0)
        self.assertAlmostEqual(r["mean"][1], 0.0, places=12)

    def test_baseline(self):
        r = S.permutation_importance(MODEL, X, Y, r2)
        self.assertAlmostEqual(r["baseline"], r2(Y, MODEL(X)))

    def test_recipe(self):
        r = S.permutation_importance(MODEL, X, Y, r2, n_repeats=2, seed=3)
        rng = np.random.default_rng(3)
        base = r2(Y, MODEL(X)); drops = []
        for j in range(2):
            for _ in range(2):
                Xp = X.copy(); Xp[:, j] = X[rng.permutation(200), j]; drops.append(base - r2(Y, MODEL(Xp)))
        np.testing.assert_allclose(r["mean"], [np.mean(drops[:2]), np.mean(drops[2:])])

    def test_std_shape(self):
        r = S.permutation_importance(MODEL, X, Y, r2, n_repeats=4)
        self.assertEqual(r["std"].shape, (2,))
        self.assertEqual(r["std"][1], 0.0)

    def test_no_mutation(self):
        Xc = X.copy()
        S.permutation_importance(MODEL, Xc, Y, r2, n_repeats=1)
        np.testing.assert_array_equal(Xc, X)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.permutation_importance(MODEL, X, Y, r2, n_repeats=0)
''',
"feedback": [
    ("test_recipe", "One default_rng(seed); loop features outer, repeats inner; permute rows of column j only."),
    ("test_relevant_vs_irrelevant", "Importance = baseline score − permuted score (don't refit)."),
    ("test_no_mutation", "Permute a copy of X, not X itself."),
    ("test_std_shape", "Return mean and std arrays with one entry per feature."),
],
},
# ---------------------------------------------------------------- occlusion-saliency
{
"slug": "occlusion-saliency", "title": "Occlusion Saliency Map",
"difficulty": "intermediate", "prereqs": ["cv-pooling-torch", "ice-curve"], "packages": ["numpy"],
"objectives": ["Occlude image patches with a baseline value", "Measure the drop in class score per patch",
               "Build a saliency heat-map at patch resolution"],
"tags": ["saliency", "occlusion", "image-explanations", "perturbation"],
"sources": ["S024", "S015"], "entry": "occlusion_map(score_fn, img, patch=2, baseline=0.0)",
"article": r'''
# Occlusion Saliency

## Intuition
Cover part of an image with a grey square. If the classifier's confidence in "dog" drops sharply, that
region mattered. Slide the square over the whole image to build a heat-map of importance.

## Precise explanation
For a scoring function `score_fn(img) -> float` (e.g. the logit of the predicted class):
1. Reference score $s = \text{score}(I)$.
2. For each non-overlapping patch (top-left corners on a grid with step `patch`; edge patches may be
   smaller), set its pixels to `baseline` and compute $s_{p}$.
3. Saliency of the patch = $s - s_p$ (positive = the patch supported the score).
Output shape: `(ceil(H/patch), ceil(W/patch))`. This is a **perturbation** method: model-agnostic but
needs one forward pass per patch. The baseline (black, grey, blurred) changes the answer.

## Worked example
score = sum of the top-left 2×2 region of a 4×4 image of ones, patch 2: occluding the top-left patch
drops the score from 4 to 0 → saliency 4; other patches → 0.

## Common mistakes
* Occluding the original array in place (corrupts later patches).
* Forgetting partial patches at the right/bottom edges.
* Interpreting saliency as "what the model sees" — it measures sensitivity to this particular
  perturbation.

## Why this matters
Occlusion maps (and gradient saliency) are common sanity checks for vision models, e.g. revealing
models that rely on watermarks or backgrounds.
''',
"statement": r'''
Write `occlusion_map(score_fn, img, patch=2, baseline=0.0)` for a 2-D image returning a float array
of shape `(ceil(H/patch), ceil(W/patch))` as described. `img` must not change. Raise `ValueError`
if `patch < 1`.

**Example**
```python
score = lambda im: float(im[:2, :2].sum())
occlusion_map(score, np.ones((4, 4)), patch=2)   # [[4., 0.], [0., 0.]]
```
''',
"starter": r'''
import numpy as np


def occlusion_map(score_fn, img, patch=2, baseline=0.0):
    pass
''',
"hints": [
    "`Hp = -(-H // patch)` is ceil division.",
    "For each (pi, pj): `occ = img.copy(); occ[pi*patch:(pi+1)*patch, pj*patch:(pj+1)*patch] = baseline`.",
    "`sal[pi, pj] = base - score_fn(occ)`.",
],
"solution": r'''
import numpy as np


def occlusion_map(score_fn, img, patch=2, baseline=0.0):
    if patch < 1:
        raise ValueError("patch must be >= 1")
    img = np.asarray(img, dtype=float)
    H, W = img.shape
    Hp, Wp = -(-H // patch), -(-W // patch)
    base = float(score_fn(img))
    sal = np.zeros((Hp, Wp))
    for pi in range(Hp):
        for pj in range(Wp):
            occ = img.copy()
            occ[pi * patch:(pi + 1) * patch, pj * patch:(pj + 1) * patch] = baseline
            sal[pi, pj] = base - float(score_fn(occ))
    return sal
''',
"explanation": r'''
Each patch is occluded on a fresh copy; slicing past the edge automatically gives smaller edge
patches. The saliency is the score drop relative to the unoccluded image.
''',
"tests": r'''
import numpy as np

class TestOcclusion(unittest.TestCase):
    def test_example(self):
        score = lambda im: float(im[:2, :2].sum())
        np.testing.assert_allclose(S.occlusion_map(score, np.ones((4, 4)), 2), [[4, 0], [0, 0]])

    def test_edge_patches(self):
        out = S.occlusion_map(lambda im: float(im.sum()), np.ones((5, 3)), 2)
        self.assertEqual(out.shape, (3, 2))
        np.testing.assert_allclose(out, [[4, 2], [4, 2], [2, 1]])

    def test_linear_model(self):
        rng = np.random.default_rng(0)
        Wt, img = rng.normal(size=(4, 4)), rng.normal(size=(4, 4))
        out = S.occlusion_map(lambda im: float((Wt * im).sum()), img, 1)
        np.testing.assert_allclose(out, Wt * img)

    def test_baseline_value(self):
        out = S.occlusion_map(lambda im: float(im.sum()), np.full((2, 2), 3.0), 2, baseline=1.0)
        np.testing.assert_allclose(out, [[8.0]])

    def test_no_mutation(self):
        img = np.ones((2, 2))
        S.occlusion_map(lambda im: float(im.sum()), img, 1)
        np.testing.assert_array_equal(img, np.ones((2, 2)))

    def test_irrelevant_region_zero(self):
        out = S.occlusion_map(lambda im: float(im[0, 0]), np.arange(16.).reshape(4, 4) + 1, 2)
        self.assertEqual(out[1, 1], 0.0)

    def test_bad_patch(self):
        with self.assertRaises(ValueError):
            S.occlusion_map(lambda im: 0.0, np.ones((2, 2)), 0)
''',
"feedback": [
    ("test_edge_patches", "Use ceil division for the map shape; edge patches are smaller."),
    ("test_linear_model", "Saliency = original score − occluded score."),
    ("test_no_mutation", "Occlude a copy of the image for every patch."),
    ("test_baseline_value", "Fill occluded pixels with the baseline value."),
],
},
# ---------------------------------------------------------------- surrogate-fidelity
{
"slug": "surrogate-fidelity", "title": "Global Surrogate and Fidelity",
"difficulty": "intermediate", "prereqs": ["xai-permutation-importance", "least-squares-line"], "packages": ["numpy"],
"objectives": ["Fit an interpretable model to a black box's predictions", "Measure fidelity with R² against the black box",
               "Recognise when a surrogate explanation cannot be trusted"],
"tags": ["global-surrogate", "fidelity", "model-agnostic", "interpretable-models"],
"sources": ["S024"], "entry": "fit_linear_surrogate(predict, X); fidelity_r2(predict, surrogate, X)",
"article": r'''
# Global Surrogate Models

## Intuition
Train a simple, readable model (linear or a small tree) to *imitate the black box*. If the imitation
is faithful, its structure explains the black box; if not, the explanation is fiction.

## Precise explanation
1. Query the black box: $\hat y = f(X)$ on representative data.
2. Fit the surrogate $g$ to $(X, \hat y)$ — note: the **black-box predictions**, not the true labels.
3. **Fidelity:** $R^2(\hat y, g(X))$ — how much of the black box's behaviour the surrogate captures.
Only interpret a surrogate with high fidelity (and check fidelity on held-out data). Fidelity says
nothing about whether the black box is *correct* — only whether the surrogate copies it.

Linear surrogate: least squares on $[1, X]$ ([[linalg-solve]]).

## Worked example
Black box $f(x) = 2x_0 - x_1 + 3$: linear surrogate recovers intercept 3, weights [2, −1], fidelity 1.
Black box $f(x) = x_0^2$ on symmetric data: best line is flat, fidelity ≈ 0 → do not trust it.

## Common mistakes
* Fitting the surrogate to true labels (that just trains another model).
* Reporting the surrogate's accuracy on the task as "fidelity".
* Interpreting a low-fidelity surrogate.

## Why this matters
Surrogates are a practical way to summarise complex models, and the fidelity check is a habit every
explanation method deserves.
''',
"statement": r'''
Implement:
* `fit_linear_surrogate(predict, X)` → `(intercept, coef)` from least squares of `predict(X)` on
  `[1, X]` (`np.linalg.lstsq`, `rcond=None`).
* `fidelity_r2(predict, surrogate, X)` → R² of `surrogate(X)` against `predict(X)`; if the black box
  is constant on X, return 1.0 when the surrogate matches it exactly (within 1e-12) else 0.0.

**Example**
```python
f = lambda X: 2 * X[:, 0] - X[:, 1] + 3
b, w = fit_linear_surrogate(f, X)     # (3.0, [2., -1.])
fidelity_r2(f, lambda X: b + X @ w, X)  # 1.0
```
''',
"starter": r'''
import numpy as np


def fit_linear_surrogate(predict, X):
    pass


def fidelity_r2(predict, surrogate, X):
    pass
''',
"hints": [
    "`yhat = predict(X)`; `A = np.column_stack([np.ones(len(X)), X])`.",
    "`w, *_ = np.linalg.lstsq(A, yhat, rcond=None)`; return `w[0], w[1:]`.",
    "R² = 1 − Σ(yhat − s)² / Σ(yhat − mean)²; handle zero denominator.",
],
"solution": r'''
import numpy as np


def fit_linear_surrogate(predict, X):
    X = np.asarray(X, dtype=float)
    yhat = np.asarray(predict(X), dtype=float)
    A = np.column_stack([np.ones(len(X)), X])
    w, *_ = np.linalg.lstsq(A, yhat, rcond=None)
    return float(w[0]), w[1:]


def fidelity_r2(predict, surrogate, X):
    X = np.asarray(X, dtype=float)
    yhat = np.asarray(predict(X), dtype=float)
    s = np.asarray(surrogate(X), dtype=float)
    ss_res = float(((yhat - s) ** 2).sum())
    ss_tot = float(((yhat - yhat.mean()) ** 2).sum())
    if ss_tot == 0:
        return 1.0 if ss_res <= 1e-12 else 0.0
    return 1.0 - ss_res / ss_tot
''',
"explanation": r'''
The surrogate is fitted to the black box's own outputs, so it learns to imitate the model rather than
the data. Fidelity is R² between the two models' predictions, with an explicit rule for a constant
black box.
''',
"tests": r'''
import numpy as np

X = np.random.default_rng(0).normal(size=(100, 2))

class TestSurrogate(unittest.TestCase):
    def test_linear_recovered(self):
        f = lambda X: 2 * X[:, 0] - X[:, 1] + 3
        b, w = S.fit_linear_surrogate(f, X)
        self.assertAlmostEqual(b, 3.0)
        np.testing.assert_allclose(w, [2, -1], atol=1e-10)
        self.assertAlmostEqual(S.fidelity_r2(f, lambda X: b + X @ w, X), 1.0)

    def test_nonlinear_low_fidelity(self):
        f = lambda X: X[:, 0] ** 2
        Xs = np.column_stack([np.linspace(-2, 2, 101), np.zeros(101)])
        b, w = S.fit_linear_surrogate(f, Xs)
        self.assertLess(S.fidelity_r2(f, lambda Z: b + Z @ w, Xs), 0.05)

    def test_fits_predictions_not_labels(self):
        f = lambda X: 5 * X[:, 1]
        _, w = S.fit_linear_surrogate(f, X)
        np.testing.assert_allclose(w, [0, 5], atol=1e-10)

    def test_partial_fidelity(self):
        f = lambda X: X[:, 0] + np.sin(3 * X[:, 1])
        b, w = S.fit_linear_surrogate(f, X)
        r = S.fidelity_r2(f, lambda Z: b + Z @ w, X)
        self.assertTrue(0.3 < r < 0.95)

    def test_constant_blackbox(self):
        f = lambda X: np.full(len(X), 4.0)
        self.assertEqual(S.fidelity_r2(f, lambda Z: np.full(len(Z), 4.0), X), 1.0)
        self.assertEqual(S.fidelity_r2(f, lambda Z: np.zeros(len(Z)), X), 0.0)

    def test_bad_surrogate_negative(self):
        f = lambda X: X[:, 0]
        self.assertLess(S.fidelity_r2(f, lambda Z: -Z[:, 0], X), 0)
''',
"feedback": [
    ("test_fits_predictions_not_labels", "Fit the surrogate to predict(X), the black box's outputs."),
    ("test_linear_recovered", "Include an intercept column of ones in the least-squares design."),
    ("test_nonlinear_low_fidelity", "Fidelity is R² between black-box and surrogate predictions."),
    ("test_constant_blackbox", "Handle zero variance of the black-box predictions explicitly."),
],
},
# ---------------------------------------------------------------- exact-shapley
{
"slug": "exact-shapley", "title": "Exact Shapley Values",
"difficulty": "advanced", "prereqs": ["binomial-coefficient", "linear-contributions"], "packages": ["numpy"],
"objectives": ["Define a coalition value function with a baseline", "Compute exact Shapley values by enumerating subsets",
               "Verify efficiency, symmetry and dummy properties"],
"tags": ["shapley-values", "shap", "game-theory", "feature-attribution"],
"sources": ["S026", "S024"], "entry": "coalition_value(predict, x, baseline, subset); shapley_values(predict, x, baseline)",
"article": r'''
# Shapley Values

## Intuition
Features are players in a cooperative game whose payout is the prediction. A fair split gives each
player their average marginal contribution over every order in which players could join.

## Precise explanation
Value of a coalition $S$ (baseline/interventional version): evaluate the model on an input that takes
$x_j$ for $j\in S$ and the baseline $x'_j$ otherwise: $v(S) = f(x_S, x'_{\bar S})$.
Shapley value of feature $j$ among $d$ features:
$$\phi_j = \sum_{S\subseteq N\setminus\{j\}} \frac{|S|!\,(d-|S|-1)!}{d!}\,\big[v(S\cup\{j\}) - v(S)\big].$$
Properties (Lundberg & Lee 2017; Molnar ch. "Shapley values"):
* **Efficiency:** $\sum_j\phi_j = f(x) - f(x')$.
* **Symmetry:** interchangeable features get equal values.
* **Dummy:** a feature that never changes $v$ gets 0.
For a linear model, $\phi_j = w_j(x_j - x'_j)$ ([[linear-contributions]]). Exact computation needs $2^d$ model calls —
feasible only for small d; SHAP approximates it for larger models.

## Worked example
f(x) = x₀·x₁, x = (1, 1), baseline (0, 0): v(∅) = 0, v({0}) = 0, v({1}) = 0, v({0,1}) = 1 →
φ₀ = ½(0 − 0) + ½(1 − 0) = 0.5, φ₁ = 0.5. The interaction is split equally.

## Common mistakes
* Wrong weights (use $|S|!(d-|S|-1)!/d!$).
* Forgetting the empty coalition.
* Different baselines give different (both valid) explanations — report which you used.

## Why this matters
SHAP is one of the most widely used explanation tools; implementing the exact formula shows what the
approximations approximate.
''',
"statement": r'''
Implement (use `itertools.combinations` and `math.factorial`):
* `coalition_value(predict, x, baseline, subset)` → float `predict` on a single input (shape `(1, d)`)
  that takes `x` on indices in `subset` and `baseline` elsewhere.
* `shapley_values(predict, x, baseline)` → array of exact Shapley values. Raise `ValueError` if
  `d > 12` (too many coalitions) or shapes differ.

**Example**
```python
f = lambda X: X[:, 0] * X[:, 1]
shapley_values(f, np.array([1., 1.]), np.zeros(2))   # [0.5, 0.5]
```
''',
"starter": r'''
import math
from itertools import combinations

import numpy as np


def coalition_value(predict, x, baseline, subset):
    pass


def shapley_values(predict, x, baseline):
    pass
''',
"hints": [
    "`z = baseline.copy(); z[list(subset)] = x[list(subset)]`; `float(predict(z[None, :])[0])`.",
    "Loop j; for size in 0..d−1 and each `S` in `combinations(others, size)`.",
    "Weight = `math.factorial(len(S)) * math.factorial(d - len(S) - 1) / math.factorial(d)`.",
],
"solution": r'''
import math
from itertools import combinations

import numpy as np


def coalition_value(predict, x, baseline, subset):
    x = np.asarray(x, dtype=float)
    z = np.asarray(baseline, dtype=float).copy()
    idx = list(subset)
    z[idx] = x[idx]
    return float(np.asarray(predict(z[None, :]))[0])


def shapley_values(predict, x, baseline):
    x = np.asarray(x, dtype=float)
    baseline = np.asarray(baseline, dtype=float)
    if x.shape != baseline.shape:
        raise ValueError("x and baseline must have the same shape")
    d = x.shape[0]
    if d > 12:
        raise ValueError("exact Shapley values are limited to d <= 12")
    cache = {}

    def v(S):
        key = tuple(sorted(S))
        if key not in cache:
            cache[key] = coalition_value(predict, x, baseline, key)
        return cache[key]

    phi = np.zeros(d)
    for j in range(d):
        others = [i for i in range(d) if i != j]
        for size in range(d):
            w = math.factorial(size) * math.factorial(d - size - 1) / math.factorial(d)
            for S in combinations(others, size):
                phi[j] += w * (v(S + (j,)) - v(S))
    return phi
''',
"explanation": r'''
The value function mixes the instance and the baseline according to the coalition. For each feature,
every coalition of the other features is enumerated and its weighted marginal contribution added.
A cache ensures each of the 2^d coalitions is evaluated only once.
''',
"tests": r'''
import numpy as np

class TestShapley(unittest.TestCase):
    def test_interaction_split(self):
        np.testing.assert_allclose(S.shapley_values(lambda X: X[:, 0] * X[:, 1], np.array([1., 1.]), np.zeros(2)), [0.5, 0.5])

    def test_linear_matches_xa01(self):
        w = np.array([2., -1., 0.5]); x = np.array([3., 4., -2.]); base = np.array([1., 1., 1.])
        np.testing.assert_allclose(S.shapley_values(lambda X: X @ w + 7, x, base), w * (x - base))

    def test_efficiency(self):
        f = lambda X: np.tanh(X[:, 0] * X[:, 1]) + X[:, 2] ** 2 - X[:, 0] * X[:, 3]
        rng = np.random.default_rng(0)
        x, base = rng.normal(size=4), rng.normal(size=4)
        phi = S.shapley_values(f, x, base)
        self.assertAlmostEqual(phi.sum(), f(x[None])[0] - f(base[None])[0])

    def test_dummy(self):
        phi = S.shapley_values(lambda X: X[:, 0] ** 3, np.array([2., 5., 7.]), np.zeros(3))
        np.testing.assert_allclose(phi[1:], 0.0)

    def test_symmetry(self):
        phi = S.shapley_values(lambda X: X[:, 0] + X[:, 1] + X[:, 0] * X[:, 1], np.array([2., 2.]), np.zeros(2))
        self.assertAlmostEqual(phi[0], phi[1])

    def test_coalition_value(self):
        f = lambda X: X[:, 0] * 10 + X[:, 1]
        self.assertEqual(S.coalition_value(f, np.array([1., 2.]), np.array([0., 0.]), (1,)), 2.0)

    def test_max_d(self):
        with self.assertRaises(ValueError):
            S.shapley_values(lambda X: X.sum(1), np.ones(13), np.zeros(13))
''',
"feedback": [
    ("test_efficiency", "Use weights |S|!(d−|S|−1)!/d! and include the empty coalition."),
    ("test_interaction_split", "Average marginal contributions over all coalitions of the other features."),
    ("test_coalition_value", "Take x on coalition indices and the baseline elsewhere; call predict on shape (1, d)."),
    ("test_linear_matches_xa01", "For linear models Shapley values equal w·(x − baseline)."),
],
},
# ---------------------------------------------------------------- lime-local
{
"slug": "lime-local", "title": "LIME-style Local Linear Explanation",
"difficulty": "advanced", "prereqs": ["surrogate-fidelity", "sklearn-grid-search"], "packages": ["numpy"],
"objectives": ["Perturb an instance with binary feature masks", "Weight samples by proximity with an exponential kernel",
               "Fit a weighted linear model and read local coefficients"],
"tags": ["lime", "local-surrogate", "weighted-least-squares", "perturbation"],
"sources": ["S025", "S024"], "entry": "sample_masks(n, d, rng); lime_explain(predict, x, baseline, masks, kernel_width=0.75)",
"article": r'''
# LIME: Local Interpretable Model-agnostic Explanations

## Intuition
A complex model may be curved globally but almost linear in a small neighbourhood of one input. LIME
samples variations of the instance, asks the model about them, and fits a simple linear model that
is accurate *near* the instance.

## Precise explanation (Ribeiro et al., 2016, tabular variant used here)
1. **Interpretable representation:** binary masks $z \in \{0,1\}^d$; $z_j = 1$ keeps $x_j$, $z_j = 0$
   replaces it with the baseline value. Input for mask z: $x(z) = z\odot x + (1-z)\odot x'$.
2. **Sample** masks (always include the all-ones mask = the instance itself).
3. **Proximity weights:** with distance $D(z) = 1 - \frac{1}{d}\sum_j z_j$ (fraction of features
   removed), $\pi(z) = \exp(-D^2/\sigma^2)$, σ = kernel width.
4. **Weighted least squares:** fit $g(z) = \beta_0 + \beta\cdot z$ minimising
   $\sum \pi(z)(f(x(z)) - g(z))^2$: solve with rows scaled by $\sqrt{\pi}$.
The coefficient $\beta_j$ estimates the effect of including feature j. For a linear model $f$, LIME
recovers $\beta_j = w_j(x_j - x'_j)$ exactly (same as [[linear-contributions]]/[[exact-shapley]]).

## Worked example
f(x) = 2x₀ − x₁, x = (3, 1), baseline 0 → β = [6, −1], β₀ = 0, for any set of masks that spans the space.

## Common mistakes
* Fitting on raw perturbed features instead of the binary masks (changes what β means).
* Forgetting the weights (fits a global, not local, model).
* Too few samples → unstable explanations (re-run with other seeds to check).

## Why this matters
LIME is a widely used model-agnostic local explainer; implementing it shows exactly which design
choices (baseline, kernel width, sampling) affect explanations.
''',
"statement": r'''
Implement:
* `sample_masks(n, d, rng)` → int array `(n, d)` of 0/1 with **row 0 all ones** and the other rows
  `(rng.random((n-1, d)) < 0.5).astype(int)`.
* `lime_explain(predict, x, baseline, masks, kernel_width=0.75)` → dict
  `{"intercept": float, "coef": array(d), "weights": array(n)}` via weighted least squares
  (`np.linalg.lstsq` on `sqrt(weights)`-scaled design `[1, masks]` and targets). Raise `ValueError`
  if `kernel_width <= 0` or shapes mismatch.

**Example**
```python
f = lambda X: 2 * X[:, 0] - X[:, 1]
m = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])
lime_explain(f, np.array([3., 1.]), np.zeros(2), m)["coef"]   # [ 6., -1.]
```
''',
"starter": r'''
import numpy as np


def sample_masks(n, d, rng):
    pass


def lime_explain(predict, x, baseline, masks, kernel_width=0.75):
    pass
''',
"hints": [
    "Inputs: `Xz = masks * x + (1 - masks) * baseline`; `y = predict(Xz)`.",
    "`D = 1 - masks.mean(axis=1)`; `w = np.exp(-D**2 / kernel_width**2)`.",
    "`A = np.column_stack([ones, masks]) * sqrt(w)[:, None]`; `beta = lstsq(A, y * sqrt(w))`.",
],
"solution": r'''
import numpy as np


def sample_masks(n, d, rng):
    if n < 1 or d < 1:
        raise ValueError("n and d must be >= 1")
    rest = (rng.random((n - 1, d)) < 0.5).astype(int)
    return np.vstack([np.ones((1, d), dtype=int), rest])


def lime_explain(predict, x, baseline, masks, kernel_width=0.75):
    if kernel_width <= 0:
        raise ValueError("kernel_width must be positive")
    x = np.asarray(x, dtype=float)
    base = np.asarray(baseline, dtype=float)
    Z = np.asarray(masks, dtype=float)
    if Z.ndim != 2 or Z.shape[1] != x.shape[0] or base.shape != x.shape:
        raise ValueError("shape mismatch")
    Xz = Z * x + (1 - Z) * base
    y = np.asarray(predict(Xz), dtype=float)
    D = 1.0 - Z.mean(axis=1)
    w = np.exp(-(D ** 2) / kernel_width ** 2)
    sw = np.sqrt(w)
    A = np.column_stack([np.ones(len(Z)), Z]) * sw[:, None]
    beta, *_ = np.linalg.lstsq(A, y * sw, rcond=None)
    return {"intercept": float(beta[0]), "coef": beta[1:], "weights": w}
''',
"explanation": r'''
Masks map to concrete inputs by mixing the instance with the baseline. Samples closer to the
instance (fewer features removed) get larger kernel weights. Scaling rows by the square root of the
weights turns weighted least squares into ordinary least squares, whose coefficients are the local
explanation.
''',
"tests": r'''
import numpy as np

class TestLIME(unittest.TestCase):
    def test_linear_exact(self):
        f = lambda X: 2 * X[:, 0] - X[:, 1]
        m = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])
        r = S.lime_explain(f, np.array([3., 1.]), np.zeros(2), m)
        np.testing.assert_allclose(r["coef"], [6., -1.], atol=1e-10)
        self.assertAlmostEqual(r["intercept"], 0.0, places=10)

    def test_masks(self):
        m = S.sample_masks(50, 4, np.random.default_rng(0))
        self.assertEqual(m.shape, (50, 4))
        np.testing.assert_array_equal(m[0], 1)
        self.assertTrue(set(np.unique(m)) <= {0, 1})

    def test_masks_recipe(self):
        m = S.sample_masks(5, 3, np.random.default_rng(7))
        exp = (np.random.default_rng(7).random((4, 3)) < 0.5).astype(int)
        np.testing.assert_array_equal(m[1:], exp)

    def test_weights(self):
        m = np.array([[1, 1], [0, 0], [1, 0]])
        r = S.lime_explain(lambda X: X.sum(1), np.ones(2), np.zeros(2), m, kernel_width=1.0)
        np.testing.assert_allclose(r["weights"], [1.0, np.exp(-1.0), np.exp(-0.25)])

    def test_matches_shapley_linear_random_masks(self):
        rng = np.random.default_rng(1)
        w = np.array([1.5, -2.0, 0.5, 3.0]); x = rng.normal(size=4); base = rng.normal(size=4)
        r = S.lime_explain(lambda X: X @ w + 1, x, base, S.sample_masks(64, 4, rng))
        np.testing.assert_allclose(r["coef"], w * (x - base), atol=1e-9)

    def test_ignored_feature_zero(self):
        rng = np.random.default_rng(2)
        r = S.lime_explain(lambda X: np.exp(X[:, 0]), np.array([1., 5.]), np.zeros(2), S.sample_masks(40, 2, rng))
        self.assertAlmostEqual(r["coef"][1], 0.0, places=9)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.lime_explain(lambda X: X[:, 0], np.ones(2), np.zeros(2), np.ones((3, 2)), kernel_width=0)
''',
"feedback": [
    ("test_linear_exact", "Fit on the binary masks (with intercept), not on the raw perturbed inputs."),
    ("test_weights", "D = fraction of features removed; weight = exp(−D²/σ²)."),
    ("test_masks_recipe", "Row 0 is all ones; other rows are rng.random((n−1, d)) < 0.5."),
    ("test_matches_shapley_linear_random_masks", "Scale both the design rows and targets by sqrt(weight) before lstsq."),
],
},
# ---------------------------------------------------------------- counterfactual-search
{
"slug": "counterfactual-search", "title": "Minimal Counterfactual Search",
"difficulty": "advanced", "prereqs": ["decision-path"], "packages": ["numpy"],
"objectives": ["Define a counterfactual as a minimal change that flips a decision",
               "Search a grid of actionable changes exhaustively", "Respect immutable features and bounds"],
"tags": ["counterfactuals", "recourse", "search", "local-explanation"],
"sources": ["S024"], "entry": "find_counterfactual(predict, x, steps, max_steps=3, lower=None, upper=None)",
"article": r'''
# Counterfactual Explanations

## Intuition
"Your loan was rejected. If your income were 5 000 higher, it would have been approved." A
counterfactual explains a decision by the smallest realistic change to the input that changes the
outcome — and tells the person what they could do (recourse).

## Precise explanation
For a classifier `predict(X) -> labels`, an instance $x$ with label $c$, and per-feature step sizes
$\delta_j$ (0 = immutable, e.g. age or ethnicity):
* candidate changes: $x_j + k_j\delta_j$ with integers $|k_j| \le K$;
* cost: $\sum_j |k_j|$ (number of unit steps, an L1 distance in step units);
* find the minimum-cost candidate whose label differs from $c$, staying within optional bounds.
Exhaustive search over $(2K+1)^{d_\text{mutable}}$ candidates is fine for small problems and gives the
true minimum; real systems use optimisation or heuristics. Ties: smallest cost, then lexicographically
smallest step vector $k$.

## Worked example
predict = 1 if income + 2·savings ≥ 10; x = (4, 2) → 8 → class 0. Steps (1, 1): cost-1 options
(5, 2) → 9 ✗, (4, 3) → 10 ✓ → counterfactual: savings + 1.

## Common mistakes
* Changing immutable features.
* Returning any flipping point instead of the minimal one.
* Ignoring plausibility (bounds, realistic values).

## Why this matters
Counterfactuals are human-friendly, actionable explanations and relate to legal discussions of a
"right to explanation"; they also expose how close decisions are to the boundary.
''',
"statement": r'''
Write `find_counterfactual(predict, x, steps, max_steps=3, lower=None, upper=None)` returning `None`
if no counterfactual exists within the search space, else a dict
`{"x_cf": array, "k": tuple[int], "cost": int, "label": label}`.
* Enumerate all `k` with `k_j = 0` for features whose step is 0 and `|k_j| <= max_steps` otherwise
  (`itertools.product`); skip candidates outside `[lower, upper]` (element-wise, if given).
* Choose minimal cost, ties → smallest `k` tuple (Python ordering). Evaluate candidates in batches or
  one by one (both fine).

**Example**
```python
predict = lambda X: (X[:, 0] + 2 * X[:, 1] >= 10).astype(int)
find_counterfactual(predict, np.array([4., 2.]), np.array([1., 1.]))
# {'x_cf': array([4., 3.]), 'k': (0, 1), 'cost': 1, 'label': 1}
```
''',
"starter": r'''
from itertools import product

import numpy as np


def find_counterfactual(predict, x, steps, max_steps=3, lower=None, upper=None):
    return None
''',
"hints": [
    "Original label: `c = predict(x[None])[0]`.",
    "Ranges: `range(-max_steps, max_steps + 1)` if step != 0 else `(0,)`; build all k with `product`.",
    "Sort candidates by `(sum(abs(k)), k)` and return the first that flips the label and is in bounds.",
],
"solution": r'''
from itertools import product

import numpy as np


def find_counterfactual(predict, x, steps, max_steps=3, lower=None, upper=None):
    x = np.asarray(x, dtype=float)
    steps = np.asarray(steps, dtype=float)
    if steps.shape != x.shape or max_steps < 1:
        raise ValueError("steps must match x and max_steps must be >= 1")
    c = predict(x[None, :])[0]
    ranges = [range(-max_steps, max_steps + 1) if s != 0 else (0,) for s in steps]
    ks = sorted((k for k in product(*ranges) if any(k)), key=lambda k: (sum(abs(v) for v in k), k))
    if not ks:
        return None
    K = np.array(ks, dtype=float)
    cands = x + K * steps
    ok = np.ones(len(cands), dtype=bool)
    if lower is not None:
        ok &= (cands >= np.asarray(lower, dtype=float)).all(axis=1)
    if upper is not None:
        ok &= (cands <= np.asarray(upper, dtype=float)).all(axis=1)
    labels = predict(cands)
    for i in range(len(ks)):
        if ok[i] and labels[i] != c:
            return {"x_cf": cands[i], "k": tuple(int(v) for v in ks[i]), "cost": int(sum(abs(v) for v in ks[i])),
                    "label": labels[i]}
    return None
''',
"explanation": r'''
All step combinations are generated (immutable features fixed at 0), sorted by cost and then
lexicographically, and evaluated in one batch. The first in-bounds candidate whose predicted label
differs from the original is, by construction, a minimum-cost counterfactual.
''',
"tests": r'''
import numpy as np

P = lambda X: (X[:, 0] + 2 * X[:, 1] >= 10).astype(int)

class TestCF(unittest.TestCase):
    def test_example(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 1.]))
        np.testing.assert_allclose(r["x_cf"], [4., 3.])
        self.assertEqual((r["k"], r["cost"], int(r["label"])), ((0, 1), 1, 1))

    def test_immutable(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 0.]))
        self.assertEqual(r["k"], (2, 0))

    def test_none(self):
        self.assertIsNone(S.find_counterfactual(P, np.array([0., 0.]), np.array([1., 1.]), max_steps=2))

    def test_bounds(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 1.]), upper=np.array([100., 2.]))
        self.assertEqual(r["k"], (2, 0))

    def test_minimal_cost(self):
        f = lambda X: (X[:, 0] * X[:, 1] > 6).astype(int)
        r = S.find_counterfactual(f, np.array([2., 2.]), np.array([1., 1.]))
        self.assertEqual(r["cost"], 2)
        self.assertEqual(r["k"], (0, 2))

    def test_flip_other_direction(self):
        r = S.find_counterfactual(P, np.array([10., 1.]), np.array([0.5, 0.5]))
        self.assertEqual(int(r["label"]), 0)
        self.assertEqual((r["k"], r["cost"]), ((-1, -2), 3))

    def test_label_differs(self):
        r = S.find_counterfactual(P, np.array([4., 2.]), np.array([1., 1.]))
        self.assertNotEqual(int(P(r["x_cf"][None])[0]), int(P(np.array([[4., 2.]]))[0]))
''',
"feedback": [
    ("test_example", "Sort candidates by (cost, k) and return the first that flips the label."),
    ("test_immutable", "Features with step 0 must never change."),
    ("test_bounds", "Skip candidates outside lower/upper."),
    ("test_none", "Return None if no candidate within max_steps changes the prediction."),
],
},
# ---------------------------------------------------------------- integrated-gradients
{
"slug": "integrated-gradients", "title": "Integrated Gradients",
"difficulty": "advanced", "prereqs": ["exact-shapley", "neuron-backprop"], "packages": ["numpy"],
"objectives": ["Integrate gradients along the straight path from a baseline", "Approximate the integral with a midpoint Riemann sum",
               "Check the completeness axiom"],
"tags": ["integrated-gradients", "gradient-attribution", "completeness", "deep-learning-explanations"],
"sources": ["S027", "S024"], "entry": "integrated_gradients(grad_fn, x, baseline, steps=50)",
"article": r'''
# Integrated Gradients

## Intuition
A plain gradient tells you the local slope, which can be zero for a saturated neuron even when the
feature mattered. Integrated gradients (IG) accumulate gradients along the whole path from a
baseline (e.g. a black image) to the input, so nothing that mattered along the way is missed.

## Precise explanation (Sundararajan et al., 2017)
$$\text{IG}_j(x) = (x_j - x'_j)\int_0^1 \frac{\partial f}{\partial x_j}\big(x' + \alpha(x - x')\big)\,d\alpha.$$
**Completeness:** $\sum_j \text{IG}_j = f(x) - f(x')$ (by the fundamental theorem of calculus along
the path). Approximate the integral with a **midpoint Riemann sum** over m steps:
$\alpha_k = (k + 0.5)/m$, $k = 0..m-1$, average the gradients and multiply by $(x - x')$. Error
shrinks as m grows (compare [[trapezoid-rule]]). For linear models IG equals $w_j(x_j - x'_j)$ — again matching
[[linear-contributions]]/[[exact-shapley]].

## Worked example
f(x) = x₀²·x₁, x = (1, 2), baseline 0: ∂f/∂x₀ = 2x₀x₁, ∂f/∂x₁ = x₀². On the path (α, 2α):
∫ 4α² dα = 4/3 → IG₀ = 4/3; ∫ α² dα = 1/3 → IG₁ = 2/3; sum = 2 = f(x) ✓.

## Common mistakes
* Forgetting the (x − x′) factor.
* Endpoint Riemann sums with few steps (biased); use midpoints.
* Choosing a baseline that is not "neutral" for the task and misreading results.

## Why this matters
IG is a standard attribution method for neural networks (images, text) and satisfies axioms that
plain gradients violate.
''',
"statement": r'''
Write `integrated_gradients(grad_fn, x, baseline, steps=50)` where `grad_fn(points)` takes an array
`(m, d)` of inputs and returns their gradients `(m, d)`. Use the midpoint rule with a **single**
`grad_fn` call on all path points. Return `(attributions, alphas)`. Raise `ValueError` if
`steps < 1` or shapes differ.

**Example**
```python
grad = lambda P: np.column_stack([2 * P[:, 0] * P[:, 1], P[:, 0] ** 2])
ig, _ = integrated_gradients(grad, np.array([1., 2.]), np.zeros(2), steps=1000)
ig        # ≈ [1.33333, 0.66667]
```
''',
"starter": r'''
import numpy as np


def integrated_gradients(grad_fn, x, baseline, steps=50):
    pass
''',
"hints": [
    "`alphas = (np.arange(steps) + 0.5) / steps`.",
    "`points = baseline + alphas[:, None] * (x - baseline)`.",
    "`ig = (x - baseline) * grad_fn(points).mean(axis=0)`.",
],
"solution": r'''
import numpy as np


def integrated_gradients(grad_fn, x, baseline, steps=50):
    x = np.asarray(x, dtype=float)
    base = np.asarray(baseline, dtype=float)
    if steps < 1 or x.shape != base.shape:
        raise ValueError("steps must be >= 1 and shapes must match")
    alphas = (np.arange(steps) + 0.5) / steps
    points = base + alphas[:, None] * (x - base)
    grads = np.asarray(grad_fn(points), dtype=float)
    return (x - base) * grads.mean(axis=0), alphas
''',
"explanation": r'''
All points along the straight path are built at once and their gradients computed in one batch; the
midpoint average approximates the path integral, and multiplying by the input–baseline difference
gives the attribution per feature.
''',
"tests": r'''
import numpy as np

F = lambda P: P[:, 0] ** 2 * P[:, 1]
G = lambda P: np.column_stack([2 * P[:, 0] * P[:, 1], P[:, 0] ** 2])

class TestIG(unittest.TestCase):
    def test_example(self):
        ig, _ = S.integrated_gradients(G, np.array([1., 2.]), np.zeros(2), steps=1000)
        np.testing.assert_allclose(ig, [4 / 3, 2 / 3], atol=1e-5)

    def test_completeness(self):
        x, b = np.array([1.5, -0.5]), np.array([0.2, 0.3])
        ig, _ = S.integrated_gradients(G, x, b, steps=2000)
        self.assertAlmostEqual(ig.sum(), F(x[None])[0] - F(b[None])[0], places=5)

    def test_linear_exact(self):
        w = np.array([2., -3., 0.5])
        ig, _ = S.integrated_gradients(lambda P: np.tile(w, (len(P), 1)), np.array([1., 2., 3.]), np.zeros(3), steps=1)
        np.testing.assert_allclose(ig, w * np.array([1., 2., 3.]))

    def test_alphas_midpoint(self):
        _, a = S.integrated_gradients(G, np.ones(2), np.zeros(2), steps=4)
        np.testing.assert_allclose(a, [0.125, 0.375, 0.625, 0.875])

    def test_single_call(self):
        calls = []
        def g(P):
            calls.append(P.shape); return G(P)
        S.integrated_gradients(g, np.ones(2), np.zeros(2), steps=7)
        self.assertEqual(calls, [(7, 2)])

    def test_saturation_vs_gradient(self):
        sig = lambda z: 1 / (1 + np.exp(-z))
        g = lambda P: (sig(10 * P) * (1 - sig(10 * P))) * 10
        x = np.array([5.0])
        ig, _ = S.integrated_gradients(g, x, np.zeros(1), steps=4000)
        self.assertLess(float(g(x[None])[0, 0]), 1e-15)
        self.assertAlmostEqual(ig[0], sig(50) - 0.5, places=4)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.integrated_gradients(G, np.ones(2), np.zeros(3))
''',
"feedback": [
    ("test_alphas_midpoint", "Midpoint rule: alpha_k = (k + 0.5) / steps."),
    ("test_completeness", "Multiply the averaged gradient by (x − baseline)."),
    ("test_single_call", "Build all path points and call grad_fn once."),
    ("test_saturation_vs_gradient", "IG captures effects even where the local gradient is ~0."),
],
},
]
