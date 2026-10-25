"""Library comparisons attached to packs that were written before the 2026-10 revision.

LIBRARY maps a slug to {"text": markdown, "tests": unittest code, "optional": [packages]}. The
builder appends "text" to the lesson as "## Library implementation" and "tests" to tests.py.
Comparisons that need a package outside the course's permitted packages are skipped when that
package is not installed, so core grading never depends on it.
"""

SKLEARN = '''
try:
    import sklearn  # noqa: F401
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False
'''

SCIPY = '''
try:
    import scipy  # noqa: F401
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False
'''

TORCH = '''
try:
    import torch
except ImportError:
    torch = None
'''

LIBRARY = {
# ======================================================================== Python
"sum-and-mean": {
"text": r'''
Python's built-in `sum(nums)` performs the same accumulation, and `statistics.fmean(nums)`
computes the mean (it raises `StatisticsError` for empty data instead of returning `None`).
You will import modules properly in [[standard-library]]; the comparison below already uses them.
''',
"tests": r'''
import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_builtins(self):
        data = [3, -1.5, 8, 0.25, 4]
        total, mean = S.sum_and_mean(data)
        self.assertAlmostEqual(total, sum(data))
        self.assertAlmostEqual(mean, statistics.fmean(data))
''',
},
"unique-words": {
"text": r'''
Since Python 3.7 dictionaries keep insertion order, so `list(dict.fromkeys(words))` removes
duplicates while keeping first occurrences — a common one-line idiom once the words are
normalised. The set-plus-list loop makes the idea explicit; the test checks both agree.
''',
"tests": r'''
import string


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_dict_fromkeys(self):
        text = "The cat; the CAT and a dog, a Dog!"
        words = [w.strip(string.punctuation).lower() for w in text.split()]
        self.assertEqual(S.unique_words(text), list(dict.fromkeys(w for w in words if w)))
''',
},
"factorial-validated": {
"text": r'''
`math.factorial(n)` computes the same value (and also raises `ValueError` for negative
numbers and `TypeError` for floats). It is implemented in C and uses a faster
divide-and-conquer product for large `n`, but the result is identical.
''',
"tests": r'''
class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_math_factorial(self):
        for n in (0, 1, 5, 20, 100):
            self.assertEqual(S.factorial(n), math.factorial(n))
''',
},
"matrix-transpose": {
"text": r'''
The idiomatic transpose of a rectangular list of lists is `[list(row) for row in zip(*matrix)]`:
`zip(*matrix)` passes every row as a separate argument and yields one tuple per column. It does
not validate ragged input (it silently stops at the shortest row), which is why the exercise asks
for explicit checks. In [[array-info]] and later, NumPy's `array.T` does the same for arrays.
''',
"tests": r'''
class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_zip_idiom(self):
        m = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(S.transpose(m), [list(r) for r in zip(*m)])
''',
},
# ======================================================================== Mathematics
"binomial-coefficient": {
"text": r'''
`math.comb(n, k)` is the standard-library binomial coefficient (exact integers, returns 0 when
`k > n`). [[binomial-pmf]] uses it directly once you have seen how it works.
''',
"tests": r'''
class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_math_comb(self):
        for n in range(0, 30, 3):
            for k in range(0, n + 3):
                self.assertEqual(S.comb(n, k), math.comb(n, k))
''',
},
"trapezoid-rule": {
"text": r'''
NumPy implements the same rule for sampled data as `np.trapezoid(y, x)` (named `np.trapz` before
NumPy 2.0), and SciPy offers more accurate methods such as `scipy.integrate.quad`. You will meet
NumPy in [[array-info]]; the comparison below evaluates your function and NumPy's on the same grid.
''',
"tests": r'''
import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_trapezoid(self):
        f = lambda t: math.exp(-t) * math.sin(3 * t)
        x = np.linspace(0.0, 2.0, 41)
        y = np.array([f(t) for t in x])
        integrate = getattr(np, "trapezoid", None) or np.trapz
        self.assertAlmostEqual(S.trapezoid(f, 0.0, 2.0, 40), float(integrate(y, x)), places=12)
''',
},
"power-iteration": {
"text": r'''
`numpy.linalg.eigh` (symmetric matrices) or `numpy.linalg.eig` compute *all* eigenvalues with
LAPACK; power iteration finds only the dominant one but needs nothing beyond matrix–vector
products, which is why it scales to huge sparse matrices (it is the idea behind PageRank). The
test compares your result with `eigh` on a symmetric matrix.
''',
"tests": r'''
import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_eigh(self):
        A = [[4.0, 1.0, 0.5], [1.0, 3.0, 0.2], [0.5, 0.2, 1.0]]
        lam, v = S.power_iteration(A)
        w, V = np.linalg.eigh(np.array(A))
        self.assertAlmostEqual(lam, w[-1], places=8)
        top = V[:, -1] * np.sign(V[np.argmax(np.abs(V[:, -1])), -1])
        np.testing.assert_allclose(v, top, atol=1e-4)
''',
},
# ======================================================================== Statistics
"mean-variance": {
"text": r'''
The `statistics` module provides `fmean`, `pvariance` (divide by $n$) and `variance` (divide by
$n-1$), plus `pstdev`/`stdev`. They use exact arithmetic internally where possible, so tiny
differences from your loop are rounding only.
''',
"tests": r'''
import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_statistics(self):
        data = [2.5, 3.0, 7.25, -1.0, 4.0]
        m, pv = S.mean_variance(data)
        _, sv = S.mean_variance(data, sample=True)
        self.assertAlmostEqual(m, statistics.fmean(data), places=12)
        self.assertAlmostEqual(pv, statistics.pvariance(data), places=12)
        self.assertAlmostEqual(sv, statistics.variance(data), places=12)
''',
},
"median-mode": {
"text": r'''
`statistics.median` averages the two middle values for even-length data, and
`statistics.multimode` returns every most-common value (in first-seen order; your function
sorts them). `statistics.mode` returns only one value.
''',
"tests": r'''
import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_statistics(self):
        for data in ([3, 1, 4, 1, 5, 9, 2, 6], [7], [2, 2, 3, 3, 1]):
            self.assertAlmostEqual(S.median(data), statistics.median(data))
            self.assertEqual(S.modes(data), sorted(statistics.multimode(data)))
''',
},
"percentiles": {
"text": r'''
Linear interpolation between order statistics is NumPy's default
(`np.percentile(data, q)`, method `"linear"`) and the `"inclusive"` method of
`statistics.quantiles(data, n=4, method="inclusive")`, which returns the three quartiles at once.
Other methods (such as the default `"exclusive"`) give slightly different answers for small
samples — always check which definition a library uses.
''',
"tests": r'''
import statistics

import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_and_statistics(self):
        data = [7, 1, 3, 9, 4, 4, 12, 2]
        for q in (0, 10, 25, 50, 90, 100):
            self.assertAlmostEqual(S.percentile(data, q), float(np.percentile(data, q)))
        q1, q2, q3 = statistics.quantiles(data, n=4, method="inclusive")
        self.assertAlmostEqual(S.iqr(data), q3 - q1)
''',
},
"histogram-bins": {
"text": r'''
`np.histogram(data, bins=k, range=(lo, hi))` uses the same rule: equal-width bins, each
half-open `[a, b)` except the last, which also includes `hi`; when `lo == hi` it widens the range
by 0.5 on each side, exactly as this exercise specifies. It returns `(counts, edges)` — the
opposite order to your function.
''',
"tests": r'''
import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_histogram(self):
        data = [0.0, 0.5, 1.0, 2.5, 3.0, 3.0, 4.9, 5.0]
        edges, counts = S.histogram(data, 5)
        np_counts, np_edges = np.histogram(data, bins=5)
        self.assertEqual(counts, np_counts.tolist())
        np.testing.assert_allclose(edges, np_edges)
        edges, counts = S.histogram([2.0, 2.0], 2)
        np_counts, np_edges = np.histogram([2.0, 2.0], bins=2)
        self.assertEqual(counts, np_counts.tolist())
        np.testing.assert_allclose(edges, np_edges)
''',
},
"covariance-correlation": {
"text": r'''
Python 3.10+ provides `statistics.covariance(x, y)` (sample, $n-1$) and
`statistics.correlation(x, y)` (Pearson). NumPy's `np.cov` and `np.corrcoef` return full
matrices for several variables at once.
''',
"tests": r'''
import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_statistics_module(self):
        x = [1.0, 2.0, 4.0, 7.0, 11.0]
        y = [2.1, 3.9, 8.2, 13.8, 22.5]
        self.assertAlmostEqual(S.covariance(x, y), statistics.covariance(x, y), places=10)
        self.assertAlmostEqual(S.pearson(x, y), statistics.correlation(x, y), places=10)
''',
},
"binomial-pmf": {
"text": r'''
`scipy.stats.binom(n, p)` provides `.pmf(k)`, `.cdf(k)` and `.sf(k - 1)` (the survival function,
$P(X \ge k)$), computed in a numerically careful way for large `n`. The comparison runs only when
SciPy is installed.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy_binom(self):
        from scipy.stats import binom
        for k in (0, 3, 7, 12):
            self.assertAlmostEqual(S.binom_pmf(k, 12, 0.35), float(binom.pmf(k, 12, 0.35)), places=12)
            self.assertAlmostEqual(S.binom_cdf(k, 12, 0.35), float(binom.cdf(k, 12, 0.35)), places=12)
            self.assertAlmostEqual(S.prob_at_least(k, 12, 0.35), float(binom.sf(k - 1, 12, 0.35)), places=12)
''',
},
"chi-square-gof": {
"text": r'''
`scipy.stats.chisquare(observed, f_exp=expected)` returns the same statistic together with a
p-value from the chi-square distribution with `len(observed) - 1` degrees of freedom, so you do not
need a critical-value table. The comparison runs only when SciPy is installed.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy_chisquare(self):
        from scipy.stats import chisquare
        observed, probs = [18, 22, 30, 30], [0.25, 0.25, 0.25, 0.25]
        res = S.chi_square_gof(observed, probs)
        ref = chisquare(observed, f_exp=res["expected"])
        self.assertAlmostEqual(res["statistic"], float(ref.statistic), places=10)
''',
},
"welch-t": {
"text": r'''
`scipy.stats.ttest_ind(x, y, equal_var=False)` performs Welch's test: its `statistic` is your
t, and recent SciPy versions also expose the Welch–Satterthwaite degrees of freedom as `.df`, plus
a p-value. The comparison runs only when SciPy is installed.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy_welch(self):
        from scipy.stats import ttest_ind
        x = [5.1, 4.9, 6.2, 5.8, 6.0, 5.5]
        y = [4.1, 4.4, 3.9, 4.8, 5.0]
        t, df = S.welch_t(x, y)
        ref = ttest_ind(x, y, equal_var=False)
        self.assertAlmostEqual(t, float(ref.statistic), places=10)
        if hasattr(ref, "df"):
            self.assertAlmostEqual(df, float(ref.df), places=8)
''',
},
"bootstrap-ci": {
"text": r'''
`scipy.stats.bootstrap((data,), np.mean, method="percentile")` computes percentile bootstrap
intervals (and better "BCa" intervals by default). Because it uses NumPy's random generator, its
resamples differ from yours, so the two intervals agree only approximately; the comparison checks
that they overlap closely and runs only when SciPy is installed.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_close_to_scipy_bootstrap(self):
        import numpy as np
        from scipy.stats import bootstrap
        data = [2.3, 3.1, 4.8, 5.0, 5.5, 6.1, 7.4, 8.0, 9.2, 10.5, 3.3, 4.4]
        lo, hi = S.bootstrap_ci(data, n_boot=4000, seed=1)
        ref = bootstrap((np.array(data),), np.mean, n_resamples=4000, method="percentile",
                        random_state=np.random.default_rng(1)).confidence_interval
        self.assertAlmostEqual(lo, ref.low, delta=0.35)
        self.assertAlmostEqual(hi, ref.high, delta=0.35)
''',
},
# ======================================================================== NumPy
"pairwise-distances": {
"text": r'''
The expansion $\lVert a-b\rVert^2 = \lVert a\rVert^2 + \lVert b\rVert^2 - 2a\cdot b$ is what fast
libraries use. SciPy exposes it as `scipy.spatial.distance.cdist(A, B, "sqeuclidean")` and
scikit-learn as `sklearn.metrics.pairwise.euclidean_distances(A, B, squared=True)`. The tests
compare with a plain double loop and, when installed, with SciPy.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_double_loop(self):
        import numpy as np
        rng = np.random.default_rng(0)
        A, B = rng.normal(size=(4, 3)), rng.normal(size=(5, 3))
        loop = [[sum((a - b) ** 2 for a, b in zip(r, s)) for s in B] for r in A]
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), loop, atol=1e-10)

    @unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
    def test_library_matches_cdist(self):
        import numpy as np
        from scipy.spatial.distance import cdist
        rng = np.random.default_rng(1)
        A, B = rng.normal(size=(6, 4)), rng.normal(size=(3, 4))
        np.testing.assert_allclose(S.pairwise_sq_dists(A, B), cdist(A, B, "sqeuclidean"), atol=1e-10)
''',
},
"linalg-solve": {
"text": r'''
`np.linalg.solve` is the library version of [[solve-2x2-cramer]] for any size (it uses an LU
factorisation, not Cramer's rule, which would be far slower and less stable). For fitting lines,
`np.polyfit(x, y, 1)` returns `[slope, intercept]` — the reverse order of `fit_line`. The tests
compare against Cramer's rule for a 2×2 system and `np.polyfit`.
''',
"tests": r'''
import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_cramer_2x2(self):
        (a, b), (c, d), (e, f) = (2.0, 1.0), (1.0, 3.0), (5.0, 10.0)
        det = a * d - b * c
        x = S.solve([[a, b], [c, d]], [e, f])
        np.testing.assert_allclose(x, [(e * d - b * f) / det, (a * f - e * c) / det])

    def test_library_fit_line_matches_polyfit(self):
        x = [0.0, 1.0, 2.0, 3.0, 4.5]
        y = [1.1, 2.9, 5.2, 7.1, 9.8]
        slope, intercept = np.polyfit(x, y, 1)
        b0, b1 = S.fit_line(x, y)
        self.assertAlmostEqual(b0, intercept, places=10)
        self.assertAlmostEqual(b1, slope, places=10)
''',
},
"one-hot": {
"text": r'''
A compact NumPy idiom is `np.eye(K)[labels]`: row `i` of the identity matrix is the one-hot
vector for class `i`, and fancy indexing picks one row per label. scikit-learn's `OneHotEncoder`
and pandas' `pd.get_dummies` do the same for tables, including string categories.
''',
"tests": r'''
import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_eye_idiom(self):
        labels = np.array([2, 0, 1, 2, 3])
        np.testing.assert_array_equal(S.one_hot(labels, 5), np.eye(5)[labels])
''',
},
"moving-average": {
"text": r'''
`np.convolve(x, np.ones(w) / w, mode="valid")` computes the same moving average as a
convolution, and pandas offers `Series.rolling(w).mean()` ([[rolling-features]]). The cumulative-sum
trick costs O(n) regardless of `w`.
''',
"tests": r'''
import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_convolve(self):
        x = np.array([3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0])
        for w in (1, 3, 8):
            np.testing.assert_allclose(S.moving_average(x, w), np.convolve(x, np.ones(w) / w, mode="valid"))
''',
},
# ======================================================================== pandas
"groupby-agg": {
"text": r'''
Before `groupby`, the same summary is a dictionary of lists ([[gradebook-aggregate]]): append each
value to its category's list, then count, sum and average while skipping missing values. pandas
does the split–apply–combine in optimised code and keeps the result as a DataFrame. The test
computes the summary both ways.
''',
"tests": r'''
import math

import numpy as np
import pandas as pd


class TestAgainstPlainPython(unittest.TestCase):
    def test_library_matches_dict_version(self):
        rows = [("b", 4.0), ("a", 1.0), ("b", None), ("a", 3.0), ("c", 10.0), ("b", 2.0)]
        df = pd.DataFrame(rows, columns=["category", "value"])
        groups = {}
        for cat, val in rows:
            groups.setdefault(cat, []).append(val)
        out = S.category_summary(df)
        for _, r in out.iterrows():
            vals = groups[r["category"]]
            valid = [v for v in vals if v is not None]
            self.assertEqual(r["n"], len(vals))
            self.assertEqual(r["n_valid"], len(valid))
            self.assertAlmostEqual(r["total"], sum(valid))
            self.assertAlmostEqual(r["mean"], sum(valid) / len(valid))
        self.assertEqual(out["category"].tolist(), sorted(groups))
''',
},
"merge-tables": {
"text": r'''
A left join is a dictionary lookup: build `{customer_id: name}` from the customers table, then
look up each order, using a default when the id is missing. `pd.merge` does this for whole tables,
can check the relationship (`validate="many_to_one"`), and supports inner, outer and right joins.
The test performs the join with a dict and compares.
''',
"tests": r'''
import pandas as pd


class TestAgainstPlainPython(unittest.TestCase):
    def test_library_left_join_matches_dict_lookup(self):
        orders = pd.DataFrame({"order_id": [1, 2, 3, 4], "customer_id": [10, 11, 10, 99], "amount": [5.0, 7.5, 2.5, 1.0]})
        customers = pd.DataFrame({"customer_id": [10, 11], "name": ["ada", "bob"]})
        lookup = dict(zip(customers["customer_id"], customers["name"]))
        expected = [lookup.get(c, "unknown") for c in orders["customer_id"]]
        self.assertEqual(S.orders_with_customers(orders, customers)["name"].tolist(), expected)
''',
},
# ======================================================================== Machine Learning
"train-test-split": {
"text": r'''
scikit-learn's `train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)` does the same
job with its own random generator, so the chosen rows differ from yours; it also rounds the test
size **up** (`ceil`) where this exercise rounds to nearest. What must agree is the contract: the
two parts are disjoint, together contain every row, and stratification preserves class
proportions. The test checks that contract on scikit-learn's output and yours when it is
installed.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_same_contract(self):
        import numpy as np
        from sklearn.model_selection import train_test_split as sk_split
        X = np.arange(40).reshape(20, 2)
        y = np.array([0] * 12 + [1] * 8)
        for split in (S.train_test_split(X, y, test_size=0.25, seed=0, stratify=True),
                      sk_split(X, y, test_size=0.25, random_state=0, stratify=y)):
            Xtr, Xte, ytr, yte = split
            self.assertEqual(sorted(np.concatenate([Xtr[:, 0], Xte[:, 0]]).tolist()), X[:, 0].tolist())
            self.assertEqual(np.bincount(yte).tolist(), [3, 2])
''',
},
"regression-metrics": {
"text": r'''
`sklearn.metrics` provides `mean_squared_error`, `root_mean_squared_error`,
`mean_absolute_error` and `r2_score` with the same definitions. Comparison runs when scikit-learn
is installed.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_metrics(self):
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        yt, yp = [3.0, -0.5, 2.0, 7.0, 4.2], [2.5, 0.0, 2.0, 8.0, 3.9]
        r = S.regression_report(yt, yp)
        self.assertAlmostEqual(r["mse"], mean_squared_error(yt, yp))
        self.assertAlmostEqual(r["mae"], mean_absolute_error(yt, yp))
        self.assertAlmostEqual(r["r2"], r2_score(yt, yp))
''',
},
"classification-metrics": {
"text": r'''
`sklearn.metrics.confusion_matrix(y_true, y_pred, labels=range(K))` uses the same layout (rows =
true class, columns = predicted), and `precision_recall_fscore_support(..., zero_division=0)`
returns per-class precision, recall and F1 with the same convention for empty classes.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn(self):
        import numpy as np
        from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support
        yt = [0, 1, 2, 2, 1, 0, 2, 3]
        yp = [0, 2, 2, 2, 1, 1, 0, 0]
        np.testing.assert_array_equal(S.confusion_matrix(yt, yp, 4), confusion_matrix(yt, yp, labels=range(4)))
        rep = S.classification_report(yt, yp, 4)
        p, r, f, _ = precision_recall_fscore_support(yt, yp, labels=range(4), zero_division=0)
        np.testing.assert_allclose(rep["precision"], p)
        np.testing.assert_allclose(rep["recall"], r)
        np.testing.assert_allclose(rep["f1"], f)
        self.assertAlmostEqual(rep["macro_f1"], f1_score(yt, yp, labels=range(4), average="macro", zero_division=0))
''',
},
"standard-scaler": {
"text": r'''
`sklearn.preprocessing.StandardScaler` has the same interface (`fit`, `transform`,
`fit_transform`, `inverse_transform`), uses the population standard deviation and leaves
constant columns unscaled (scale 1), exactly like your class.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_scaler(self):
        import numpy as np
        from sklearn.preprocessing import StandardScaler as SkScaler
        Xtr = np.array([[1.0, 5.0, 2.0], [2.0, 5.0, 4.0], [4.0, 5.0, 9.0]])
        Xte = np.array([[3.0, 5.0, 1.0]])
        ours, theirs = S.StandardScaler().fit(Xtr), SkScaler().fit(Xtr)
        np.testing.assert_allclose(ours.transform(Xte), theirs.transform(Xte))
        np.testing.assert_allclose(ours.scale_, theirs.scale_)
''',
},
"least-squares-line": {
"text": r'''
`np.polyfit(x, y, 1)` and scikit-learn's `LinearRegression().fit(x.reshape(-1, 1), y)` fit the
same line; `LinearRegression.score` is the same $R^2$. The NumPy comparison always runs; the
scikit-learn one runs when it is installed.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_polyfit(self):
        import numpy as np
        x = np.array([1.0, 2.0, 3.0, 5.0, 8.0])
        y = np.array([2.2, 2.8, 4.1, 6.2, 9.9])
        m = S.SimpleLinearRegression().fit(x, y)
        slope, intercept = np.polyfit(x, y, 1)
        self.assertAlmostEqual(m.slope_, slope, places=10)
        self.assertAlmostEqual(m.intercept_, intercept, places=10)

    @unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
    def test_library_matches_sklearn(self):
        import numpy as np
        from sklearn.linear_model import LinearRegression
        x = np.array([1.0, 2.0, 3.0, 5.0, 8.0])
        y = np.array([2.2, 2.8, 4.1, 6.2, 9.9])
        sk = LinearRegression().fit(x.reshape(-1, 1), y)
        m = S.SimpleLinearRegression().fit(x, y)
        self.assertAlmostEqual(m.score(x, y), sk.score(x.reshape(-1, 1), y), places=10)
''',
},
"knn-classifier": {
"text": r'''
`sklearn.neighbors.KNeighborsClassifier(n_neighbors=k)` gives the same predictions when there are
no ties; for tied votes it picks the smallest label, whereas this exercise picks the label of the
nearest tied neighbour. It also uses tree structures to find neighbours quickly in large data.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_without_ties(self):
        import numpy as np
        from sklearn.neighbors import KNeighborsClassifier
        rng = np.random.default_rng(0)
        Xtr = np.vstack([rng.normal(0, 1, (15, 2)), rng.normal(3, 1, (15, 2))])
        ytr = np.array([0] * 15 + [1] * 15)
        Xte = rng.normal(1.5, 1.5, (20, 2))
        sk = KNeighborsClassifier(n_neighbors=3).fit(Xtr, ytr)
        np.testing.assert_array_equal(S.knn_predict(Xtr, ytr, Xte, k=3), sk.predict(Xte))
''',
},
"logistic-regression": {
"text": r'''
`sklearn.linear_model.LogisticRegression` fits the same model with a second-order solver (L-BFGS)
instead of fixed-step gradient descent, and adds L2 regularisation by default (strength `1/C`).
With a very large `C` the regularisation vanishes, and after enough epochs your gradient descent
reaches nearly the same probabilities. The comparison runs when scikit-learn is installed.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_close_to_sklearn(self):
        import numpy as np
        from sklearn.linear_model import LogisticRegression as SkLR
        rng = np.random.default_rng(0)
        X = rng.normal(size=(200, 2))
        p = 1 / (1 + np.exp(-(X @ np.array([1.5, -2.0]) + 0.3)))
        y = (rng.random(200) < p).astype(int)
        ours = S.LogisticRegression(lr=0.5, epochs=4000).fit(X, y)
        sk = SkLR(C=1e10, max_iter=10000, tol=1e-10).fit(X, y)
        np.testing.assert_allclose(ours.predict_proba(X), sk.predict_proba(X)[:, 1], atol=2e-3)
''',
},
"k-fold-cv": {
"text": r'''
`sklearn.model_selection.KFold(n_splits=k)` (no shuffling) produces exactly the folds of
`np.array_split`: consecutive blocks, the first `n % k` folds one element larger.
`cross_val_score(estimator, X, y, cv=KFold(...))` runs the fit–score loop for you.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_folds_match_kfold(self):
        import numpy as np
        from sklearn.model_selection import KFold
        ours = S.kfold_indices(11, 3)
        theirs = list(KFold(n_splits=3).split(np.zeros(11)))
        for (tr, te), (str_, ste) in zip(ours, theirs):
            np.testing.assert_array_equal(np.sort(tr), str_)
            np.testing.assert_array_equal(te, ste)
''',
},
"ridge-regression": {
"text": r'''
`sklearn.linear_model.Ridge(alpha=...)` solves the same penalised least-squares problem and, like
your class, does not penalise the intercept (it centres the data first).
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_ridge(self):
        import numpy as np
        from sklearn.linear_model import Ridge as SkRidge
        rng = np.random.default_rng(0)
        X = rng.normal(size=(30, 4))
        y = X @ np.array([1.0, -2.0, 0.5, 0.0]) + 3 + rng.normal(0, 0.1, 30)
        for alpha in (0.1, 5.0):
            ours, sk = S.Ridge(alpha).fit(X, y), SkRidge(alpha=alpha).fit(X, y)
            np.testing.assert_allclose(ours.coef_, sk.coef_, atol=1e-8)
            self.assertAlmostEqual(ours.intercept_, sk.intercept_, places=8)
''',
},
"decision-stump-gini": {
"text": r'''
A depth-1 `sklearn.tree.DecisionTreeClassifier(max_depth=1, criterion="gini")` is a decision
stump: it searches the same midpoint thresholds and minimises the same weighted Gini impurity. Its
`tree_` attribute exposes the chosen `feature[0]` and `threshold[0]`.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_depth_one_tree(self):
        import numpy as np
        from sklearn.tree import DecisionTreeClassifier
        X = np.array([[2.0, 7.0], [3.0, 1.0], [5.0, 6.0], [6.0, 2.0], [8.0, 3.0], [9.0, 8.0]])
        y = np.array([0, 0, 0, 1, 1, 1])
        best = S.best_split(X, y)
        tree = DecisionTreeClassifier(max_depth=1, random_state=0).fit(X, y).tree_
        self.assertEqual(best["feature"], tree.feature[0])
        self.assertAlmostEqual(best["threshold"], tree.threshold[0])
''',
},
"kmeans": {
"text": r'''
`sklearn.cluster.KMeans(n_clusters=k, init=initial_centroids, n_init=1, algorithm="lloyd")` runs
the same Lloyd iterations from the same starting centroids; by default it instead chooses starts
with k-means++ and keeps the best of several runs. The comparison runs when scikit-learn is
installed.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_lloyd(self):
        import numpy as np
        from sklearn.cluster import KMeans
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(c, 0.5, (20, 2)) for c in (0.0, 4.0, 8.0)])
        init = X[[0, 25, 45]]
        ours = S.kmeans(X, init)
        sk = KMeans(n_clusters=3, init=init, n_init=1, algorithm="lloyd", tol=0).fit(X)
        np.testing.assert_allclose(ours["centroids"], sk.cluster_centers_, atol=1e-8)
        np.testing.assert_array_equal(ours["labels"], sk.labels_)
        self.assertAlmostEqual(ours["inertia"], sk.inertia_, places=6)
''',
},
# ======================================================================== Deep Learning
"stable-softmax": {
"text": r'''
`scipy.special.softmax` and `scipy.special.log_softmax` (and `torch.softmax` /
`torch.log_softmax`) implement the same max-subtraction trick along any axis.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_scipy(self):
        import numpy as np
        from scipy.special import log_softmax, softmax
        z = np.array([[1000.0, 1001.0, 999.0], [-3.0, 0.0, 2.5]])
        np.testing.assert_allclose(S.softmax(z, axis=1), softmax(z, axis=1), atol=1e-12)
        np.testing.assert_allclose(S.log_softmax(z, axis=0), log_softmax(z, axis=0), atol=1e-12)
''',
},
"cross-entropy": {
"text": r'''
`torch.nn.functional.cross_entropy(logits, labels)` combines log-softmax and the negative
log-likelihood exactly like your function (mean over the batch), and autograd's gradient equals
`(softmax - one_hot) / n`. The comparison runs when PyTorch is installed.
''',
"optional": ["torch"],
"tests": TORCH + r'''

@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_library_matches_torch(self):
        import numpy as np
        logits = np.array([[2.0, -1.0, 0.5], [0.1, 0.2, 3.0], [-2.0, 4.0, 1.0]])
        labels = np.array([0, 2, 1])
        t = torch.tensor(logits, requires_grad=True)
        loss = torch.nn.functional.cross_entropy(t, torch.tensor(labels))
        loss.backward()
        self.assertAlmostEqual(S.cross_entropy(logits, labels), loss.item(), places=12)
        np.testing.assert_allclose(S.cross_entropy_grad(logits, labels), t.grad.numpy(), atol=1e-12)
''',
},
"batchnorm-forward": {
"text": r'''
`torch.nn.BatchNorm1d(n_features, momentum=0.1, eps=1e-5)` uses the same conventions: batch
statistics with the biased variance in training mode, running averages updated with the
**unbiased** variance, and running statistics in evaluation mode (`model.eval()`).
''',
"optional": ["torch"],
"tests": TORCH + r'''

@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_library_matches_torch_batchnorm(self):
        import numpy as np
        rng = np.random.default_rng(0)
        batches = [rng.normal(2, 3, (8, 4)) for _ in range(3)]
        ours = S.BatchNorm1d(4)
        theirs = torch.nn.BatchNorm1d(4, dtype=torch.float64)
        theirs.train()
        for b in batches:
            np.testing.assert_allclose(ours.forward(b, training=True),
                                       theirs(torch.tensor(b)).detach().numpy(), atol=1e-10)
        np.testing.assert_allclose(ours.running_var, theirs.running_var.numpy(), atol=1e-10)
        theirs.eval()
        test = rng.normal(size=(5, 4))
        np.testing.assert_allclose(ours.forward(test, training=False),
                                   theirs(torch.tensor(test)).detach().numpy(), atol=1e-10)
''',
},
"conv1d": {
"text": r'''
With stride 1, `np.correlate(np.pad(x, p), kernel, mode="valid")` computes the same values
(NumPy's `np.convolve` flips the kernel; deep-learning "convolution" does not).
`torch.nn.functional.conv1d` adds batches, channels and strides.
''',
"tests": r'''
import numpy as np


class TestAgainstLibrary(unittest.TestCase):
    def test_library_matches_numpy_correlate(self):
        x = np.array([1.0, 3.0, -2.0, 4.0, 0.5, 2.0])
        w = np.array([0.5, -1.0, 2.0])
        for p in (0, 1, 2):
            np.testing.assert_allclose(S.conv1d(x, w, padding=p), np.correlate(np.pad(x, p), w, mode="valid"))
        np.testing.assert_allclose(S.conv1d(x, w, stride=2), np.correlate(x, w, mode="valid")[::2])
''',
},
# ======================================================================== Computer Vision
"conv2d-filter": {
"text": r'''
`scipy.ndimage.correlate(img, kernel, mode="constant", cval=0.0)` computes the same zero-padded
filter, and `mode="nearest"` matches edge padding. OpenCV's `cv2.filter2D` is the equivalent in
OpenCV. The comparison runs when SciPy is installed.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_ndimage_correlate(self):
        import numpy as np
        from scipy.ndimage import correlate
        rng = np.random.default_rng(0)
        img = rng.integers(0, 255, (7, 9)).astype(float)
        K = rng.normal(size=(3, 5))
        np.testing.assert_allclose(S.filter2d(img, K), correlate(img, K, mode="constant", cval=0.0), atol=1e-9)
        np.testing.assert_allclose(S.filter2d(img, K, mode="edge"), correlate(img, K, mode="nearest"), atol=1e-9)
''',
},
"sobel-edges": {
"text": r'''
`scipy.ndimage.sobel(img, axis=1)` and `axis=0` compute the horizontal and vertical Sobel
derivatives (with border handling); on interior pixels they equal your valid-region `gx` and `gy`.
`np.hypot(gx, gy)` gives the magnitude in both cases.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_ndimage_sobel(self):
        import numpy as np
        from scipy import ndimage
        rng = np.random.default_rng(1)
        img = rng.random((6, 7))
        gx, gy, _ = S.sobel(img)
        np.testing.assert_allclose(gx, ndimage.sobel(img, axis=1)[1:-1, 1:-1], atol=1e-12)
        np.testing.assert_allclose(gy, ndimage.sobel(img, axis=0)[1:-1, 1:-1], atol=1e-12)
''',
},
"max-pool-2d": {
"text": r'''
`torch.nn.functional.max_pool2d` and `avg_pool2d` (with `kernel_size` and `stride`) implement
the same windows for batched, multi-channel tensors. The comparison runs when PyTorch is installed.
''',
"optional": ["torch"],
"tests": TORCH + r'''

@unittest.skipIf(torch is None, "PyTorch not installed")
class TestAgainstPyTorch(unittest.TestCase):
    def test_library_matches_torch_pooling(self):
        import numpy as np
        x = np.random.default_rng(0).normal(size=(7, 8))
        t = torch.tensor(x)[None, None]
        F = torch.nn.functional
        np.testing.assert_allclose(S.pool2d(x, 2), F.max_pool2d(t, 2)[0, 0].numpy())
        np.testing.assert_allclose(S.pool2d(x, 3, 2, mode="avg"), F.avg_pool2d(t, 3, 2)[0, 0].numpy())
''',
},
"connected-components": {
"text": r'''
`scipy.ndimage.label(mask, structure=...)` labels connected components with optimised code; a
3×3 cross structure is 4-connectivity and `np.ones((3, 3))` is 8-connectivity. Label numbers are
assigned in scan order of each component's first pixel, so they match yours. The comparison runs
when SciPy is installed.
''',
"optional": ["scipy"],
"tests": SCIPY + r'''

@unittest.skipUnless(HAVE_SCIPY, "SciPy not installed")
class TestAgainstSciPy(unittest.TestCase):
    def test_library_matches_ndimage_label(self):
        import numpy as np
        from scipy import ndimage
        mask = np.array([[1, 1, 0, 0, 1],
                         [0, 1, 0, 1, 1],
                         [1, 0, 0, 0, 0],
                         [1, 0, 1, 1, 0],
                         [0, 0, 0, 1, 1]], dtype=bool)
        for conn, structure in ((4, ndimage.generate_binary_structure(2, 1)), (8, np.ones((3, 3)))):
            labels, sizes = S.label_components(mask, connectivity=conn)
            ref, n = ndimage.label(mask, structure=structure)
            np.testing.assert_array_equal(labels, ref)
            self.assertEqual(len(sizes), n)
''',
},
# ======================================================================== NLP
"stopword-counts": {
"text": r'''
`collections.Counter(tokens).most_common(n)` returns the top counts, but breaks ties by first
appearance rather than alphabetically, which is why this exercise sorts explicitly. NLTK and
spaCy ship curated stopword lists; scikit-learn's `CountVectorizer(stop_words="english")` uses
its own list. The test checks your counts against `Counter`.
''',
"tests": r'''
from collections import Counter


class TestAgainstLibrary(unittest.TestCase):
    def test_library_counts_match_counter(self):
        tokens = "the cat and the dog and the bird saw a cat".split()
        top = S.top_words(tokens, 10, stopwords={"the", "and", "a"})
        expected = Counter(t for t in tokens if t not in {"the", "and", "a"})
        self.assertEqual(dict(top), dict(expected))
''',
},
"bag-of-words": {
"text": r'''
scikit-learn's `CountVectorizer` builds the vocabulary and count matrix in one step (as a sparse
matrix). Passing `analyzer=lambda doc: doc` makes it accept pre-tokenised documents, and
`vocabulary=vocab` reuses your vocabulary. The comparison runs when scikit-learn is installed.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_count_vectorizer(self):
        import numpy as np
        from sklearn.feature_extraction.text import CountVectorizer
        docs = [["the", "cat", "sat"], ["the", "dog", "sat", "sat"], ["a", "cat"]]
        vocab = S.build_vocab(docs)
        cv = CountVectorizer(analyzer=lambda d: d).fit(docs)
        self.assertEqual(vocab, {k: int(v) for k, v in cv.vocabulary_.items()})
        np.testing.assert_array_equal(S.vectorize(docs, vocab), cv.transform(docs).toarray())
''',
},
"tf-idf": {
"text": r'''
`sklearn.feature_extraction.text.TfidfTransformer()` with its defaults (`smooth_idf=True`,
`norm="l2"`, raw counts) uses exactly this formula: $\mathrm{idf} = \ln\frac{1+n}{1+df} + 1$ and
L2-normalised rows. `TfidfVectorizer` does tokenising, counting and weighting together.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_tfidf_transformer(self):
        import numpy as np
        from sklearn.feature_extraction.text import TfidfTransformer
        counts = np.array([[3, 0, 1, 0], [2, 1, 0, 0], [0, 0, 4, 1], [1, 1, 1, 1]])
        W, idf = S.tfidf(counts)
        t = TfidfTransformer().fit(counts)
        np.testing.assert_allclose(idf, t.idf_)
        np.testing.assert_allclose(W, t.transform(counts).toarray(), atol=1e-12)
''',
},
"cosine-retrieval": {
"text": r'''
`sklearn.metrics.pairwise.cosine_similarity(A, B)` returns the same matrix (treating all-zero
rows as similarity 0). For large collections, vector databases and libraries such as FAISS find
the top-k without computing every score.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_cosine_similarity(self):
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        rng = np.random.default_rng(0)
        A, B = rng.random((3, 5)), rng.random((4, 5))
        np.testing.assert_allclose(S.cosine_matrix(A, B), cosine_similarity(A, B), atol=1e-12)
''',
},
"naive-bayes-text": {
"text": r'''
`sklearn.naive_bayes.MultinomialNB(alpha=1.0)` stores the same `class_log_prior_` and
`feature_log_prob_` and its `predict_log_proba` normalises the joint log-likelihood exactly as
yours does. It accepts sparse count matrices from `CountVectorizer`.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_matches_sklearn_nb(self):
        import numpy as np
        from sklearn.naive_bayes import MultinomialNB as SkNB
        X = np.array([[2, 1, 0, 0], [3, 0, 1, 0], [0, 0, 2, 3], [0, 1, 1, 4], [1, 0, 0, 2]])
        y = np.array(["spam", "spam", "ham", "ham", "ham"])
        ours, sk = S.MultinomialNB(alpha=0.5).fit(X, y), SkNB(alpha=0.5).fit(X, y)
        np.testing.assert_allclose(ours.feature_log_prob_, sk.feature_log_prob_)
        np.testing.assert_allclose(ours.class_log_prior_, sk.class_log_prior_)
        Xt = np.array([[1, 1, 0, 0], [0, 0, 1, 1]])
        np.testing.assert_allclose(ours.predict_log_proba(Xt), sk.predict_log_proba(Xt), atol=1e-12)
''',
},
# ======================================================================== Explainable AI
"permutation-importance": {
"text": r'''
`sklearn.inspection.permutation_importance(estimator, X, y, n_repeats=..., random_state=...)`
implements the same algorithm for fitted scikit-learn models (and pipelines). It uses its own
random shuffles, so individual numbers differ slightly from yours, but the ranking of clearly
important features agrees. The comparison runs when scikit-learn is installed.
''',
"optional": ["scikit-learn"],
"tests": SKLEARN + r'''

@unittest.skipUnless(HAVE_SKLEARN, "scikit-learn not installed")
class TestAgainstScikitLearn(unittest.TestCase):
    def test_library_same_ranking_as_sklearn(self):
        import numpy as np
        from sklearn.inspection import permutation_importance as sk_pi
        from sklearn.linear_model import LinearRegression
        rng = np.random.default_rng(0)
        X = rng.normal(size=(200, 3))
        y = 5 * X[:, 0] + 1 * X[:, 1] + rng.normal(0, 0.1, 200)
        model = LinearRegression().fit(X, y)
        r2 = lambda yt, yp: 1 - np.sum((yt - yp) ** 2) / np.sum((yt - yt.mean()) ** 2)
        ours = S.permutation_importance(model.predict, X, y, r2, n_repeats=10, seed=0)
        theirs = sk_pi(model, X, y, n_repeats=10, random_state=0)
        self.assertEqual(list(np.argsort(-ours["mean"])), list(np.argsort(-theirs.importances_mean)))
        np.testing.assert_allclose(ours["mean"], theirs.importances_mean, rtol=0.2, atol=0.02)
''',
},
}
