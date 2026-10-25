"""Problem definitions for the machine learning topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- train-test-split
{
"slug": "train-test-split", "title": "Seeded Train/Test Split", "optional": True,
"difficulty": "beginner", "prereqs": ["ml-baselines", "seeded-generator"], "packages": ["numpy"],
"objectives": ["Split data into disjoint train and test sets", "Keep X and y aligned when shuffling",
               "Implement a stratified split"],
"tags": ["train-test-split", "stratification", "generalisation"],
"sources": ["S012", "S007"], "entry": "train_test_split(X, y, test_size=0.25, seed=0, stratify=False)",
"article": r'''
# Train/Test Splits

## Intuition
A model is useful only if it works on data it hasn't seen. Hold some data back — the **test
set** — and never use it for training or tuning; it estimates performance on new data.

## Precise explanation
* Shuffle indices once (seeded), then take the first `n_test` as test and the rest as train.
  Index X and y with the **same** index arrays so features and labels stay paired.
* `n_test = round(n * test_size)` (here, and at least 1 and at most n − 1).
* **Stratified split:** keep class proportions similar in train and test by splitting each class
  separately and combining. Important for imbalanced classes — a random split of 95/5 data might
  put no minority examples in the test set.
* Typical sizes: 70–80 % train, 20–30 % test; a separate validation set (or cross-validation,
  [[k-fold-cv]]) is used for tuning.

## Worked example
n = 8, test_size = 0.25 → n_test = 2. With a permutation [5, 2, 7, 0, 1, 3, 6, 4], test rows
are 5, 2 and train rows the other six.

## Common mistakes
* Shuffling X and y separately (pairs broken).
* Splitting *after* preprocessing with statistics from all data (leakage; [[standard-scaler]]).
* Unseeded splits, making results irreproducible.

## Why this matters
Every evaluation in the remaining topics depends on an honest, reproducible split.
''',
"statement": r'''
Write `train_test_split(X, y, test_size=0.25, seed=0, stratify=False)` returning
`(X_train, X_test, y_train, y_test)` as NumPy arrays.

* `rng = np.random.default_rng(seed)`.
* Non-stratified: `perm = rng.permutation(n)`; `n_test = round(n * test_size)` clipped to
  `[1, n-1]`; test = `perm[:n_test]`, train = `perm[n_test:]`.
* Stratified: for each class `c` in `np.unique(y)` (sorted), shuffle that class's indices with
  `rng.permutation`, put `round(n_c * test_size)` of them in test (rest in train); concatenate
  over classes in class order.
* Raise `ValueError` if `len(X) != len(y)`, `n < 2`, or `test_size` not in `(0, 1)`.

**Example**
```python
X = np.arange(20).reshape(10, 2); y = np.array([0]*8 + [1]*2)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, seed=1, stratify=True)
sorted(yte.tolist())    # [0, 0, 0, 0, 1]  — class ratio preserved
```
''',
"starter": r'''
import numpy as np


def train_test_split(X, y, test_size=0.25, seed=0, stratify=False):
    # TODO
    pass
''',
"hints": [
    "Convert with `np.asarray`, validate, and create one `rng`.",
    "Non-stratified: `perm = rng.permutation(n)`; slice into test/train index arrays.",
    "Stratified: loop over `np.unique(y)`, permute `np.flatnonzero(y == c)` and split each.",
],
"solution": r'''
import numpy as np


def train_test_split(X, y, test_size=0.25, seed=0, stratify=False):
    X = np.asarray(X)
    y = np.asarray(y)
    n = len(X)
    if len(y) != n:
        raise ValueError("X and y must have the same length")
    if n < 2:
        raise ValueError("need at least two samples")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be in (0, 1)")
    rng = np.random.default_rng(seed)
    if not stratify:
        perm = rng.permutation(n)
        n_test = min(max(round(n * test_size), 1), n - 1)
        te, tr = perm[:n_test], perm[n_test:]
    else:
        te_parts, tr_parts = [], []
        for c in np.unique(y):
            idx = rng.permutation(np.flatnonzero(y == c))
            k = round(len(idx) * test_size)
            te_parts.append(idx[:k])
            tr_parts.append(idx[k:])
        te, tr = np.concatenate(te_parts), np.concatenate(tr_parts)
    return X[tr], X[te], y[tr], y[te]
''',
"explanation": r'''
A single permutation of row indices is used for both X and y, so pairs stay aligned. The
stratified variant applies the same idea per class, preserving class proportions. All randomness
flows through one seeded generator.
''',
"tests": r'''
import numpy as np

X = np.arange(40).reshape(20, 2)
y = np.array([0] * 15 + [1] * 5)

class TestSplit(unittest.TestCase):
    def test_sizes(self):
        Xtr, Xte, ytr, yte = S.train_test_split(X, y, test_size=0.25, seed=0)
        self.assertEqual((len(Xtr), len(Xte), len(ytr), len(yte)), (15, 5, 15, 5))

    def test_disjoint_cover(self):
        Xtr, Xte, _, _ = S.train_test_split(X, y, seed=3)
        rows = sorted(Xtr[:, 0].tolist() + Xte[:, 0].tolist())
        self.assertEqual(rows, list(range(0, 40, 2)))

    def test_alignment(self):
        Xtr, Xte, ytr, yte = S.train_test_split(X, y, seed=5)
        np.testing.assert_array_equal(ytr, (Xtr[:, 0] // 2 >= 15).astype(int))
        np.testing.assert_array_equal(yte, (Xte[:, 0] // 2 >= 15).astype(int))

    def test_reproducible(self):
        a = S.train_test_split(X, y, seed=9)
        b = S.train_test_split(X, y, seed=9)
        np.testing.assert_array_equal(a[1], b[1])

    def test_recipe(self):
        perm = np.random.default_rng(2).permutation(20)
        _, Xte, _, _ = S.train_test_split(X, y, test_size=0.25, seed=2)
        np.testing.assert_array_equal(Xte, X[perm[:5]])

    def test_stratified(self):
        _, _, ytr, yte = S.train_test_split(X, y, test_size=0.4, seed=1, stratify=True)
        self.assertEqual((int((yte == 1).sum()), int((yte == 0).sum())), (2, 6))
        self.assertEqual(int((ytr == 1).sum()), 3)

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.train_test_split(X, y[:5])
        with self.assertRaises(ValueError):
            S.train_test_split(X, y, test_size=1.0)
''',
"feedback": [
    ("test_alignment", "Index X and y with the same permutation."),
    ("test_recipe", "Use rng = default_rng(seed); perm = rng.permutation(n); test = perm[:n_test]."),
    ("test_stratified", "Split each class separately with round(n_c * test_size) test samples."),
    ("test_disjoint_cover", "Train and test must partition all rows."),
],
},
# ---------------------------------------------------------------- regression-metrics
{
"slug": "regression-metrics", "title": "Regression Metrics", "optional": True,
"difficulty": "beginner", "prereqs": ["ml-baselines"], "packages": ["numpy"],
"objectives": ["Compute MSE, RMSE, MAE and R²", "Interpret R² relative to a mean baseline",
               "Handle degenerate targets"],
"tags": ["metrics", "mse", "mae", "r2", "evaluation"],
"sources": ["S012"], "entry": "regression_report(y_true, y_pred)",
"article": r'''
# Measuring Regression Error

## Intuition
How wrong are the predictions? Average the errors — but squared errors punish big misses more
than absolute errors. R² compares the model with the simplest possible model: always predicting
the mean.

## Precise explanation
With residuals $e_i = y_i - \hat y_i$:
* $\text{MSE} = \frac1n\sum e_i^2$, $\text{RMSE} = \sqrt{\text{MSE}}$ (same units as y).
* $\text{MAE} = \frac1n\sum |e_i|$ — less sensitive to outliers.
* $R^2 = 1 - \frac{\sum e_i^2}{\sum (y_i - \bar y)^2}$. $R^2 = 1$ is perfect, 0 equals the mean
  baseline, negative is *worse* than the baseline. Undefined when all $y_i$ are equal.

## Worked example
y = [3, 5, 7], ŷ = [2, 5, 9]: e = [1, 0, −2]; MSE 5/3 ≈ 1.667, RMSE 1.291, MAE 1;
Σ(y−ȳ)² = 8, R² = 1 − 5/8 = 0.375.

## Common mistakes
* Averaging signed errors (positive and negative cancel).
* Swapping arguments in R² (it is not symmetric).
* Reporting R² on training data only.

## Why this matters
These metrics evaluate [[least-squares-line]]/07/12 and are the losses many models minimise.
''',
"statement": r'''
Write `regression_report(y_true, y_pred)` returning a dict of floats
`{"mse", "rmse", "mae", "r2"}`. Raise `ValueError` for empty or mismatched inputs, and for
constant `y_true` (R² undefined).

**Example**
```python
regression_report([3, 5, 7], [2, 5, 9])
# {'mse': 1.6667, 'rmse': 1.2910, 'mae': 1.0, 'r2': 0.375}  (rounded here)
```
''',
"starter": r'''
import numpy as np


def regression_report(y_true, y_pred):
    # TODO
    pass
''',
"hints": [
    "`e = y_true - y_pred` with float arrays.",
    "`mse = np.mean(e ** 2)`, `mae = np.mean(np.abs(e))`.",
    "`ss_tot = np.sum((y_true - y_true.mean()) ** 2)`; raise if it is 0.",
],
"solution": r'''
import numpy as np


def regression_report(y_true, y_pred):
    yt = np.asarray(y_true, dtype=float)
    yp = np.asarray(y_pred, dtype=float)
    if yt.size == 0 or yt.shape != yp.shape:
        raise ValueError("inputs must be non-empty and the same shape")
    e = yt - yp
    mse = float(np.mean(e ** 2))
    ss_tot = float(np.sum((yt - yt.mean()) ** 2))
    if ss_tot == 0:
        raise ValueError("R^2 undefined for constant y_true")
    return {"mse": mse, "rmse": float(np.sqrt(mse)), "mae": float(np.mean(np.abs(e))),
            "r2": 1.0 - float(np.sum(e ** 2)) / ss_tot}
''',
"explanation": r'''
All four metrics come from the residual vector. R² divides the residual sum of squares by the
total sum of squares around the mean, so it measures improvement over the constant-mean model.
''',
"tests": r'''
import numpy as np

class TestRegMetrics(unittest.TestCase):
    def test_example(self):
        r = S.regression_report([3, 5, 7], [2, 5, 9])
        self.assertAlmostEqual(r["mse"], 5 / 3)
        self.assertAlmostEqual(r["rmse"], np.sqrt(5 / 3))
        self.assertAlmostEqual(r["mae"], 1.0)
        self.assertAlmostEqual(r["r2"], 0.375)

    def test_perfect(self):
        r = S.regression_report([1, 2, 3], [1, 2, 3])
        self.assertEqual((r["mse"], r["r2"]), (0.0, 1.0))

    def test_mean_baseline_zero_r2(self):
        self.assertAlmostEqual(S.regression_report([1, 2, 3], [2, 2, 2])["r2"], 0.0)

    def test_negative_r2(self):
        self.assertLess(S.regression_report([1, 2, 3], [3, 2, 1])["r2"], 0)

    def test_constant_target(self):
        with self.assertRaises(ValueError):
            S.regression_report([4, 4], [4, 5])

    def test_mismatch(self):
        with self.assertRaises(ValueError):
            S.regression_report([1, 2], [1])

    def test_types(self):
        self.assertTrue(all(isinstance(v, float) for v in S.regression_report([1, 2], [1, 3]).values()))
''',
"feedback": [
    ("test_example", "Use the mean of squared and absolute residuals; R² = 1 − SS_res/SS_tot."),
    ("test_negative_r2", "Don't clip R² at 0 — worse-than-mean models have negative R²."),
    ("test_constant_target", "Raise ValueError when y_true has zero variance."),
    ("test_types", "Return plain Python floats."),
],
},
# ---------------------------------------------------------------- classification-metrics
{
"slug": "classification-metrics", "title": "Confusion Matrix, Precision, Recall, F1",
"difficulty": "beginner", "prereqs": ["ml-baselines"], "packages": ["numpy"],
"objectives": ["Build a multi-class confusion matrix", "Compute per-class precision, recall and F1",
               "Handle zero-division and macro averaging"],
"tags": ["metrics", "confusion-matrix", "precision", "recall", "f1"],
"sources": ["S012"], "entry": "confusion_matrix(y_true, y_pred, n_classes); classification_report(y_true, y_pred, n_classes)",
"article": r'''
# Beyond Accuracy

## Intuition
A spam filter that never flags spam is 95 % accurate if only 5 % of emails are spam — and
useless. The **confusion matrix** shows which classes are confused with which; precision and
recall summarise it per class.

## Precise explanation
Confusion matrix $C$ with rows = true class, columns = predicted class: $C_{ij}$ counts examples
of class $i$ predicted as $j$. For class $k$:
* TP $= C_{kk}$, FP = column sum − TP, FN = row sum − TP.
* Precision $= \frac{TP}{TP+FP}$ ("of those predicted k, how many were k").
* Recall $= \frac{TP}{TP+FN}$ ("of the true k, how many were found").
* $F_1 = \frac{2PR}{P+R}$ — harmonic mean, low if either is low.
* When a denominator is 0 we define the value as 0 (scikit-learn's `zero_division=0`).
* **Macro average** = unweighted mean over classes; accuracy = trace / total.

Vectorised construction: `np.add.at(C, (y_true, y_pred), 1)`.

## Worked example
y = [0, 0, 1, 1, 2], ŷ = [0, 1, 1, 1, 0]:
C = [[1,1,0],[0,2,0],[1,0,0]]; class 1: P = 2/3, R = 1, F1 = 0.8; class 2: P = R = F1 = 0.

## Common mistakes
* Transposing the matrix (rows vs columns).
* Averaging F1 incorrectly (F1 of averages ≠ average of F1s).
* Dividing by zero for classes never predicted.

## Why this matters
Imbalanced problems (fraud, disease, rare tokens) are judged by precision/recall, and per-class
reports reveal fairness issues.
''',
"statement": r'''
Implement:
* `confusion_matrix(y_true, y_pred, n_classes)` → int array `(n_classes, n_classes)`, rows =
  true labels. Raise `ValueError` for mismatched lengths or labels outside `0..n_classes-1`.
* `classification_report(y_true, y_pred, n_classes)` → dict with `"precision"`, `"recall"`,
  `"f1"` (float arrays of length n_classes, zero where undefined), `"accuracy"` and `"macro_f1"`
  (floats).

**Example**
```python
confusion_matrix([0, 0, 1, 1, 2], [0, 1, 1, 1, 0], 3)   # [[1,1,0],[0,2,0],[1,0,0]]
classification_report([0, 0, 1, 1, 2], [0, 1, 1, 1, 0], 3)["f1"]   # [0.5, 0.8, 0.0]
```
''',
"starter": r'''
import numpy as np


def confusion_matrix(y_true, y_pred, n_classes):
    # TODO
    pass


def classification_report(y_true, y_pred, n_classes):
    # TODO
    pass
''',
"hints": [
    "`C = np.zeros((K, K), dtype=int); np.add.at(C, (yt, yp), 1)`.",
    "TP = `np.diag(C)`, predicted totals = `C.sum(axis=0)`, true totals = `C.sum(axis=1)`.",
    "Safe division: `np.divide(a, b, out=np.zeros_like(a, dtype=float), where=b > 0)`.",
],
"solution": r'''
import numpy as np


def confusion_matrix(y_true, y_pred, n_classes):
    yt = np.asarray(y_true, dtype=int)
    yp = np.asarray(y_pred, dtype=int)
    if yt.shape != yp.shape:
        raise ValueError("length mismatch")
    if yt.size and (min(yt.min(), yp.min()) < 0 or max(yt.max(), yp.max()) >= n_classes):
        raise ValueError("label out of range")
    C = np.zeros((n_classes, n_classes), dtype=int)
    np.add.at(C, (yt, yp), 1)
    return C


def _safe_div(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return np.divide(a, b, out=np.zeros_like(a), where=b > 0)


def classification_report(y_true, y_pred, n_classes):
    C = confusion_matrix(y_true, y_pred, n_classes)
    tp = np.diag(C)
    precision = _safe_div(tp, C.sum(axis=0))
    recall = _safe_div(tp, C.sum(axis=1))
    f1 = _safe_div(2 * precision * recall, precision + recall)
    total = C.sum()
    return {"precision": precision, "recall": recall, "f1": f1,
            "accuracy": float(tp.sum() / total) if total else 0.0,
            "macro_f1": float(f1.mean())}
''',
"explanation": r'''
`np.add.at` increments one cell per (true, predicted) pair, even with repeated pairs. Column sums
are predicted counts, row sums true counts, the diagonal true positives. A guarded division sets
undefined ratios to zero.
''',
"tests": r'''
import numpy as np

YT, YP = [0, 0, 1, 1, 2], [0, 1, 1, 1, 0]

class TestClsMetrics(unittest.TestCase):
    def test_cm(self):
        np.testing.assert_array_equal(S.confusion_matrix(YT, YP, 3), [[1, 1, 0], [0, 2, 0], [1, 0, 0]])

    def test_precision_recall(self):
        r = S.classification_report(YT, YP, 3)
        np.testing.assert_allclose(r["precision"], [0.5, 2 / 3, 0.0])
        np.testing.assert_allclose(r["recall"], [0.5, 1.0, 0.0])

    def test_f1_macro(self):
        r = S.classification_report(YT, YP, 3)
        np.testing.assert_allclose(r["f1"], [0.5, 0.8, 0.0])
        self.assertAlmostEqual(r["macro_f1"], 1.3 / 3)

    def test_accuracy(self):
        self.assertAlmostEqual(S.classification_report(YT, YP, 3)["accuracy"], 0.6)

    def test_unused_class(self):
        r = S.classification_report([0, 1], [0, 1], 3)
        np.testing.assert_allclose(r["f1"], [1, 1, 0])

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            S.confusion_matrix([0, 3], [0, 1], 3)

    def test_cm_total(self):
        rng = np.random.default_rng(0)
        a, b = rng.integers(0, 4, 50), rng.integers(0, 4, 50)
        C = S.confusion_matrix(a, b, 4)
        self.assertEqual(C.sum(), 50)
        np.testing.assert_array_equal(C.sum(axis=1), np.bincount(a, minlength=4))
''',
"feedback": [
    ("test_cm", "Rows are true labels, columns predicted labels."),
    ("test_precision_recall", "Precision divides by column sums, recall by row sums."),
    ("test_unused_class", "Use 0 when a denominator is 0 instead of NaN."),
    ("test_cm_total", "Use np.add.at so repeated (true, pred) pairs all count."),
],
},
# ---------------------------------------------------------------- standard-scaler
{
"slug": "standard-scaler", "title": "Standard Scaler (fit on train only)", "optional": True,
"difficulty": "beginner", "prereqs": ["train-test-split"], "packages": ["numpy"],
"objectives": ["Write a fit/transform class", "Avoid data leakage by fitting only on training data",
               "Invert the transformation"],
"tags": ["preprocessing", "standardization", "leakage", "classes"],
"sources": ["S012"], "entry": "class StandardScaler: fit, transform, fit_transform, inverse_transform",
"article": r'''
# Fit/Transform and Data Leakage

## Intuition
Standardising needs a mean and a standard deviation. If you compute them on *all* data, the
test set has quietly influenced training — information has **leaked**. Learn the statistics on
the training set, then apply those same numbers to the test set.

## Precise explanation
The **estimator** pattern (used by scikit-learn):
* `fit(X)` learns parameters (here `mean_`, `scale_` per column) and returns `self`.
* `transform(X)` applies them: $(X - \mu)/\sigma$.
* `fit_transform(X)` = fit then transform.
* `inverse_transform(Z)` = $Z\sigma + \mu$.
* Calling `transform` before `fit` should raise an error.
Constant columns have $\sigma = 0$; use scale 1 so they map to 0 instead of NaN.

## Worked example
Train X = [[1], [3]] → mean 2, std 1. Test x = 5 → z = 3 (not 0!) — the test point is far from
the training data, and the scaler correctly reports it.

## Common mistakes
* `fit` on the test set (or refitting on each batch at prediction time).
* Returning a new array from `fit` instead of `self`.
* Using the sample std in one place and population std elsewhere.

## Why this matters
Leakage is one of the most common reasons ML results fail to reproduce; this pattern also
structures [[knn-classifier]]…[[ridge-regression]] models.
''',
"statement": r'''
Implement `class StandardScaler` with attributes `mean_` and `scale_` (both `None` until fit):
* `fit(X)` → stores column means and population stds (zero std replaced by 1.0); returns `self`.
* `transform(X)` → standardized array; raise `RuntimeError` if not fitted, `ValueError` if the
  number of columns differs from fit.
* `fit_transform(X)`, `inverse_transform(Z)`.

**Example**
```python
sc = StandardScaler().fit(np.array([[1., 10.], [3., 10.]]))
sc.mean_, sc.scale_        # (array([ 2., 10.]), array([1., 1.]))
sc.transform([[5., 10.]])  # array([[3., 0.]])
```
''',
"starter": r'''
import numpy as np


class StandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        # TODO
        return self

    def transform(self, X):
        # TODO
        pass

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        # TODO
        pass
''',
"hints": [
    "In fit: `self.mean_ = X.mean(axis=0)`; `std = X.std(axis=0)`.",
    "`self.scale_ = np.where(std == 0, 1.0, std)`.",
    "Check `self.mean_ is None` in transform and compare `X.shape[1]` with `len(self.mean_)`.",
],
"solution": r'''
import numpy as np


class StandardScaler:
    def __init__(self):
        self.mean_ = None
        self.scale_ = None

    def fit(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[0] == 0:
            raise ValueError("X must be a non-empty 2-D array")
        self.mean_ = X.mean(axis=0)
        std = X.std(axis=0)
        self.scale_ = np.where(std == 0, 1.0, std)
        return self

    def _check(self, X):
        if self.mean_ is None:
            raise RuntimeError("scaler is not fitted")
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[1] != self.mean_.shape[0]:
            raise ValueError("wrong number of columns")
        return X

    def transform(self, X):
        X = self._check(X)
        return (X - self.mean_) / self.scale_

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, Z):
        Z = self._check(Z)
        return Z * self.scale_ + self.mean_
''',
"explanation": r'''
`fit` learns per-column statistics only from the data it is given and returns `self` for
chaining. `transform` reuses the stored statistics, so test data is scaled with training
parameters. A shared `_check` enforces fitting and column consistency.
''',
"tests": r'''
import numpy as np

class TestScaler(unittest.TestCase):
    def test_fit_params(self):
        sc = S.StandardScaler().fit(np.array([[1., 10.], [3., 10.]]))
        np.testing.assert_allclose(sc.mean_, [2, 10])
        np.testing.assert_allclose(sc.scale_, [1, 1])

    def test_transform_test_point(self):
        sc = S.StandardScaler().fit(np.array([[1., 10.], [3., 10.]]))
        np.testing.assert_allclose(sc.transform([[5., 10.]]), [[3., 0.]])

    def test_fit_returns_self(self):
        sc = S.StandardScaler()
        self.assertIs(sc.fit(np.ones((2, 2))), sc)

    def test_not_fitted(self):
        with self.assertRaises(RuntimeError):
            S.StandardScaler().transform(np.ones((1, 2)))

    def test_wrong_columns(self):
        sc = S.StandardScaler().fit(np.ones((3, 2)))
        with self.assertRaises(ValueError):
            sc.transform(np.ones((3, 3)))

    def test_roundtrip(self):
        X = np.random.default_rng(0).normal(3, 2, size=(20, 4))
        sc = S.StandardScaler()
        np.testing.assert_allclose(sc.inverse_transform(sc.fit_transform(X)), X)

    def test_no_leakage(self):
        Xtr = np.array([[0.], [2.]])
        Xte = np.array([[100.]])
        sc = S.StandardScaler().fit(Xtr)
        sc.transform(Xte)
        np.testing.assert_allclose(sc.mean_, [1.0])
''',
"feedback": [
    ("test_transform_test_point", "Use the stored training mean/std; never refit inside transform."),
    ("test_fit_returns_self", "fit must `return self`."),
    ("test_not_fitted", "Raise RuntimeError when transform is called before fit."),
    ("test_fit_params", "Constant columns get scale 1.0 (not 0)."),
],
},
# ---------------------------------------------------------------- least-squares-line
{
"slug": "least-squares-line", "title": "Least-Squares Line",
"difficulty": "intermediate", "prereqs": ["sklearn-estimator-api", "covariance-correlation"], "packages": ["numpy"],
"objectives": ["Derive the closed-form slope and intercept", "Predict with a fitted line",
               "Relate slope to covariance/variance"],
"tags": ["linear-regression", "least-squares", "closed-form"],
"sources": ["S009", "S012"], "entry": "class SimpleLinearRegression: fit(x, y), predict(x), score(x, y)",
"article": r'''
# Fitting a Line by Least Squares

## Intuition
Among all straight lines, pick the one that makes the squared vertical gaps to the points as
small as possible. Squaring treats over- and under-predictions alike and gives a closed-form
answer.

## Precise explanation
Minimise $L(a, b) = \sum (y_i - (a + b x_i))^2$. Setting both partial derivatives to zero gives
$$b = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sum (x_i-\bar x)^2} = \frac{\operatorname{cov}(x,y)}{\operatorname{var}(x)},\qquad a = \bar y - b\bar x.$$
The fitted line always passes through $(\bar x, \bar y)$. If all $x$ are equal the slope is
undefined. In matrix form (many features) this is the normal equation
$w = (X^\top X)^{-1} X^\top y$ ([[linalg-solve]] used `lstsq`; [[ridge-regression]] adds regularisation).

<svg xmlns="http://www.w3.org/2000/svg" width="260" height="170" viewBox="0 0 260 170" role="img" aria-label="Scatter of five points with a fitted line and vertical residual segments">
<title>Least-squares residuals</title>
<line x1="20" y1="150" x2="250" y2="150" stroke="#999"/><line x1="20" y1="150" x2="20" y2="10" stroke="#999"/>
<line x1="30" y1="140" x2="240" y2="30" stroke="#1f77b4" stroke-width="2"/>
<circle cx="50" cy="118" r="4"/><line x1="50" y1="118" x2="50" y2="129.5" stroke="#d62728"/>
<circle cx="90" cy="118" r="4"/><line x1="90" y1="118" x2="90" y2="108.6" stroke="#d62728"/>
<circle cx="140" cy="70" r="4"/><line x1="140" y1="70" x2="140" y2="82.4" stroke="#d62728"/>
<circle cx="190" cy="66" r="4"/><line x1="190" y1="66" x2="190" y2="56.2" stroke="#d62728"/>
<circle cx="225" cy="30" r="4"/><line x1="225" y1="30" x2="225" y2="37.9" stroke="#d62728"/>
</svg>

*Figure (original): the blue line minimises the sum of squared red residuals.*

## Worked example
x = [1, 2, 3, 4], y = [2, 4, 5, 8] → b = 9.5/5 = 1.9, a = 4.75 − 1.9·2.5 = 0. Prediction at
x = 5: 9.5.

## Common mistakes
* Minimising perpendicular distances (that is a different method).
* Forgetting the intercept.
* Extrapolating far beyond the training x-range.

## Why this matters
Linear regression is the baseline model for every regression task and the building block of
GLMs, neural network output layers and many explanations ([[linear-contributions]]).
''',
"statement": r'''
Implement `class SimpleLinearRegression` with attributes `intercept_`, `slope_` (None before fit):
* `fit(x, y)` — closed form; return `self`. Raise `ValueError` for fewer than 2 points,
  mismatched lengths, or constant `x`.
* `predict(x)` → NumPy array; raise `RuntimeError` if not fitted.
* `score(x, y)` → R² of predictions.

**Example**
```python
m = SimpleLinearRegression().fit([1, 2, 3, 4], [2, 4, 5, 8])
m.slope_, m.intercept_    # (1.9, 0.0)
m.predict([5])            # array([9.5])
```
''',
"starter": r'''
import numpy as np


class SimpleLinearRegression:
    def __init__(self):
        self.intercept_ = None
        self.slope_ = None

    def fit(self, x, y):
        # TODO
        return self

    def predict(self, x):
        # TODO
        pass

    def score(self, x, y):
        # TODO
        pass
''',
"hints": [
    "`dx = x - x.mean()`, `dy = y - y.mean()`; `sxx = (dx**2).sum()`.",
    "`slope = (dx*dy).sum() / sxx`, `intercept = y.mean() - slope * x.mean()`.",
    "R² = 1 − SS_res / SS_tot ([[regression-metrics]]).",
],
"solution": r'''
import numpy as np


class SimpleLinearRegression:
    def __init__(self):
        self.intercept_ = None
        self.slope_ = None

    def fit(self, x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        if x.shape != y.shape or x.size < 2:
            raise ValueError("need at least two matching points")
        dx, dy = x - x.mean(), y - y.mean()
        sxx = float((dx ** 2).sum())
        if sxx == 0:
            raise ValueError("x is constant; slope undefined")
        self.slope_ = float((dx * dy).sum() / sxx)
        self.intercept_ = float(y.mean() - self.slope_ * x.mean())
        return self

    def predict(self, x):
        if self.slope_ is None:
            raise RuntimeError("model is not fitted")
        return self.intercept_ + self.slope_ * np.asarray(x, dtype=float)

    def score(self, x, y):
        y = np.asarray(y, dtype=float)
        res = ((y - self.predict(x)) ** 2).sum()
        tot = ((y - y.mean()) ** 2).sum()
        return float(1 - res / tot)
''',
"explanation": r'''
The slope is the centred cross-product over the centred sum of squares of x; the intercept makes
the line pass through the means. Prediction is a vectorised affine map; `score` computes R² from
residuals.
''',
"tests": r'''
import numpy as np

class TestOLS(unittest.TestCase):
    def test_fit(self):
        m = S.SimpleLinearRegression().fit([1, 2, 3, 4], [2, 4, 5, 8])
        self.assertAlmostEqual(m.slope_, 1.9)
        self.assertAlmostEqual(m.intercept_, 0.0)

    def test_predict(self):
        m = S.SimpleLinearRegression().fit([1, 2, 3, 4], [2, 4, 5, 8])
        np.testing.assert_allclose(m.predict([5]), [9.5])

    def test_through_means(self):
        x, y = np.array([0.5, 2, 3.5, 7]), np.array([1, 0, 4, 2.5])
        m = S.SimpleLinearRegression().fit(x, y)
        self.assertAlmostEqual(m.predict([x.mean()])[0], y.mean())

    def test_matches_polyfit(self):
        rng = np.random.default_rng(1)
        x = rng.uniform(0, 10, 50); y = 3 - 0.7 * x + rng.normal(0, 0.5, 50)
        m = S.SimpleLinearRegression().fit(x, y)
        slope, inter = np.polyfit(x, y, 1)
        self.assertAlmostEqual(m.slope_, slope, places=10)
        self.assertAlmostEqual(m.intercept_, inter, places=10)

    def test_score_perfect(self):
        self.assertAlmostEqual(S.SimpleLinearRegression().fit([0, 1, 2], [1, 3, 5]).score([0, 1, 2], [1, 3, 5]), 1.0)

    def test_constant_x(self):
        with self.assertRaises(ValueError):
            S.SimpleLinearRegression().fit([2, 2, 2], [1, 2, 3])

    def test_not_fitted(self):
        with self.assertRaises(RuntimeError):
            S.SimpleLinearRegression().predict([1])
''',
"feedback": [
    ("test_fit", "slope = Σdx·dy / Σdx²; intercept = ȳ − slope·x̄."),
    ("test_matches_polyfit", "Centre x and y before multiplying."),
    ("test_constant_x", "Raise ValueError when Σdx² = 0."),
    ("test_not_fitted", "predict must raise RuntimeError before fit."),
],
},
# ---------------------------------------------------------------- knn-classifier
{
"slug": "knn-classifier", "title": "k-Nearest Neighbors Classifier by Hand", "optional": True,
"difficulty": "intermediate", "prereqs": ["classification-metrics", "pairwise-distances"], "packages": ["numpy"],
"objectives": ["Classify by majority vote of the k nearest training points",
               "Break distance and vote ties deterministically", "See how k trades bias and variance"],
"tags": ["knn", "instance-based-learning", "distance", "classification"],
"sources": ["S012", "S007"], "entry": "knn_predict(X_train, y_train, X_test, k=3)",
"article": r'''
# k-Nearest Neighbours

## Intuition
"Tell me who your neighbours are and I'll tell you who you are." To classify a new point, find
the *k* training points closest to it and take a majority vote of their labels. There is no
training phase beyond storing the data.

## Precise explanation
For each test point $x$:
1. Compute distances to all training points (squared Euclidean distance ranks the same as
   Euclidean, [[pairwise-distances]]).
2. Take the $k$ smallest. Distance ties are broken by lower training index (stable sort).
3. Vote: the most frequent label among the $k$ neighbours.
4. **Vote ties** (e.g. k = 4 with 2–2): choose, among the tied labels, the one whose nearest
   member among the k neighbours is closest (i.e. the first tied label in distance order).

Small k → flexible, noisy boundaries (high variance); large k → smoother boundaries (high bias);
k = n predicts the majority class everywhere. Features should be standardised ([[standard-scaler]]), or large-
scale features dominate distances.

**Corrected from the outline:** classifying by the nearest *class mean* is a different method
(nearest centroid); k-NN votes among actual training points.

## Worked example
Train: (0,0)→A, (1,0)→A, (5,5)→B, (6,5)→B, (5,6)→B. Query (2,1), k = 3: nearest are (1,0) A,
(0,0) A, (5,5) B → A. With k = 5: 3 B vs 2 A → B.

## Common mistakes
* Using `np.argsort` without a stable kind and getting inconsistent tie handling.
* Forgetting to scale features.
* Including the query point itself when evaluating on training data.

## Why this matters
k-NN is a strong baseline, the idea behind retrieval-augmented generation (nearest documents)
and example-based explanations in XAI.
''',
"statement": r'''
Write `knn_predict(X_train, y_train, X_test, k=3)` returning a NumPy array of predicted labels
(integers) for each test row.

* Squared Euclidean distances; neighbours ordered with `np.argsort(d, kind="stable")`.
* Majority vote; vote ties go to the tied label that appears first in the neighbour order.
* Raise `ValueError` unless `1 <= k <= len(X_train)`, or if feature dimensions differ.

**Example**
```python
Xtr = np.array([[0, 0], [1, 0], [5, 5], [6, 5], [5, 6]]); ytr = np.array([0, 0, 1, 1, 1])
knn_predict(Xtr, ytr, np.array([[2, 1]]), k=3)   # array([0])
knn_predict(Xtr, ytr, np.array([[2, 1]]), k=5)   # array([1])
```
''',
"starter": r'''
import numpy as np


def knn_predict(X_train, y_train, X_test, k=3):
    # TODO
    pass
''',
"hints": [
    "Compute the (n_test, n_train) squared-distance matrix with broadcasting ([[pairwise-distances]]).",
    "For each row: `order = np.argsort(d_row, kind='stable')[:k]`; `labels = y_train[order]`.",
    "Count votes in neighbour order; pick the label with the max count, scanning `labels` left to right for ties.",
],
"solution": r'''
import numpy as np


def knn_predict(X_train, y_train, X_test, k=3):
    Xtr = np.asarray(X_train, dtype=float)
    ytr = np.asarray(y_train)
    Xte = np.asarray(X_test, dtype=float)
    if Xtr.ndim != 2 or Xte.ndim != 2 or Xtr.shape[1] != Xte.shape[1]:
        raise ValueError("feature dimensions must match")
    if not 1 <= k <= len(Xtr):
        raise ValueError("k must be between 1 and n_train")
    d = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    preds = []
    for row in d:
        labels = ytr[np.argsort(row, kind="stable")[:k]]
        counts = {}
        for lab in labels:
            counts[lab] = counts.get(lab, 0) + 1
        best = max(counts.values())
        preds.append(next(lab for lab in labels if counts[lab] == best))
    return np.array(preds)
''',
"explanation": r'''
All test–train distances are computed at once. For each test point a stable argsort orders
neighbours (ties by training index); the vote counts labels among the first k, and the first
label in neighbour order reaching the maximum count wins, which implements the nearest-member
tie-break.
''',
"tests": r'''
import numpy as np

XTR = np.array([[0, 0], [1, 0], [5, 5], [6, 5], [5, 6]]); YTR = np.array([0, 0, 1, 1, 1])

class TestKNN(unittest.TestCase):
    def test_k3(self):
        np.testing.assert_array_equal(S.knn_predict(XTR, YTR, np.array([[2, 1]]), k=3), [0])

    def test_k5_majority(self):
        np.testing.assert_array_equal(S.knn_predict(XTR, YTR, np.array([[2, 1]]), k=5), [1])

    def test_k1_training_points(self):
        np.testing.assert_array_equal(S.knn_predict(XTR, YTR, XTR, k=1), YTR)

    def test_vote_tie_nearest_wins(self):
        Xtr = np.array([[0.0], [3.0], [-2.0], [5.0]]); ytr = np.array([1, 0, 1, 0])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[1.0]]), k=4), [1])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[2.0]]), k=4), [0])

    def test_distance_tie_index(self):
        Xtr = np.array([[-1.0], [1.0]]); ytr = np.array([7, 3])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[0.0]]), k=1), [7])

    def test_not_nearest_centroid(self):
        # class-1 centroid is far away (~67), but its member at 2.0 is the nearest point to 1.2
        Xtr = np.array([[0.0], [0.1], [2.0], [100.0], [100.0]]); ytr = np.array([0, 0, 1, 1, 1])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[1.2]]), k=1), [1])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, np.array([[1.2]]), k=3), [0])

    def test_bad_k(self):
        with self.assertRaises(ValueError):
            S.knn_predict(XTR, YTR, XTR, k=6)

    def test_many_queries(self):
        rng = np.random.default_rng(0)
        Xtr = np.vstack([rng.normal(0, 0.5, (30, 2)), rng.normal(4, 0.5, (30, 2))])
        ytr = np.array([0] * 30 + [1] * 30)
        q = np.array([[0, 0], [4, 4], [0.2, -0.3], [3.8, 4.1]])
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, q, k=5), [0, 1, 0, 1])
''',
"feedback": [
    ("test_k5_majority", "Vote among the k nearest *training points*, not class means."),
    ("test_vote_tie_nearest_wins", "On a vote tie pick the tied label that appears first in neighbour (distance) order."),
    ("test_distance_tie_index", "Use np.argsort(..., kind='stable') so equal distances keep training order."),
    ("test_not_nearest_centroid", "Nearest centroid would predict differently here — vote among neighbours."),
],
},
# ---------------------------------------------------------------- linreg-gradient-descent
{
"slug": "linreg-gradient-descent", "title": "Linear Regression by Gradient Descent",
"difficulty": "intermediate", "prereqs": ["least-squares-line", "numerical-gradient"], "packages": ["numpy"],
"objectives": ["Derive the MSE gradient in vector form", "Train with batch gradient descent",
               "Verify against the closed-form solution"],
"tags": ["gradient-descent", "linear-regression", "mse", "vectorisation"],
"sources": ["S013", "S009"], "entry": "mse_grad(X, y, w, b); fit_gd(X, y, lr=0.1, epochs=1000)",
"article": r'''
# Training Linear Regression with Gradient Descent

## Intuition
Closed forms don't exist for most models. Gradient descent ([[gradient-descent-1d]]) works for all differentiable
losses: compute how the loss changes with each weight, step against it, repeat.

## Precise explanation
Model $\hat y = Xw + b$, loss $L = \frac1n\lVert \hat y - y\rVert^2$. With residual
$r = \hat y - y$:
$$\nabla_w L = \frac{2}{n} X^\top r,\qquad \frac{\partial L}{\partial b} = \frac{2}{n}\sum_i r_i.$$
Update: $w \leftarrow w - \eta \nabla_w L$, $b \leftarrow b - \eta\,\partial L/\partial b$.
**Batch** gradient descent uses all rows every step. Standardised features let one learning rate
work for all weights. The result should match `np.linalg.lstsq`.

## Worked example
One feature, x = [0, 1, 2], y = [1, 3, 5], start w = b = 0: r = [−1, −3, −5];
∂w = (2/3)(0·−1 + 1·−3 + 2·−5) = −8.67, ∂b = (2/3)(−9) = −6. With η = 0.1:
w = 0.867, b = 0.6.

## Common mistakes
* Forgetting the factor 2/n (only scales the learning rate, but tests expect the exact gradient).
* `X @ r` instead of `X.T @ r` (shape error or wrong result).
* Learning rate too large → loss explodes ([[gradient-descent-1d]]).

## Why this matters
This loop — forward, loss, gradient, update — is exactly how neural networks (DL), logistic
regression ([[logistic-regression]]) and federated clients ([[local-sgd]]) are trained.
''',
"statement": r'''
Implement:
* `mse_grad(X, y, w, b)` → `(loss, grad_w, grad_b)` for $L = \text{mean}((Xw+b-y)^2)$.
* `fit_gd(X, y, lr=0.1, epochs=1000)` → `(w, b, history)` starting from zeros; `history` holds
  the loss **before** each update (length `epochs`).

Raise `ValueError` for shape mismatches, `lr <= 0` or `epochs < 1`.

**Example**
```python
X = np.array([[0.], [1.], [2.]]); y = np.array([1., 3., 5.])
mse_grad(X, y, np.zeros(1), 0.0)     # (11.666..., array([-8.666...]), -6.0)
w, b, h = fit_gd(X, y, lr=0.1, epochs=2000)   # w ≈ [2.0], b ≈ 1.0
```
''',
"starter": r'''
import numpy as np


def mse_grad(X, y, w, b):
    # TODO
    pass


def fit_gd(X, y, lr=0.1, epochs=1000):
    # TODO
    pass
''',
"hints": [
    "`r = X @ w + b - y`; `loss = np.mean(r ** 2)`.",
    "`grad_w = 2 / n * X.T @ r`, `grad_b = 2 / n * r.sum()`.",
    "In fit_gd append the loss, then update w and b.",
],
"solution": r'''
import numpy as np


def mse_grad(X, y, w, b):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    w = np.asarray(w, dtype=float)
    if X.ndim != 2 or X.shape[0] != y.shape[0] or X.shape[1] != w.shape[0]:
        raise ValueError("shape mismatch")
    n = X.shape[0]
    r = X @ w + b - y
    return float(np.mean(r ** 2)), 2.0 / n * (X.T @ r), float(2.0 / n * r.sum())


def fit_gd(X, y, lr=0.1, epochs=1000):
    if lr <= 0 or epochs < 1:
        raise ValueError("lr must be > 0 and epochs >= 1")
    X = np.asarray(X, dtype=float)
    w = np.zeros(X.shape[1])
    b = 0.0
    history = []
    for _ in range(epochs):
        loss, gw, gb = mse_grad(X, y, w, b)
        history.append(loss)
        w = w - lr * gw
        b = b - lr * gb
    return w, b, history
''',
"explanation": r'''
The residual vector gives both the loss and the gradients in two matrix expressions. The training
loop records the current loss and takes a step against the gradient. For a convex loss with a
suitable learning rate, the parameters converge to the least-squares solution.
''',
"tests": r'''
import numpy as np

X1 = np.array([[0.], [1.], [2.]]); Y1 = np.array([1., 3., 5.])

class TestGDReg(unittest.TestCase):
    def test_grad_values(self):
        loss, gw, gb = S.mse_grad(X1, Y1, np.zeros(1), 0.0)
        self.assertAlmostEqual(loss, 35 / 3)
        np.testing.assert_allclose(gw, [-26 / 3])
        self.assertAlmostEqual(gb, -6.0)

    def test_grad_numerical(self):
        rng = np.random.default_rng(0)
        X, y, w, b = rng.normal(size=(8, 3)), rng.normal(size=8), rng.normal(size=3), 0.3
        _, gw, gb = S.mse_grad(X, y, w, b)
        h = 1e-6
        for j in range(3):
            e = np.zeros(3); e[j] = h
            num = (S.mse_grad(X, y, w + e, b)[0] - S.mse_grad(X, y, w - e, b)[0]) / (2 * h)
            self.assertAlmostEqual(gw[j], num, places=5)
        numb = (S.mse_grad(X, y, w, b + h)[0] - S.mse_grad(X, y, w, b - h)[0]) / (2 * h)
        self.assertAlmostEqual(gb, numb, places=5)

    def test_fit_simple(self):
        w, b, _ = S.fit_gd(X1, Y1, lr=0.1, epochs=2000)
        np.testing.assert_allclose(w, [2.0], atol=1e-6)
        self.assertAlmostEqual(b, 1.0, delta=1e-6)

    def test_matches_lstsq(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(100, 3)); y = X @ np.array([1.5, -2.0, 0.5]) + 0.7 + rng.normal(0, 0.1, 100)
        w, b, _ = S.fit_gd(X, y, lr=0.1, epochs=3000)
        A = np.column_stack([np.ones(100), X])
        sol = np.linalg.lstsq(A, y, rcond=None)[0]
        np.testing.assert_allclose(np.r_[b, w], sol, atol=1e-6)

    def test_history_decreasing(self):
        _, _, h = S.fit_gd(X1, Y1, lr=0.05, epochs=50)
        self.assertEqual(len(h), 50)
        self.assertTrue(all(h[i + 1] <= h[i] for i in range(49)))

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.fit_gd(X1, Y1, lr=0)
        with self.assertRaises(ValueError):
            S.mse_grad(X1, Y1[:2], np.zeros(1), 0.0)
''',
"feedback": [
    ("test_grad_values", "Gradient is (2/n)·Xᵀr with r = Xw + b − y."),
    ("test_grad_numerical", "Compare your analytic gradient with central differences ([[numerical-gradient]])."),
    ("test_history_decreasing", "Record the loss before each update; use minus the gradient."),
    ("test_matches_lstsq", "Update both w and b every epoch."),
],
},
# ---------------------------------------------------------------- logistic-regression
{
"slug": "logistic-regression", "title": "Logistic Regression from Scratch",
"difficulty": "intermediate", "prereqs": ["linreg-gradient-descent", "sigmoid-function"], "packages": ["numpy"],
"objectives": ["Implement a numerically stable sigmoid and log-loss", "Derive the log-loss gradient (p − y)",
               "Train and threshold a binary classifier"],
"tags": ["logistic-regression", "log-loss", "sigmoid", "classification"],
"sources": ["S012", "S013"], "entry": "sigmoid(z); log_loss(y, p); class LogisticRegression",
"article": r'''
# Logistic Regression

## Intuition
To predict a probability, squash a linear score into (0, 1) with the S-shaped **sigmoid**. Train
by rewarding confident correct predictions and heavily penalising confident wrong ones.

## Precise explanation
$p = \sigma(z) = \frac{1}{1+e^{-z}}$, $z = Xw + b$.
**Log-loss (binary cross-entropy):**
$$L = -\frac1n\sum \big[y\log p + (1-y)\log(1-p)\big].$$
Its gradient is remarkably simple: $\nabla_w L = \frac1n X^\top (p - y)$,
$\partial L/\partial b = \frac1n\sum (p-y)$.

**Numerical stability:** for $z = -1000$, `np.exp(1000)` overflows. A stable sigmoid uses
$e^{-|z|}$: for $z\ge0$, $1/(1+e^{-z})$; for $z<0$, $e^{z}/(1+e^{z})$. Clip $p$ into
$[\epsilon, 1-\epsilon]$ before taking logs (ε = 1e−12) so $\log 0$ never occurs.

Predict class 1 when $p \ge 0.5$ (threshold adjustable). The decision boundary $Xw + b = 0$ is
linear.

## Worked example
w = [2], b = −1, x = 1: z = 1, p = 0.731; if y = 1 the loss is −log 0.731 = 0.313.

## Common mistakes
* Using MSE for classification (non-convex with sigmoid, slow learning).
* Overflow warnings from a naive sigmoid.
* `log(0)` → −inf loss.

## Why this matters
Logistic regression is the standard baseline classifier and is exactly a one-neuron network with
sigmoid output — the bridge to Deep Learning.
''',
"statement": r'''
Implement:
* `sigmoid(z)` — stable, works on scalars and arrays, no overflow warnings for |z| up to 1e4.
* `log_loss(y, p, eps=1e-12)` — mean binary cross-entropy with clipping.
* `class LogisticRegression(lr=0.1, epochs=1000)` with `fit(X, y)` (batch GD from zeros, stores
  `w_`, `b_`, `history_` of losses before each update), `predict_proba(X)`,
  `predict(X, threshold=0.5)` (ints 0/1). Raise `ValueError` if `y` contains values other than 0/1.

**Example**
```python
sigmoid(np.array([-1000., 0., 1000.]))   # [0., 0.5, 1.]
log_loss([1, 0], [0.9, 0.1])             # 0.10536...
```
''',
"starter": r'''
import numpy as np


def sigmoid(z):
    # TODO
    pass


def log_loss(y, p, eps=1e-12):
    # TODO
    pass


class LogisticRegression:
    def __init__(self, lr=0.1, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.w_ = None
        self.b_ = None
        self.history_ = []

    def fit(self, X, y):
        # TODO
        return self

    def predict_proba(self, X):
        # TODO
        pass

    def predict(self, X, threshold=0.5):
        # TODO
        pass
''',
"hints": [
    "Stable sigmoid: `e = np.exp(-np.abs(z)); np.where(z >= 0, 1/(1+e), e/(1+e))`.",
    "Clip: `p = np.clip(p, eps, 1 - eps)` before logs.",
    "Gradient: `g = (p - y)`; `w -= lr * X.T @ g / n`; `b -= lr * g.mean()`.",
],
"solution": r'''
import numpy as np


def sigmoid(z):
    z = np.asarray(z, dtype=float)
    e = np.exp(-np.abs(z))
    out = np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))
    return out if out.ndim else float(out)


def log_loss(y, p, eps=1e-12):
    y = np.asarray(y, dtype=float)
    p = np.clip(np.asarray(p, dtype=float), eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


class LogisticRegression:
    def __init__(self, lr=0.1, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.w_ = None
        self.b_ = None
        self.history_ = []

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if not np.isin(y, (0, 1)).all():
            raise ValueError("y must contain only 0 and 1")
        n, d = X.shape
        self.w_, self.b_, self.history_ = np.zeros(d), 0.0, []
        for _ in range(self.epochs):
            p = sigmoid(X @ self.w_ + self.b_)
            self.history_.append(log_loss(y, p))
            g = p - y
            self.w_ = self.w_ - self.lr * (X.T @ g) / n
            self.b_ = self.b_ - self.lr * float(g.mean())
        return self

    def predict_proba(self, X):
        return sigmoid(np.asarray(X, dtype=float) @ self.w_ + self.b_)

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)
''',
"explanation": r'''
The sigmoid only ever exponentiates a non-positive number, so it cannot overflow. Clipping keeps
the logs finite. The log-loss gradient with respect to the linear score is p − y, so training is
the same loop as [[linreg-gradient-descent]] with a different output function.
''',
"tests": r'''
import warnings
import numpy as np

class TestLogReg(unittest.TestCase):
    def test_sigmoid_extremes(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            np.testing.assert_allclose(S.sigmoid(np.array([-1000., 0., 1000.])), [0, 0.5, 1], atol=1e-300)

    def test_sigmoid_scalar(self):
        self.assertAlmostEqual(S.sigmoid(1.0), 1 / (1 + np.exp(-1)))

    def test_sigmoid_symmetry(self):
        z = np.linspace(-20, 20, 41)
        np.testing.assert_allclose(S.sigmoid(z) + S.sigmoid(-z), 1.0, atol=1e-12)

    def test_log_loss(self):
        self.assertAlmostEqual(S.log_loss([1, 0], [0.9, 0.1]), -np.log(0.9))

    def test_log_loss_clipped(self):
        self.assertTrue(np.isfinite(S.log_loss([1], [0.0])))

    def test_fit_separable(self):
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(-2, 1, (50, 2)), rng.normal(2, 1, (50, 2))])
        y = np.array([0] * 50 + [1] * 50)
        m = S.LogisticRegression(lr=0.5, epochs=500).fit(X, y)
        self.assertGreaterEqual((m.predict(X) == y).mean(), 0.97)
        self.assertLess(m.history_[-1], m.history_[0])

    def test_first_step(self):
        X = np.array([[1.0], [-1.0]]); y = np.array([1, 0])
        m = S.LogisticRegression(lr=1.0, epochs=1).fit(X, y)
        np.testing.assert_allclose(m.w_, [0.5])
        self.assertAlmostEqual(m.b_, 0.0)
        self.assertAlmostEqual(m.history_[0], np.log(2))

    def test_bad_labels(self):
        with self.assertRaises(ValueError):
            S.LogisticRegression().fit(np.ones((2, 1)), np.array([0, 2]))
''',
"feedback": [
    ("test_sigmoid_extremes", "Use exp(-|z|) so the exponent is never positive."),
    ("test_first_step", "Gradient is Xᵀ(p − y)/n; with w = 0, p = 0.5 for all rows."),
    ("test_log_loss_clipped", "Clip p to [eps, 1 − eps] before log."),
    ("test_fit_separable", "Update w and b every epoch and record history_ before the update."),
],
},
# ---------------------------------------------------------------- kmeans
{
"slug": "kmeans", "title": "k-Means Clustering by Hand", "optional": True,
"difficulty": "advanced", "prereqs": ["knn-classifier"], "packages": ["numpy"],
"objectives": ["Alternate assignment and update steps", "Handle empty clusters and convergence",
               "Compute inertia (within-cluster sum of squares)"],
"tags": ["clustering", "kmeans", "unsupervised-learning", "lloyd-algorithm"],
"sources": ["S012"], "entry": "kmeans(X, init_centroids, max_iter=100, tol=1e-9)",
"article": r'''
# k-Means

## Intuition
Place k "centres", give each point to its nearest centre, move each centre to the average of its
points, repeat. Groups of similar points emerge without any labels — **unsupervised** learning.

## Precise explanation
Lloyd's algorithm minimises **inertia** $J = \sum_i \lVert x_i - \mu_{c(i)}\rVert^2$:
1. **Assign:** $c(i) = \arg\min_j \lVert x_i - \mu_j\rVert^2$ (lowest index on ties).
2. **Update:** $\mu_j$ = mean of points assigned to $j$. If a cluster is empty, keep its old
   centroid (one common policy).
3. Stop when centroids move less than `tol` (max squared shift) or after `max_iter` iterations.
Each step never increases $J$, so the algorithm converges — but only to a *local* optimum that
depends on initialisation (k-means++ or several restarts help). Passing initial centroids
explicitly makes runs deterministic.

```mermaid
flowchart LR
  I[initial centroids] --> A[assign points to nearest]
  A --> U[move centroids to means]
  U --> C{moved < tol?}
  C -- no --> A
  C -- yes --> D[done]
```

## Worked example
X = [0, 1, 10, 11] (1-D), init [0, 1]: assign → {0}, {1, 10, 11}; update → 0, 7.33; assign →
{0, 1}, {10, 11}; update → 0.5, 10.5; stable. Inertia = 4 × 0.25 = 1.0.

## Common mistakes
* Recomputing distances with the *new* centroids before assigning (mixing steps).
* Dividing by zero for empty clusters.
* Comparing labels across runs: cluster ids are arbitrary.

## Why this matters
Clustering segments users, compresses colours (vector quantisation), initialises mixture models,
and illustrates the alternating-optimisation pattern used across ML.
''',
"statement": r'''
Write `kmeans(X, init_centroids, max_iter=100, tol=1e-9)` returning a dict
`{"centroids": (k, d) array, "labels": (n,) int array, "inertia": float, "n_iter": int}`.

* Each iteration: assign (argmin squared distance, lowest index on ties), then update means
  (empty clusters keep their previous centroid). `n_iter` counts completed iterations.
* Stop after an iteration whose maximum squared centroid shift is `<= tol`.
* Final `labels` and `inertia` correspond to the returned centroids.
* Raise `ValueError` on dimension mismatch or `k > n`.

**Example**
```python
r = kmeans(np.array([[0.], [1.], [10.], [11.]]), np.array([[0.], [1.]]))
r["centroids"].ravel()   # [ 0.5, 10.5]
r["labels"]              # [0, 0, 1, 1]
r["inertia"]             # 1.0
```
''',
"starter": r'''
import numpy as np


def kmeans(X, init_centroids, max_iter=100, tol=1e-9):
    # TODO
    pass
''',
"hints": [
    "Distances: `((X[:, None, :] - C[None, :, :]) ** 2).sum(-1)`; labels = `argmin(axis=1)`.",
    "New centroid j = `X[labels == j].mean(axis=0)` if any points, else old `C[j]`.",
    "After the loop, recompute labels and inertia for the final centroids.",
],
"solution": r'''
import numpy as np


def _assign(X, C):
    d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)
    labels = d.argmin(axis=1)
    return labels, float(d[np.arange(len(X)), labels].sum())


def kmeans(X, init_centroids, max_iter=100, tol=1e-9):
    X = np.asarray(X, dtype=float)
    C = np.array(init_centroids, dtype=float)
    if X.ndim != 2 or C.ndim != 2 or X.shape[1] != C.shape[1]:
        raise ValueError("dimension mismatch")
    if C.shape[0] > X.shape[0]:
        raise ValueError("k cannot exceed n")
    n_iter = 0
    for _ in range(max_iter):
        labels, _ = _assign(X, C)
        newC = C.copy()
        for j in range(C.shape[0]):
            members = X[labels == j]
            if len(members):
                newC[j] = members.mean(axis=0)
        shift = float(((newC - C) ** 2).sum(axis=1).max())
        C = newC
        n_iter += 1
        if shift <= tol:
            break
    labels, inertia = _assign(X, C)
    return {"centroids": C, "labels": labels, "inertia": inertia, "n_iter": n_iter}
''',
"explanation": r'''
Each iteration performs one assignment step and one update step. Empty clusters keep their
previous centre, avoiding NaN. Convergence is detected by the largest squared centroid movement.
A final assignment makes labels and inertia consistent with the returned centroids.
''',
"tests": r'''
import numpy as np

class TestKMeans(unittest.TestCase):
    def test_1d(self):
        r = S.kmeans(np.array([[0.], [1.], [10.], [11.]]), np.array([[0.], [1.]]))
        np.testing.assert_allclose(r["centroids"].ravel(), [0.5, 10.5])
        np.testing.assert_array_equal(r["labels"], [0, 0, 1, 1])
        self.assertAlmostEqual(r["inertia"], 1.0)

    def test_n_iter(self):
        r = S.kmeans(np.array([[0.], [1.], [10.], [11.]]), np.array([[0.], [1.]]))
        self.assertEqual(r["n_iter"], 3)

    def test_blobs(self):
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(0, 0.3, (40, 2)), rng.normal(5, 0.3, (40, 2))])
        r = S.kmeans(X, X[[0, 79]])
        self.assertEqual(len(set(r["labels"][:40])), 1)
        self.assertEqual(len(set(r["labels"][40:])), 1)

    def test_empty_cluster_kept(self):
        r = S.kmeans(np.array([[0.], [0.2]]), np.array([[0.], [100.]]))
        np.testing.assert_allclose(r["centroids"].ravel(), [0.1, 100.0])

    def test_inertia_matches(self):
        rng = np.random.default_rng(3)
        X = rng.normal(size=(30, 3))
        r = S.kmeans(X, X[:3])
        C, lab = r["centroids"], r["labels"]
        self.assertAlmostEqual(r["inertia"], float(((X - C[lab]) ** 2).sum()), places=10)

    def test_monotone_with_iterations(self):
        rng = np.random.default_rng(4)
        X = rng.normal(size=(50, 2))
        inert = [S.kmeans(X, X[:4], max_iter=m)["inertia"] for m in (1, 2, 5, 50)]
        self.assertTrue(all(inert[i + 1] <= inert[i] + 1e-12 for i in range(3)))

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.kmeans(np.zeros((2, 2)), np.zeros((3, 2)))
''',
"feedback": [
    ("test_1d", "Assign with the current centroids, then move each centroid to its members' mean."),
    ("test_empty_cluster_kept", "If no points are assigned, keep the old centroid."),
    ("test_inertia_matches", "Recompute labels and inertia after the final update."),
    ("test_n_iter", "Count iterations and stop when the max squared shift <= tol."),
],
},
# ---------------------------------------------------------------- k-fold-cv
{
"slug": "k-fold-cv", "title": "k-Fold Cross-Validation by Hand", "optional": True,
"difficulty": "advanced", "prereqs": ["polynomial-overfitting"], "packages": ["numpy"],
"objectives": ["Create k disjoint folds", "Train/evaluate k times and aggregate",
               "Use CV to choose a hyperparameter"],
"tags": ["cross-validation", "model-selection", "folds"],
"sources": ["S012"], "entry": "kfold_indices(n, k, seed=None); cross_val_score(fit, score, X, y, k=5, seed=0)",
"article": r'''
# k-Fold Cross-Validation

## Intuition
One train/test split gives one noisy estimate. Cross-validation rotates: split the data into k
folds, train on k − 1 of them and test on the remaining one, k times. Every example is tested
exactly once.

## Precise explanation
* Shuffle indices (if seeded) and split them into k nearly equal folds: the first `n % k` folds
  get one extra element (same convention as `np.array_split`).
* For fold i: test = fold i, train = all others.
* Report the mean (and spread) of the k scores.
* Use CV on the **training** data to pick hyperparameters (k in k-NN, λ in ridge); keep the test
  set for the final estimate.

| fold | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| round 1 | test | train | train | train | train |
| round 2 | train | test | train | train | train |
| … | | | | | |

## Worked example
n = 7, k = 3 → fold sizes 3, 2, 2: [0,1,2], [3,4], [5,6] (without shuffling).

## Common mistakes
* Overlapping folds or leaving examples out.
* Preprocessing (scaling) on all data before CV — fit inside each training fold.
* Using CV scores of the tuned model as the final unbiased estimate.

## Why this matters
CV is the standard way to compare models and tune hyperparameters on small datasets.
''',
"statement": r'''
Implement:
* `kfold_indices(n, k, seed=None)` → list of `k` `(train_idx, test_idx)` pairs. If `seed` is not
  None, shuffle with `np.random.default_rng(seed).permutation(n)`; otherwise use `0..n-1`. Split
  with `np.array_split(order, k)`. Raise `ValueError` unless `2 <= k <= n`.
* `cross_val_score(fit, score, X, y, k=5, seed=0)` → NumPy array of k scores, where
  `model = fit(X_train, y_train)` and `score(model, X_test, y_test)` returns a float.

**Example**
```python
[t.tolist() for _, t in kfold_indices(7, 3)]   # [[0, 1, 2], [3, 4], [5, 6]]
```
''',
"starter": r'''
import numpy as np


def kfold_indices(n, k, seed=None):
    # TODO
    return []


def cross_val_score(fit, score, X, y, k=5, seed=0):
    # TODO
    pass
''',
"hints": [
    "`order = np.arange(n)` or the seeded permutation; `folds = np.array_split(order, k)`.",
    "Train indices for fold i: `np.concatenate([f for j, f in enumerate(folds) if j != i])`.",
    "Loop over folds calling fit and score, collecting scores into an array.",
],
"solution": r'''
import numpy as np


def kfold_indices(n, k, seed=None):
    if not 2 <= k <= n:
        raise ValueError("k must satisfy 2 <= k <= n")
    order = np.arange(n) if seed is None else np.random.default_rng(seed).permutation(n)
    folds = np.array_split(order, k)
    pairs = []
    for i in range(k):
        train = np.concatenate([f for j, f in enumerate(folds) if j != i])
        pairs.append((train, folds[i]))
    return pairs


def cross_val_score(fit, score, X, y, k=5, seed=0):
    X = np.asarray(X)
    y = np.asarray(y)
    scores = []
    for tr, te in kfold_indices(len(X), k, seed):
        model = fit(X[tr], y[tr])
        scores.append(float(score(model, X[te], y[te])))
    return np.array(scores)
''',
"explanation": r'''
`array_split` produces k nearly equal folds; each fold serves once as the test set while the
others are concatenated for training. `cross_val_score` is model-agnostic: it only needs a fit
function and a score function, so any model in this topic can be evaluated.
''',
"tests": r'''
import numpy as np

def fit_mean(X, y):
    return float(np.mean(y))

def neg_mse(m, X, y):
    return -float(np.mean((y - m) ** 2))

class TestCV(unittest.TestCase):
    def test_sizes(self):
        self.assertEqual([t.tolist() for _, t in S.kfold_indices(7, 3)], [[0, 1, 2], [3, 4], [5, 6]])

    def test_partition(self):
        pairs = S.kfold_indices(23, 5, seed=1)
        tests = np.concatenate([t for _, t in pairs])
        self.assertEqual(sorted(tests.tolist()), list(range(23)))
        for tr, te in pairs:
            self.assertEqual(len(set(tr) & set(te)), 0)
            self.assertEqual(len(tr) + len(te), 23)

    def test_seeded_recipe(self):
        perm = np.random.default_rng(4).permutation(10)
        np.testing.assert_array_equal(S.kfold_indices(10, 2, seed=4)[0][1], perm[:5])

    def test_bad_k(self):
        with self.assertRaises(ValueError):
            S.kfold_indices(3, 4)
        with self.assertRaises(ValueError):
            S.kfold_indices(3, 1)

    def test_cv_score_count(self):
        s = S.cross_val_score(fit_mean, neg_mse, np.zeros((10, 1)), np.arange(10.0), k=5)
        self.assertEqual(s.shape, (5,))

    def test_cv_values(self):
        y = np.array([1.0, 1.0, 3.0, 3.0])
        s = S.cross_val_score(fit_mean, neg_mse, np.zeros((4, 1)), y, k=2, seed=None)
        np.testing.assert_allclose(s, [-4.0, -4.0])

    def test_model_selection(self):
        rng = np.random.default_rng(0)
        X = rng.uniform(-1, 1, (60, 1)); y = 3 * X[:, 0] + rng.normal(0, 0.1, 60)
        fit_lin = lambda X, y: np.polyfit(X[:, 0], y, 1)
        sc_lin = lambda m, X, y: -float(np.mean((np.polyval(m, X[:, 0]) - y) ** 2))
        self.assertGreater(S.cross_val_score(fit_lin, sc_lin, X, y).mean(),
                           S.cross_val_score(fit_mean, neg_mse, X, y).mean())
''',
"feedback": [
    ("test_sizes", "Use np.array_split so the first n % k folds are one larger."),
    ("test_partition", "Each index must appear in exactly one test fold; train = all other folds."),
    ("test_seeded_recipe", "Shuffle with default_rng(seed).permutation(n) only when seed is not None."),
    ("test_cv_values", "Call fit on the training fold and score on the test fold."),
],
},
# ---------------------------------------------------------------- decision-stump-gini
{
"slug": "decision-stump-gini", "title": "Decision Stump with Gini Impurity",
"difficulty": "advanced", "prereqs": ["classification-metrics"], "packages": ["numpy"],
"objectives": ["Compute Gini impurity", "Search thresholds at midpoints between sorted unique values",
               "Choose the split with the lowest weighted impurity"],
"tags": ["decision-trees", "gini", "splitting", "greedy-search"],
"sources": ["S012", "S024"], "entry": "gini(y); best_split(X, y)",
"article": r'''
# Decision Stumps and Gini Impurity

## Intuition
A decision tree asks yes/no questions ("is age < 30?"). A **stump** asks one. The best question
splits the data into groups that are as *pure* (single-class) as possible.

## Precise explanation
**Gini impurity** of labels with class proportions $p_c$: $G = 1 - \sum_c p_c^2$. Pure → 0;
50/50 binary → 0.5.
For a split into left (L) and right (R):
$$G_\text{split} = \frac{n_L}{n} G(L) + \frac{n_R}{n} G(R).$$
**Candidate thresholds:** for each feature, midpoints between consecutive *distinct* sorted
values. Rule: go left if $x_j \le t$.
**Search:** try every feature and threshold; keep the lowest $G_\text{split}$. Ties → lowest
feature index, then lowest threshold. Leaves predict their majority class (ties → smaller label).

```mermaid
flowchart TD
  R{"x_j ≤ t ?"} -- yes --> L["left leaf: majority class"]
  R -- no --> Rt["right leaf: majority class"]
```

## Worked example
x = [1, 2, 3, 4], y = [0, 0, 1, 1]: thresholds 1.5, 2.5, 3.5. At 2.5 both sides are pure →
G = 0. Best split: feature 0, t = 2.5, left 0, right 1.

## Common mistakes
* Using raw values as thresholds (≤ on the largest value sends everything left).
* Forgetting to weight child impurities by size.
* Considering thresholds between duplicate values (no-op splits).

## Why this matters
Stumps are the weak learners in boosting; trees and forests are stacked stumps, and their
decision paths are inherently interpretable ([[decision-path]]).
''',
"statement": r'''
Implement:
* `gini(y)` → Gini impurity of a 1-D integer label array (0.0 for empty).
* `best_split(X, y)` → dict `{"feature": int, "threshold": float, "impurity": float,
  "left_class": int, "right_class": int}` using the rules above. If no feature has two distinct
  values, raise `ValueError`.

**Examples**
```python
gini(np.array([0, 0, 1, 1]))     # 0.5
best_split(np.array([[1], [2], [3], [4]]), np.array([0, 0, 1, 1]))
# {'feature': 0, 'threshold': 2.5, 'impurity': 0.0, 'left_class': 0, 'right_class': 1}
```
''',
"starter": r'''
import numpy as np


def gini(y):
    # TODO
    pass


def best_split(X, y):
    # TODO
    pass
''',
"hints": [
    "`_, counts = np.unique(y, return_counts=True); p = counts / len(y); 1 - (p**2).sum()`.",
    "Thresholds: `u = np.unique(X[:, j]); (u[:-1] + u[1:]) / 2`.",
    "Use strict `<` when comparing impurities so the first (lowest feature/threshold) best is kept.",
],
"solution": r'''
import numpy as np


def gini(y):
    y = np.asarray(y)
    if y.size == 0:
        return 0.0
    _, counts = np.unique(y, return_counts=True)
    p = counts / y.size
    return float(1.0 - (p ** 2).sum())


def _majority(y):
    vals, counts = np.unique(y, return_counts=True)
    return int(vals[np.argmax(counts)])


def best_split(X, y):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    n = len(y)
    best = None
    for j in range(X.shape[1]):
        u = np.unique(X[:, j])
        for t in (u[:-1] + u[1:]) / 2:
            left = X[:, j] <= t
            yl, yr = y[left], y[~left]
            g = (len(yl) * gini(yl) + len(yr) * gini(yr)) / n
            if best is None or g < best["impurity"] - 1e-15:
                best = {"feature": j, "threshold": float(t), "impurity": float(g),
                        "left_class": _majority(yl), "right_class": _majority(yr)}
    if best is None:
        raise ValueError("no feature can be split")
    return best
''',
"explanation": r'''
Gini comes from class proportions. The search scans features in order and thresholds in
increasing order, keeping a candidate only if it is strictly better, which implements the
tie-breaking rule. `np.unique` with `argmax` picks the smallest label among majority ties.
''',
"tests": r'''
import numpy as np

class TestStump(unittest.TestCase):
    def test_gini(self):
        self.assertAlmostEqual(S.gini(np.array([0, 0, 1, 1])), 0.5)
        self.assertEqual(S.gini(np.array([2, 2, 2])), 0.0)
        self.assertAlmostEqual(S.gini(np.array([0, 1, 2])), 2 / 3)
        self.assertEqual(S.gini(np.array([], dtype=int)), 0.0)

    def test_perfect(self):
        self.assertEqual(S.best_split(np.array([[1], [2], [3], [4]]), np.array([0, 0, 1, 1])),
                         {"feature": 0, "threshold": 2.5, "impurity": 0.0, "left_class": 0, "right_class": 1})

    def test_second_feature(self):
        X = np.array([[5, 1], [5, 2], [5, 8], [5, 9]]); y = np.array([1, 1, 0, 0])
        r = S.best_split(X, y)
        self.assertEqual((r["feature"], r["threshold"], r["left_class"], r["right_class"]), (1, 5.0, 1, 0))

    def test_weighted_impurity(self):
        X = np.array([[1], [2], [3], [4], [5]]); y = np.array([0, 0, 1, 0, 1])
        r = S.best_split(X, y)
        self.assertAlmostEqual(r["impurity"], 4 / 15)
        self.assertEqual(r["threshold"], 2.5)

    def test_tie_lowest_feature(self):
        X = np.array([[1, 1], [2, 2]]); y = np.array([0, 1])
        self.assertEqual(S.best_split(X, y)["feature"], 0)

    def test_duplicates_midpoints(self):
        X = np.array([[1], [1], [3], [3]]); y = np.array([0, 0, 1, 1])
        self.assertEqual(S.best_split(X, y)["threshold"], 2.0)

    def test_unsplittable(self):
        with self.assertRaises(ValueError):
            S.best_split(np.array([[1], [1]]), np.array([0, 1]))
''',
"feedback": [
    ("test_weighted_impurity", "Weight each child's Gini by its share of samples."),
    ("test_duplicates_midpoints", "Thresholds are midpoints between consecutive *unique* values."),
    ("test_tie_lowest_feature", "Only replace the best split when strictly better."),
    ("test_gini", "Gini = 1 − Σ p_c²; return 0 for empty input."),
],
},
# ---------------------------------------------------------------- ridge-regression
{
"slug": "ridge-regression", "title": "Ridge Regression (Closed Form)", "optional": True,
"difficulty": "advanced", "prereqs": ["k-fold-cv", "standard-scaler"], "packages": ["numpy"],
"objectives": ["Add L2 regularisation to least squares", "Leave the intercept unpenalised via centring",
               "Observe shrinkage and stability with collinear features"],
"tags": ["regularisation", "ridge", "l2", "bias-variance"],
"sources": ["S012", "S009"], "entry": "class Ridge(alpha=1.0): fit, predict",
"article": r'''
# Ridge Regression

## Intuition
When features are nearly duplicates, ordinary least squares can produce wild coefficients that
cancel each other (+500 and −499). Ridge regression adds a penalty on large weights, preferring
smaller, more stable coefficients — trading a little bias for much less variance.

## Precise explanation
Minimise $\lVert y - Xw - b\rVert^2 + \alpha \lVert w\rVert^2$ ($\alpha \ge 0$). The intercept is
**not** penalised. Centre the data ($X_c = X - \bar X$, $y_c = y - \bar y$), then
$$w = (X_c^\top X_c + \alpha I)^{-1} X_c^\top y_c,\qquad b = \bar y - \bar X w.$$
Solve with `np.linalg.solve`, not an explicit inverse. For $\alpha > 0$ the matrix is always
invertible, even with perfectly collinear features. $\alpha = 0$ recovers OLS; as $\alpha \to
\infty$, $w \to 0$ and predictions → $\bar y$. Choose α by cross-validation ([[k-fold-cv]]).

## Worked example
Two identical columns x and x, y = 2x: OLS is singular (any w₁ + w₂ = 2 works); ridge with small
α gives the symmetric solution w ≈ [1, 1].

## Common mistakes
* Penalising the intercept (adding α to the bias term).
* Not scaling features — the penalty then depends on units.
* Using `np.linalg.inv` (less stable).

## Why this matters
L2 regularisation (weight decay) is used in almost every neural network; ridge is the cleanest
place to see the bias–variance trade-off.
''',
"statement": r'''
Implement `class Ridge(alpha=1.0)` with `coef_` (shape `(d,)`) and `intercept_` (float):
* `fit(X, y)` — centred closed form above, solved with `np.linalg.solve`; returns `self`.
  Raise `ValueError` if `alpha < 0`. (With `alpha == 0` and singular `X_c^T X_c`,
  `np.linalg.solve` may raise `LinAlgError`; that is acceptable.)
* `predict(X)`; raise `RuntimeError` before fit.

**Example**
```python
X = np.array([[1., 1.], [2., 2.], [3., 3.]]); y = np.array([2., 4., 6.])
Ridge(alpha=1e-6).fit(X, y).coef_    # ≈ [1., 1.]  (collinear columns share the weight)
```
''',
"starter": r'''
import numpy as np


class Ridge:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        # TODO
        return self

    def predict(self, X):
        # TODO
        pass
''',
"hints": [
    "`xm, ym = X.mean(axis=0), y.mean()`; `Xc, yc = X - xm, y - ym`.",
    "`A = Xc.T @ Xc + alpha * np.eye(d)`; `w = np.linalg.solve(A, Xc.T @ yc)`.",
    "`intercept = ym - xm @ w`.",
],
"solution": r'''
import numpy as np


class Ridge:
    def __init__(self, alpha=1.0):
        self.alpha = alpha
        self.coef_ = None
        self.intercept_ = None

    def fit(self, X, y):
        if self.alpha < 0:
            raise ValueError("alpha must be >= 0")
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        xm, ym = X.mean(axis=0), y.mean()
        Xc, yc = X - xm, y - ym
        A = Xc.T @ Xc + self.alpha * np.eye(X.shape[1])
        self.coef_ = np.linalg.solve(A, Xc.T @ yc)
        self.intercept_ = float(ym - xm @ self.coef_)
        return self

    def predict(self, X):
        if self.coef_ is None:
            raise RuntimeError("model is not fitted")
        return np.asarray(X, dtype=float) @ self.coef_ + self.intercept_
''',
"explanation": r'''
Centring removes the intercept from the penalised problem; the α·I term makes the system
well-conditioned. The intercept is recovered from the means so that the fitted plane passes
through (X̄, ȳ).
''',
"tests": r'''
import numpy as np

class TestRidge(unittest.TestCase):
    def test_collinear(self):
        X = np.array([[1., 1.], [2., 2.], [3., 3.]]); y = np.array([2., 4., 6.])
        np.testing.assert_allclose(S.Ridge(alpha=1e-6).fit(X, y).coef_, [1, 1], atol=1e-5)

    def test_alpha0_is_ols(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(40, 3)); y = X @ [1., -2., 3.] + 5 + rng.normal(0, 0.1, 40)
        m = S.Ridge(alpha=0.0).fit(X, y)
        sol = np.linalg.lstsq(np.column_stack([np.ones(40), X]), y, rcond=None)[0]
        np.testing.assert_allclose(np.r_[m.intercept_, m.coef_], sol, atol=1e-10)

    def test_shrinkage(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(50, 4)); y = X @ [3., -1., 2., 0.5] + rng.normal(0, 0.5, 50)
        norms = [np.linalg.norm(S.Ridge(alpha=a).fit(X, y).coef_) for a in (0.0, 1.0, 10.0, 1000.0)]
        self.assertTrue(all(norms[i + 1] < norms[i] for i in range(3)))

    def test_large_alpha_predicts_mean(self):
        X = np.array([[0.], [1.], [2.]]); y = np.array([1., 2., 6.])
        np.testing.assert_allclose(S.Ridge(alpha=1e12).fit(X, y).predict(X), y.mean(), atol=1e-6)

    def test_intercept_not_penalised(self):
        X = np.array([[0.], [0.], [0.]]); y = np.array([10., 10., 10.])
        m = S.Ridge(alpha=100.0).fit(X, y)
        self.assertAlmostEqual(m.intercept_, 10.0)

    def test_closed_form(self):
        X = np.array([[1., 0.], [0., 1.], [1., 1.]]); y = np.array([1., 2., 4.])
        m = S.Ridge(alpha=2.0).fit(X, y)
        Xc, yc = X - X.mean(0), y - y.mean()
        np.testing.assert_allclose(m.coef_, np.linalg.solve(Xc.T @ Xc + 2 * np.eye(2), Xc.T @ yc))

    def test_errors(self):
        with self.assertRaises(ValueError):
            S.Ridge(alpha=-1).fit(np.ones((2, 1)), np.ones(2))
        with self.assertRaises(RuntimeError):
            S.Ridge().predict(np.ones((1, 1)))
''',
"feedback": [
    ("test_intercept_not_penalised", "Centre X and y; compute the intercept from the means."),
    ("test_shrinkage", "Add alpha·I to Xcᵀ Xc (not to the whole design matrix with a bias column)."),
    ("test_collinear", "Use np.linalg.solve on (XcᵀXc + αI)."),
    ("test_alpha0_is_ols", "With alpha = 0 you should recover ordinary least squares."),
],
},
]
