"""Problem definitions for the statistics topic (original 2026 packs, revised for the step-by-step path).

Topic order and IDs come from build/path.py; topic introductions from build/overviews.py.
"""

PROBLEMS = [
# ---------------------------------------------------------------- mean-variance
{
"slug": "mean-variance", "title": "Mean and Variance (Population vs Sample)",
"difficulty": "beginner", "prereqs": ["summation"], "packages": [],
"objectives": ["Compute mean and variance", "Distinguish population (N) and sample (N−1) variance",
               "Relate variance and standard deviation"],
"tags": ["descriptive-statistics", "variance", "bessel-correction"],
"sources": ["S003", "S010"], "entry": "mean_variance(data, sample=False)",
"article": r'''
# Mean and Variance

## Intuition
The mean tells you where the data is centred; the variance tells you how spread out it is
around that centre. Variance is the average squared distance from the mean.

## Precise explanation
For data $x_1,\dots,x_n$ with mean $\bar x = \frac1n\sum x_i$:
* **Population variance** (the data *is* the whole population):
  $\sigma^2 = \frac{1}{n}\sum (x_i-\bar x)^2$.
* **Sample variance** (the data is a sample used to estimate a larger population):
  $s^2 = \frac{1}{n-1}\sum (x_i-\bar x)^2$. Dividing by $n-1$ (Bessel's correction) makes the
  estimate unbiased, because deviations from the *sample* mean are slightly too small on average.
* Standard deviation = square root of variance, in the original units.

Python's `statistics.pvariance` uses $n$, `statistics.variance` uses $n-1$; NumPy's `np.var`
defaults to $n$ (`ddof=0`) — a frequent source of mismatched results.

The two-pass method (compute the mean, then sum squared deviations) is numerically safer than
the textbook shortcut $\overline{x^2} - \bar x^2$, which can lose precision or even go negative.

## Worked example
Data 2, 4, 4, 4, 5, 5, 7, 9: mean 5; squared deviations 9,1,1,1,0,0,4,16 sum 32.
Population variance 32/8 = 4 (sd 2). Sample variance 32/7 ≈ 4.571.

## Common mistakes
* Mixing $n$ and $n-1$ between libraries.
* Computing sample variance of a single value (division by zero — it is undefined).
* Forgetting to square deviations (they sum to zero).

## Why this matters
Variance drives feature standardisation ([[standard-scaler]]), batch normalisation ([[batchnorm-forward]]), confidence
intervals and the bias–variance trade-off.
''',
"statement": r'''
Write `mean_variance(data, sample=False)` returning `(mean, variance)` as floats using the
two-pass method.

* `sample=False` → divide by `n`; `sample=True` → divide by `n - 1`.
* Raise `ValueError` if `data` is empty, or if `sample=True` and `len(data) < 2`.
* Do not use the `statistics` module.

**Examples**
```python
mean_variance([2, 4, 4, 4, 5, 5, 7, 9])               # (5.0, 4.0)
mean_variance([2, 4, 4, 4, 5, 5, 7, 9], sample=True)  # (5.0, 4.571428571428571)
mean_variance([3])                                    # (3.0, 0.0)
```
''',
"starter": r'''
def mean_variance(data, sample=False):
    """Return (mean, variance); population by default, sample if sample=True."""
    # TODO
    pass
''',
"hints": [
    "Validate the length first, depending on `sample`.",
    "Pass 1: `m = sum(data) / n`. Pass 2: `ss = sum((x - m) ** 2 for x in data)`.",
    "Divide `ss` by `n - 1` if sample else `n`.",
],
"solution": r'''
def mean_variance(data, sample=False):
    n = len(data)
    if n == 0:
        raise ValueError("data must be non-empty")
    if sample and n < 2:
        raise ValueError("sample variance needs at least two values")
    m = sum(data) / n
    ss = sum((x - m) ** 2 for x in data)
    return float(m), ss / (n - 1 if sample else n)
''',
"explanation": r'''
The mean is computed first, then the sum of squared deviations from it. The only difference
between population and sample variance is the denominator. Validation prevents division by zero.
''',
"tests": r'''
import statistics

DATA = [2, 4, 4, 4, 5, 5, 7, 9]

class TestMeanVar(unittest.TestCase):
    def test_population(self):
        self.assertEqual(S.mean_variance(DATA), (5.0, 4.0))

    def test_sample(self):
        m, v = S.mean_variance(DATA, sample=True)
        self.assertAlmostEqual(v, 32 / 7, places=12)

    def test_single(self):
        self.assertEqual(S.mean_variance([3]), (3.0, 0.0))

    def test_single_sample_error(self):
        with self.assertRaises(ValueError):
            S.mean_variance([3], sample=True)

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.mean_variance([])

    def test_matches_statistics_module(self):
        d = [0.5, 1.75, -2.0, 3.25, 10.0]
        self.assertAlmostEqual(S.mean_variance(d)[1], statistics.pvariance(d), places=12)
        self.assertAlmostEqual(S.mean_variance(d, sample=True)[1], statistics.variance(d), places=12)

    def test_large_offset_stable(self):
        d = [1e9 + 4, 1e9 + 7, 1e9 + 13, 1e9 + 16]
        self.assertAlmostEqual(S.mean_variance(d)[1], 22.5, places=6)
''',
"feedback": [
    ("test_sample", "Sample variance divides by n − 1."),
    ("test_large_offset_stable", "Use the two-pass method; E[x²] − E[x]² loses precision for large values."),
    ("test_single_sample_error", "Sample variance of one value is undefined — raise ValueError."),
    ("test_population", "Return the mean as a float and divide by n for population variance."),
],
},
# ---------------------------------------------------------------- median-mode
{
"slug": "median-mode", "title": "Median and Mode",
"difficulty": "beginner", "prereqs": ["mean-variance"], "packages": [],
"objectives": ["Compute the median for odd and even n", "Find all modes including ties",
               "Explain robustness to outliers"],
"tags": ["descriptive-statistics", "median", "mode", "robustness"],
"sources": ["S003", "S010"], "entry": "median(data); modes(data)",
"article": r'''
# Median and Mode

## Intuition
The **median** is the middle value when the data is sorted — half the data is below it, half
above. The **mode** is the most common value. Unlike the mean, the median barely moves when one
value is extreme: the median salary in a room doesn't change when a billionaire walks in.

## Precise explanation
Sort the data, $x_{(1)} \le \dots \le x_{(n)}$.
* $n$ odd: median $= x_{((n+1)/2)}$ — in 0-based Python, `s[n // 2]`.
* $n$ even: median = average of the two middle values, `(s[n//2 - 1] + s[n//2]) / 2`.

A dataset may have several modes (multimodal). Returning all of them, sorted, is unambiguous.
`statistics.multimode` returns them in first-occurrence order; here we sort for determinism.

## Worked example
`[7, 1, 3, 3, 100]` → sorted `[1, 3, 3, 7, 100]` → median 3, mean 22.8 (pulled by 100).
`[4, 1, 2, 3]` → sorted `[1, 2, 3, 4]` → median 2.5. Modes of `[1, 2, 2, 3, 3]` → `[2, 3]`.

## Common mistakes
* Taking the middle element without sorting.
* Using `n / 2` (a float) as an index.
* Returning only the first mode when there is a tie.

## Why this matters
Robust statistics (median, IQR) are used for outlier-resistant scaling and to impute missing
values; the mode is the natural imputation for categorical data.
''',
"statement": r'''
Implement:
* `median(data)` → float median; raise `ValueError` on empty input. Do not modify `data`.
* `modes(data)` → sorted list of all values with the highest frequency (`[]` for empty input).

**Examples**
```python
median([7, 1, 3, 3, 100])   # 3.0
median([4, 1, 2, 3])        # 2.5   — even length: mean of the two middle values
modes([1, 2, 2, 3, 3])      # [2, 3]
modes([5])                  # [5]
```
''',
"starter": r'''
def median(data):
    """Return the median of data as a float."""
    # TODO
    pass


def modes(data):
    """Return a sorted list of all most-frequent values."""
    # TODO
    return []
''',
"hints": [
    "Use `s = sorted(data)` (a new list) and `n = len(s)`.",
    "Odd: `s[n // 2]`; even: average of `s[n // 2 - 1]` and `s[n // 2]`.",
    "Count with a dict, find the max count, collect keys with that count, then sort.",
],
"solution": r'''
def median(data):
    if not data:
        raise ValueError("median of empty data")
    s = sorted(data)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return float(s[mid])
    return (s[mid - 1] + s[mid]) / 2


def modes(data):
    if not data:
        return []
    counts = {}
    for x in data:
        counts[x] = counts.get(x, 0) + 1
    top = max(counts.values())
    return sorted(k for k, c in counts.items() if c == top)
''',
"explanation": r'''
`sorted` returns a new list so the input is untouched; integer division picks the middle index
and the even case averages two values. `modes` counts frequencies with a dict and keeps every
value tied for the maximum count, sorted for a deterministic answer.
''',
"tests": r'''
class TestMedianMode(unittest.TestCase):
    def test_odd(self):
        self.assertEqual(S.median([7, 1, 3, 3, 100]), 3.0)

    def test_even(self):
        self.assertEqual(S.median([4, 1, 2, 3]), 2.5)

    def test_single(self):
        self.assertEqual(S.median([42]), 42.0)

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.median([])

    def test_not_modified(self):
        d = [3, 1, 2]
        S.median(d)
        self.assertEqual(d, [3, 1, 2])

    def test_modes_tie(self):
        self.assertEqual(S.modes([3, 3, 1, 2, 2]), [2, 3])

    def test_modes_single_and_empty(self):
        self.assertEqual(S.modes([5]), [5])
        self.assertEqual(S.modes([]), [])

    def test_all_unique(self):
        self.assertEqual(S.modes([4, 2, 9]), [2, 4, 9])
''',
"feedback": [
    ("test_odd", "Sort before picking the middle element."),
    ("test_even", "For even n, average the two middle values."),
    ("test_modes_tie", "Return every value tied for the highest count, sorted."),
    ("test_not_modified", "Use sorted(data), not data.sort()."),
],
},
# ---------------------------------------------------------------- histogram-bins
{
"slug": "histogram-bins", "title": "Histogram with Equal-Width Bins",
"difficulty": "beginner", "prereqs": ["mean-variance"], "packages": [],
"objectives": ["Compute equal-width bin edges", "Assign values to bins including the right edge",
               "Handle values outside the range"],
"tags": ["histograms", "binning", "distributions"],
"sources": ["S010", "S007"], "entry": "histogram(data, bins, lo=None, hi=None)",
"article": r'''
# Histograms

## Intuition
A histogram groups numbers into bins (intervals) and counts how many fall in each — a quick
picture of a distribution's shape: where it peaks, how wide it is, whether it is skewed.

## Precise explanation
With range $[\text{lo}, \text{hi}]$ and $k$ bins, width $w = (\text{hi}-\text{lo})/k$ and edges
$e_j = \text{lo} + j w$ for $j = 0..k$. Bin $j$ is the half-open interval $[e_j, e_{j+1})$,
**except the last bin, which is closed** $[e_{k-1}, e_k]$ so the maximum value is counted.
This is the same convention NumPy's `np.histogram` uses.

Index of value $x$: $j = \lfloor (x - \text{lo})/w \rfloor$, then clamp $j = k$ to $k-1$.
Values below lo or above hi are ignored.

If lo/hi are not given, use the data's min and max. If they are equal, the width is zero; a
common convention (used here) is to widen the range to $[\text{lo}-0.5, \text{hi}+0.5]$.

<svg xmlns="http://www.w3.org/2000/svg" width="280" height="150" viewBox="0 0 280 150" role="img" aria-label="Histogram with four bins of heights 2, 5, 3 and 1">
<title>Four-bin histogram</title>
<line x1="20" y1="130" x2="270" y2="130" stroke="#333"/>
<rect x="30" y="90" width="55" height="40" fill="#9ecae1" stroke="#3182bd"/>
<rect x="90" y="30" width="55" height="100" fill="#9ecae1" stroke="#3182bd"/>
<rect x="150" y="70" width="55" height="60" fill="#9ecae1" stroke="#3182bd"/>
<rect x="210" y="110" width="55" height="20" fill="#9ecae1" stroke="#3182bd"/>
<text x="52" y="85" font-size="12">2</text><text x="112" y="25" font-size="12">5</text><text x="172" y="65" font-size="12">3</text><text x="232" y="105" font-size="12">1</text>
</svg>

*Figure (original): counts per bin; the last bin includes its right edge.*

## Worked example
data `[1, 2, 2, 3, 4, 5]`, 2 bins over [1, 5]: width 2, edges [1, 3, 5].
Bin 0 = [1, 3): 1, 2, 2 → 3. Bin 1 = [3, 5]: 3, 4, 5 → 3.

## Common mistakes
* Dropping the maximum value because every bin is half-open.
* Floating-point edges such as 0.1 + 0.2; compute edges as `lo + j*w`.
* Too few/too many bins hiding the shape.

## Why this matters
Histograms are the first look at any feature, the basis of intensity histograms in images
([[intensity-histogram]]), and the binning used in calibration plots.
''',
"statement": r'''
Write `histogram(data, bins, lo=None, hi=None)` returning `(edges, counts)`.

* `edges` has `bins + 1` floats; `counts` has `bins` ints.
* Default `lo = min(data)`, `hi = max(data)`; if `lo == hi`, use `lo - 0.5` and `hi + 0.5`.
* Bins are `[e_j, e_{j+1})` except the last, which includes `hi`. Ignore values outside `[lo, hi]`.
* Raise `ValueError` if `bins < 1`, if `data` is empty and `lo`/`hi` are not both given, or if
  `lo > hi`.

**Examples**
```python
histogram([1, 2, 2, 3, 4, 5], 2)
# ([1.0, 3.0, 5.0], [3, 3])
histogram([0, 10, 11], 2, lo=0, hi=10)
# ([0.0, 5.0, 10.0], [1, 1])   — 11 is outside and ignored; 10 lands in the last bin
```
''',
"starter": r'''
def histogram(data, bins, lo=None, hi=None):
    """Return (edges, counts) for an equal-width histogram."""
    # TODO
    pass
''',
"hints": [
    "Resolve lo/hi defaults first, then `w = (hi - lo) / bins`.",
    "`edges = [lo + j * w for j in range(bins + 1)]`.",
    "For each x in range, `j = int((x - lo) / w)`; if `j == bins` set `j = bins - 1`.",
],
"solution": r'''
def histogram(data, bins, lo=None, hi=None):
    if bins < 1:
        raise ValueError("bins must be >= 1")
    if lo is None or hi is None:
        if not data:
            raise ValueError("empty data needs explicit lo and hi")
        lo = min(data) if lo is None else lo
        hi = max(data) if hi is None else hi
    if lo > hi:
        raise ValueError("lo must be <= hi")
    if lo == hi:
        lo, hi = lo - 0.5, hi + 0.5
    lo, hi = float(lo), float(hi)
    w = (hi - lo) / bins
    edges = [lo + j * w for j in range(bins + 1)]
    edges[-1] = hi
    counts = [0] * bins
    for x in data:
        if x < lo or x > hi:
            continue
        j = int((x - lo) / w)
        if j >= bins:
            j = bins - 1
        counts[j] += 1
    return edges, counts
''',
"explanation": r'''
Defaults and degenerate ranges are resolved before computing the width. Edges are computed by
multiplication (and the last edge pinned to hi to avoid rounding drift). Each in-range value's
bin index is the floor of its scaled position; the value equal to hi would land in a non-existent
bin `bins`, so it is clamped into the last, closed bin.
''',
"tests": r'''
class TestHistogram(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(S.histogram([1, 2, 2, 3, 4, 5], 2), ([1.0, 3.0, 5.0], [3, 3]))

    def test_explicit_range_outside(self):
        self.assertEqual(S.histogram([0, 10, 11], 2, lo=0, hi=10), ([0.0, 5.0, 10.0], [1, 1]))

    def test_max_in_last_bin(self):
        _, c = S.histogram([0, 1, 2, 3, 4], 4)
        self.assertEqual(c, [1, 1, 1, 2])

    def test_constant_data(self):
        e, c = S.histogram([7, 7, 7], 1)
        self.assertEqual(e, [6.5, 7.5])
        self.assertEqual(c, [3])

    def test_counts_sum(self):
        d = [0.1 * i for i in range(101)]
        _, c = S.histogram(d, 7)
        self.assertEqual(sum(c), 101)

    def test_bad_bins(self):
        with self.assertRaises(ValueError):
            S.histogram([1, 2], 0)

    def test_empty_needs_range(self):
        with self.assertRaises(ValueError):
            S.histogram([], 3)
        self.assertEqual(S.histogram([], 2, lo=0, hi=1), ([0.0, 0.5, 1.0], [0, 0]))

    def test_matches_numpy_convention(self):
        e, c = S.histogram([0.0, 0.25, 0.5, 0.75, 1.0], 2)
        self.assertEqual(c, [2, 3])
''',
"feedback": [
    ("test_max_in_last_bin", "The maximum value must go in the last (closed) bin — clamp index bins → bins−1."),
    ("test_explicit_range_outside", "Skip values below lo or above hi."),
    ("test_constant_data", "When lo == hi, widen to [lo−0.5, hi+0.5]."),
    ("test_matches_numpy_convention", "A value exactly on an interior edge belongs to the bin on its right."),
],
},
# ---------------------------------------------------------------- z-scores
{
"slug": "z-scores", "title": "Standardize to z-scores",
"difficulty": "beginner", "prereqs": ["mean-variance"], "packages": [],
"objectives": ["Standardize data", "Interpret z-scores", "Flag outliers with a |z| threshold"],
"tags": ["standardization", "z-score", "outliers"],
"sources": ["S010"], "entry": "z_scores(data, sample=False); outliers(data, threshold=3.0)",
"article": r'''
# z-scores

## Intuition
A z-score answers "how many standard deviations is this value from the mean?" It puts values on
a common, unit-free scale, so a test score and a height can be compared.

## Precise explanation
$$z_i = \frac{x_i - \bar x}{s}$$
where $s$ is the standard deviation (population by default here). Standardized data has mean 0
and standard deviation 1. If all values are equal, $s = 0$ and z-scores are undefined.

**Outlier rule of thumb:** flag values with $|z| > 3$ (or 2.5, 2…). It is a heuristic: in small
samples a single extreme value inflates $s$ and can hide itself (*masking*), which is why robust
alternatives use the median and IQR.

## Worked example
data `[2, 4, 4, 4, 5, 5, 7, 9]`: mean 5, sd 2 → z = `[-1.5, -0.5, -0.5, -0.5, 0, 0, 1, 2]`.

## Common mistakes
* Dividing by the variance instead of the standard deviation.
* Using the sample sd in one place and the population sd elsewhere.
* Not guarding against zero standard deviation.

## Why this matters
Standardization is the default preprocessing for gradient-based models and distance-based models
(k-NN, k-means) so that no feature dominates just because of its units.
''',
"statement": r'''
Implement:
* `z_scores(data, sample=False)` → list of floats; use the population sd unless `sample=True`.
  Raise `ValueError` for empty data or zero standard deviation.
* `outliers(data, threshold=3.0)` → sorted list of **indices** whose population z-score has
  `abs(z) > threshold`.

**Examples**
```python
z_scores([2, 4, 4, 4, 5, 5, 7, 9])   # [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
outliers([10, 11, 9, 10, 50], threshold=1.5)   # [4]
```
''',
"starter": r'''
import math


def z_scores(data, sample=False):
    """Return the z-score of every value."""
    # TODO
    return []


def outliers(data, threshold=3.0):
    """Return indices with |z| > threshold."""
    # TODO
    return []
''',
"hints": [
    "Compute mean and variance (n or n−1), then `sd = math.sqrt(var)`.",
    "Raise ValueError if `sd == 0`.",
    "`[i for i, z in enumerate(z_scores(data)) if abs(z) > threshold]`.",
],
"solution": r'''
import math


def z_scores(data, sample=False):
    n = len(data)
    if n == 0 or (sample and n < 2):
        raise ValueError("not enough data")
    m = sum(data) / n
    var = sum((x - m) ** 2 for x in data) / (n - 1 if sample else n)
    sd = math.sqrt(var)
    if sd == 0:
        raise ValueError("standard deviation is zero")
    return [(x - m) / sd for x in data]


def outliers(data, threshold=3.0):
    return [i for i, z in enumerate(z_scores(data)) if abs(z) > threshold]
''',
"explanation": r'''
The mean and standard deviation are computed once and every value is shifted and scaled. A zero
spread makes standardization meaningless, so it is rejected. `outliers` reuses `z_scores` and
returns indices so the caller can locate the original records.
''',
"tests": r'''
class TestZ(unittest.TestCase):
    def test_example(self):
        z = S.z_scores([2, 4, 4, 4, 5, 5, 7, 9])
        exp = [-1.5, -0.5, -0.5, -0.5, 0.0, 0.0, 1.0, 2.0]
        for a, b in zip(z, exp):
            self.assertAlmostEqual(a, b)

    def test_mean_zero_sd_one(self):
        z = S.z_scores([3.0, -1.0, 8.5, 0.25, 4.0])
        self.assertAlmostEqual(sum(z) / len(z), 0.0, places=12)
        self.assertAlmostEqual(math.sqrt(sum(t * t for t in z) / len(z)), 1.0, places=12)

    def test_sample_variant(self):
        z = S.z_scores([1, 2, 3], sample=True)
        self.assertAlmostEqual(z[0], -1.0)

    def test_constant(self):
        with self.assertRaises(ValueError):
            S.z_scores([5, 5, 5])

    def test_empty(self):
        with self.assertRaises(ValueError):
            S.z_scores([])

    def test_outliers(self):
        self.assertEqual(S.outliers([10, 11, 9, 10, 50], threshold=1.5), [4])

    def test_no_outliers_default(self):
        self.assertEqual(S.outliers([1, 2, 3, 4, 5]), [])
''',
"feedback": [
    ("test_example", "Divide by the standard deviation (sqrt of variance), not the variance."),
    ("test_sample_variant", "With sample=True use n − 1 in the variance."),
    ("test_constant", "Raise ValueError when sd == 0."),
    ("test_outliers", "Return indices, not values, and compare abs(z) > threshold."),
],
},
# ---------------------------------------------------------------- covariance-correlation
{
"slug": "covariance-correlation", "title": "Covariance and Pearson Correlation",
"difficulty": "intermediate", "prereqs": ["z-scores", "dot-product"], "packages": [],
"objectives": ["Compute sample covariance", "Compute Pearson's r and interpret its range",
               "Recognise that correlation measures only linear association"],
"tags": ["covariance", "correlation", "association"],
"sources": ["S003", "S010"], "entry": "covariance(x, y, sample=True); pearson(x, y)",
"article": r'''
# Covariance and Correlation

## Intuition
Do two variables move together? If above-average $x$ tends to come with above-average $y$, the
products of their deviations are mostly positive — positive covariance. Correlation rescales
covariance to $[-1, 1]$ so it no longer depends on units.

## Precise explanation
$$\operatorname{cov}(x,y) = \frac{1}{n-1}\sum (x_i-\bar x)(y_i-\bar y)\quad(\text{sample}),$$
$$r = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sqrt{\sum (x_i-\bar x)^2}\,\sqrt{\sum (y_i-\bar y)^2}}.$$
The $n$ vs $n-1$ factor cancels in $r$. $r = \pm 1$ means a perfect line; $r = 0$ means no
*linear* relationship — $y = x^2$ on symmetric $x$ has $r = 0$ despite perfect dependence.
$r$ is the cosine of the angle between the centred vectors (compare [[dot-product]]).

`statistics.covariance` and `statistics.correlation` (Python 3.10+) implement these.

## Worked example
x = [1, 2, 3, 4], y = [2, 4, 5, 8]: means 2.5 and 4.75; deviation products
(−1.5)(−2.75)+(−0.5)(−0.75)+(0.5)(0.25)+(1.5)(3.25) = 9.5; sample cov = 9.5/3 ≈ 3.167;
Σdx² = 5, Σdy² = 18.75, r = 9.5/√93.75 ≈ 0.981.

## Common mistakes
* Interpreting correlation as causation.
* Ignoring that one outlier can create or destroy a strong r.
* Dividing by zero when one variable is constant (r is undefined).

## Why this matters
Correlated features cause unstable linear-model coefficients (ridge regression helps, [[ridge-regression]]),
and correlation matrices are a standard first exploratory step.
''',
"statement": r'''
Implement:
* `covariance(x, y, sample=True)` — raise `ValueError` if lengths differ, or there are fewer
  than 2 points (sample) / 1 point (population).
* `pearson(x, y)` — raise `ValueError` if lengths differ, `n < 2`, or either variable is constant.

**Examples**
```python
covariance([1, 2, 3, 4], [2, 4, 5, 8])   # 3.1666666666666665
pearson([1, 2, 3, 4], [2, 4, 5, 8])      # 0.9811...
pearson([1, 2, 3], [3, 2, 1])            # -1.0
```
''',
"starter": r'''
import math


def covariance(x, y, sample=True):
    # TODO
    pass


def pearson(x, y):
    # TODO
    pass
''',
"hints": [
    "Compute both means, then `sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))`.",
    "Covariance = `sxy / (n - 1)` (sample) or `/ n`.",
    "r = `sxy / math.sqrt(sxx * syy)`; raise if `sxx` or `syy` is 0.",
],
"solution": r'''
import math


def _centered_sums(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n == 0:
        raise ValueError("empty input")
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return n, sxy, sxx, syy


def covariance(x, y, sample=True):
    n, sxy, _, _ = _centered_sums(x, y)
    if sample and n < 2:
        raise ValueError("need at least two points")
    return sxy / (n - 1 if sample else n)


def pearson(x, y):
    n, sxy, sxx, syy = _centered_sums(x, y)
    if n < 2:
        raise ValueError("need at least two points")
    if sxx == 0 or syy == 0:
        raise ValueError("correlation undefined for a constant variable")
    return sxy / math.sqrt(sxx * syy)
''',
"explanation": r'''
A shared helper computes the centred cross- and self-sums once. Covariance divides the cross-sum
by n or n−1; Pearson's r normalises it by the geometric mean of the self-sums, so the denominator
choice cancels. Constant variables make the denominator zero and are rejected.
''',
"tests": r'''
import statistics

class TestCovCorr(unittest.TestCase):
    def test_cov(self):
        self.assertAlmostEqual(S.covariance([1, 2, 3, 4], [2, 4, 5, 8]), 9.5 / 3, places=12)

    def test_cov_population(self):
        self.assertAlmostEqual(S.covariance([1, 2, 3, 4], [2, 4, 5, 8], sample=False), 9.5 / 4)

    def test_r(self):
        self.assertAlmostEqual(S.pearson([1, 2, 3, 4], [2, 4, 5, 8]), 9.5 / math.sqrt(93.75), places=12)

    def test_perfect_negative(self):
        self.assertAlmostEqual(S.pearson([1, 2, 3], [3, 2, 1]), -1.0)

    def test_nonlinear_zero(self):
        self.assertAlmostEqual(S.pearson([-2, -1, 0, 1, 2], [4, 1, 0, 1, 4]), 0.0)

    def test_constant_raises(self):
        with self.assertRaises(ValueError):
            S.pearson([1, 2, 3], [5, 5, 5])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.covariance([1, 2], [1, 2, 3])

    def test_matches_statistics(self):
        x, y = [0.5, 2.0, 3.5, -1.0, 4.0], [1.0, 1.5, 4.0, -2.0, 3.0]
        self.assertAlmostEqual(S.covariance(x, y), statistics.covariance(x, y), places=12)
        self.assertAlmostEqual(S.pearson(x, y), statistics.correlation(x, y), places=12)

    def test_scale_invariance(self):
        x, y = [1, 3, 2, 5], [2, 1, 4, 3]
        self.assertAlmostEqual(S.pearson(x, y), S.pearson([10 * v + 7 for v in x], y), places=12)
''',
"feedback": [
    ("test_cov", "Sample covariance divides the sum of deviation products by n − 1."),
    ("test_nonlinear_zero", "r measures linear association only; y = x² on symmetric x gives 0."),
    ("test_constant_raises", "A constant variable has zero spread — raise ValueError."),
    ("test_scale_invariance", "Centre both variables before multiplying deviations."),
],
},
# ---------------------------------------------------------------- binomial-pmf
{
"slug": "binomial-pmf", "title": "Binomial Probabilities",
"difficulty": "intermediate", "prereqs": ["probability-basics", "binomial-coefficient"], "packages": [],
"objectives": ["Apply the binomial PMF", "Compute cumulative and tail probabilities",
               "Check that probabilities sum to 1"],
"tags": ["probability", "binomial-distribution", "bernoulli-trials"],
"sources": ["S010", "S011"], "entry": "binom_pmf(k, n, p); binom_cdf(k, n, p); prob_at_least(k, n, p)",
"article": r'''
# The Binomial Distribution

## Intuition
Flip a biased coin $n$ times. The number of heads is random; the binomial distribution says how
likely each count is. Every count $k$ can happen in $\binom{n}{k}$ orders, each with the same
probability.

## Precise explanation
For $n$ independent trials with success probability $p$:
$$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k},\qquad k = 0,\dots,n.$$
Cumulative: $P(X \le k) = \sum_{j=0}^{k} P(X=j)$. Tail: $P(X \ge k) = 1 - P(X \le k-1)$.
Mean $np$, variance $np(1-p)$. Values of $k$ outside $0..n$ have probability 0.

`math.comb(n, k)` gives the binomial coefficient (you implemented it in [[binomial-coefficient]]).
In Python `0 ** 0 == 1`, which correctly handles $p = 0$ or $p = 1$ at the boundaries.

## Worked example
$n = 4$, $p = 0.5$: $P(X=2) = 6 \cdot 0.5^4 = 0.375$.
$P(X \ge 3) = P(3) + P(4) = 4/16 + 1/16 = 0.3125$.

## Common mistakes
* Forgetting the $\binom{n}{k}$ factor (computing one specific sequence).
* Computing $P(X\ge k)$ as $1 - P(X \le k)$ (off by one).
* Not validating $0 \le p \le 1$.

## Why this matters
Accuracy on a test set of $n$ examples is a binomial proportion; A/B tests, dropout masks
([[inverted-dropout]]) and client participation ([[client-sampling]]) are Bernoulli processes.
''',
"statement": r'''
Implement (you may use `math.comb`):
* `binom_pmf(k, n, p)` → $P(X = k)$; returns `0.0` for `k < 0` or `k > n`.
* `binom_cdf(k, n, p)` → $P(X \le k)$ (0.0 if `k < 0`, 1.0 if `k >= n`).
* `prob_at_least(k, n, p)` → $P(X \ge k)$.

Raise `ValueError` if `n < 0` or `p` is outside `[0, 1]`.

**Examples**
```python
binom_pmf(2, 4, 0.5)      # 0.375
prob_at_least(3, 4, 0.5)  # 0.3125
binom_cdf(10, 10, 0.3)    # 1.0
```
''',
"starter": r'''
import math


def binom_pmf(k, n, p):
    # TODO
    pass


def binom_cdf(k, n, p):
    # TODO
    pass


def prob_at_least(k, n, p):
    # TODO
    pass
''',
"hints": [
    "Write a `_check(n, p)` helper that raises ValueError.",
    "pmf: `math.comb(n, k) * p**k * (1 - p)**(n - k)` for 0 ≤ k ≤ n.",
    "cdf sums pmf for j = 0..min(k, n); at_least = 1 − cdf(k − 1).",
],
"solution": r'''
import math


def _check(n, p):
    if n < 0:
        raise ValueError("n must be >= 0")
    if not 0 <= p <= 1:
        raise ValueError("p must be in [0, 1]")


def binom_pmf(k, n, p):
    _check(n, p)
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def binom_cdf(k, n, p):
    _check(n, p)
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return min(1.0, sum(binom_pmf(j, n, p) for j in range(k + 1)))


def prob_at_least(k, n, p):
    _check(n, p)
    return max(0.0, 1.0 - binom_cdf(k - 1, n, p))
''',
"explanation": r'''
The PMF is the formula directly. The CDF sums PMF terms (returning exact 0/1 at the extremes),
and the upper tail uses the complement rule with k − 1 because P(X ≥ k) excludes k − 1 and below.
`min`/`max` clamp tiny floating-point overshoots outside [0, 1].
''',
"tests": r'''
class TestBinom(unittest.TestCase):
    def test_pmf(self):
        self.assertAlmostEqual(S.binom_pmf(2, 4, 0.5), 0.375)

    def test_at_least(self):
        self.assertAlmostEqual(S.prob_at_least(3, 4, 0.5), 0.3125)

    def test_cdf_full(self):
        self.assertEqual(S.binom_cdf(10, 10, 0.3), 1.0)

    def test_out_of_range_k(self):
        self.assertEqual(S.binom_pmf(5, 4, 0.5), 0.0)
        self.assertEqual(S.binom_pmf(-1, 4, 0.5), 0.0)

    def test_sums_to_one(self):
        self.assertAlmostEqual(sum(S.binom_pmf(k, 12, 0.37) for k in range(13)), 1.0, places=12)

    def test_mean(self):
        n, p = 9, 0.2
        self.assertAlmostEqual(sum(k * S.binom_pmf(k, n, p) for k in range(n + 1)), n * p, places=12)

    def test_edge_p(self):
        self.assertEqual(S.binom_pmf(0, 5, 0.0), 1.0)
        self.assertEqual(S.binom_pmf(5, 5, 1.0), 1.0)

    def test_at_least_zero(self):
        self.assertAlmostEqual(S.prob_at_least(0, 7, 0.4), 1.0)

    def test_bad_p(self):
        with self.assertRaises(ValueError):
            S.binom_pmf(1, 3, 1.5)
''',
"feedback": [
    ("test_pmf", "Include the C(n, k) factor."),
    ("test_at_least", "P(X ≥ k) = 1 − P(X ≤ k − 1), not 1 − P(X ≤ k)."),
    ("test_out_of_range_k", "Return 0.0 when k is outside 0..n."),
    ("test_bad_p", "Validate 0 ≤ p ≤ 1."),
],
},
# ---------------------------------------------------------------- dice-lln
{
"slug": "dice-lln", "title": "Dice Simulation and the Law of Large Numbers",
"difficulty": "intermediate", "prereqs": ["probability-basics"], "packages": [],
"objectives": ["Simulate a discrete random variable reproducibly", "Track a running mean",
               "Observe the law of large numbers"],
"tags": ["simulation", "monte-carlo", "law-of-large-numbers", "reproducibility"],
"sources": ["S004", "S010"], "entry": "roll(rng); simulate_two_dice(n, seed)",
"article": r'''
# Simulation and the Law of Large Numbers

## Intuition
The expected sum of two fair dice is 7. Roll them 10 times and the average may be 6.2 or 8.1;
roll them 100 000 times and it will be very close to 7. The **law of large numbers** says sample
averages settle down to the expected value as the sample grows.

## Precise explanation
For i.i.d. $X_i$ with mean $\mu$, the running mean $\bar X_n = \frac1n\sum_{i\le n} X_i$
converges to $\mu$. Its typical error shrinks like $\sigma/\sqrt n$: 100× more rolls ≈ 10× less
error.

**Reproducible randomness.** `random.Random(seed)` creates an independent generator. Python only
guarantees the sequence of `rng.random()` (floats in $[0, 1)$) across versions, so we derive die
faces from it:
$$\text{face} = \lfloor 6u \rfloor + 1,\quad u = \text{rng.random()}.$$
Since $0 \le u < 1$, faces are 1..6 with equal probability.

## Worked example
If the first four `rng.random()` values were 0.10, 0.95, 0.50, 0.33, the faces are 1, 6, 4, 2;
the first two-dice roll sums to 7, the second to 6; running means 7.0, 6.5.

## Common mistakes
* Using the global `random.seed`, which other code can disturb.
* `int(u * 6)` without `+ 1` (faces 0..5) or `round(u * 6)` (faces 0..6 with uneven odds).
* Expecting the running mean to equal exactly 7.

## Why this matters
Monte Carlo simulation estimates quantities that are hard to compute exactly — expected returns
in RL ([[mc-first-visit]]), bootstrap confidence intervals ([[bootstrap-ci]]), dropout's expected behaviour.
''',
"statement": r'''
Implement:
* `roll(rng)` → one die face `int(rng.random() * 6) + 1`, using **only** `rng.random()`.
* `simulate_two_dice(n, seed)` → dict with keys
  * `"sums"`: list of `n` sums, each `roll(rng) + roll(rng)` (first die drawn first),
  * `"running_mean"`: list where element i is the mean of `sums[:i+1]`,
  * `"freq"`: dict mapping each sum 2..12 to its count (all 11 keys present),
  using `rng = random.Random(seed)`. Raise `ValueError` if `n < 1`.

**Examples**
```python
r = simulate_two_dice(5, seed=0)
len(r["sums"]) == 5 and all(2 <= s <= 12 for s in r["sums"])    # True
abs(simulate_two_dice(100000, seed=1)["running_mean"][-1] - 7) < 0.05   # True (LLN)
```
''',
"starter": r'''
import random


def roll(rng):
    """Return one fair die face using only rng.random()."""
    # TODO
    pass


def simulate_two_dice(n, seed):
    # TODO
    return {"sums": [], "running_mean": [], "freq": {}}
''',
"hints": [
    "`int(rng.random() * 6) + 1` maps [0,1) to 1..6.",
    "Keep a running total; running_mean[i] = total / (i + 1).",
    "Initialise `freq = {s: 0 for s in range(2, 13)}`.",
],
"solution": r'''
import random


def roll(rng):
    return int(rng.random() * 6) + 1


def simulate_two_dice(n, seed):
    if n < 1:
        raise ValueError("n must be >= 1")
    rng = random.Random(seed)
    sums, running = [], []
    freq = {s: 0 for s in range(2, 13)}
    total = 0
    for i in range(n):
        s = roll(rng) + roll(rng)
        sums.append(s)
        freq[s] += 1
        total += s
        running.append(total / (i + 1))
    return {"sums": sums, "running_mean": running, "freq": freq}
''',
"explanation": r'''
A private generator seeded once makes the whole simulation reproducible. Each die face comes from
a single `rng.random()` call (the only output Python guarantees across versions). One loop records
the sum, updates the frequency table and the running mean.
''',
"tests": r'''
import random

def _ref(n, seed):
    rng = random.Random(seed)
    return [int(rng.random() * 6) + 1 + int(rng.random() * 6) + 1 for _ in range(n)]

class TestDice(unittest.TestCase):
    def test_roll_range(self):
        rng = random.Random(3)
        faces = {S.roll(rng) for _ in range(2000)}
        self.assertEqual(faces, {1, 2, 3, 4, 5, 6})

    def test_exact_sequence(self):
        self.assertEqual(S.simulate_two_dice(50, seed=42)["sums"], _ref(50, 42))

    def test_reproducible(self):
        self.assertEqual(S.simulate_two_dice(30, 7), S.simulate_two_dice(30, 7))

    def test_running_mean(self):
        r = S.simulate_two_dice(20, seed=5)
        for i in range(20):
            self.assertAlmostEqual(r["running_mean"][i], sum(r["sums"][:i + 1]) / (i + 1))

    def test_freq_keys_and_total(self):
        r = S.simulate_two_dice(500, seed=9)
        self.assertEqual(set(r["freq"]), set(range(2, 13)))
        self.assertEqual(sum(r["freq"].values()), 500)

    def test_lln(self):
        r = S.simulate_two_dice(100000, seed=1)
        self.assertLess(abs(r["running_mean"][-1] - 7), 0.05)

    def test_seven_most_common(self):
        f = S.simulate_two_dice(60000, seed=2)["freq"]
        self.assertEqual(max(f, key=f.get), 7)

    def test_bad_n(self):
        with self.assertRaises(ValueError):
            S.simulate_two_dice(0, 1)
''',
"feedback": [
    ("test_exact_sequence", "Use random.Random(seed) and draw exactly two rng.random() calls per roll, first die first."),
    ("test_roll_range", "Faces must be 1..6: int(u*6) + 1."),
    ("test_freq_keys_and_total", "All sums 2..12 must be keys, even with count 0."),
    ("test_running_mean", "running_mean[i] is the mean of the first i+1 sums."),
],
},
# ---------------------------------------------------------------- percentiles
{
"slug": "percentiles", "title": "Percentiles by Linear Interpolation",
"difficulty": "beginner", "prereqs": ["median-mode"], "packages": [],
"objectives": ["Compute percentiles with linear interpolation", "Compute the IQR",
               "Apply Tukey's fences for outliers"],
"tags": ["percentiles", "quantiles", "iqr", "robust-statistics"],
"sources": ["S010", "S007"], "entry": "percentile(data, q); iqr(data); tukey_outliers(data, k=1.5)",
"article": r'''
# Percentiles and the IQR

## Intuition
The 90th percentile is the value below which 90% of the data falls. Percentiles describe a
distribution without assuming it is bell-shaped, and they are robust to outliers.

## Precise explanation
There are several percentile definitions. We use **linear interpolation between order
statistics** (NumPy's default `method="linear"`): with sorted data $s_0..s_{n-1}$,
$$r = \frac{q}{100}(n-1),\quad i = \lfloor r\rfloor,\quad f = r - i,\quad
P_q = s_i + f\,(s_{i+1} - s_i)$$
(when $i = n-1$ just return $s_{n-1}$). $P_{50}$ is the median.

**IQR** = $P_{75} - P_{25}$, the width of the middle half.
**Tukey's fences:** values below $P_{25} - k\cdot\text{IQR}$ or above $P_{75} + k\cdot\text{IQR}$
($k = 1.5$) are flagged — the rule behind box-plot whiskers.

## Worked example
data [1, 2, 3, 4, 10]: $P_{25}$: r = 1 → 2; $P_{75}$: r = 3 → 4; IQR = 2; fences
[2 − 3, 4 + 3] = [−1, 7] → 10 is an outlier. $P_{40}$: r = 1.6 → 2 + 0.6·1 = 2.6.

## Common mistakes
* Using $q/100 \cdot n$ instead of $(n-1)$ (that is a different definition).
* Forgetting to sort.
* Comparing percentiles computed by different definitions across tools.

## Why this matters
Robust scaling, latency SLOs ("p99 < 200 ms"), box plots and clipping extreme gradient values all
use percentiles.
''',
"statement": r'''
Implement:
* `percentile(data, q)` with the linear method above; `0 <= q <= 100` else `ValueError`;
  empty data → `ValueError`.
* `iqr(data)` → `percentile(data, 75) - percentile(data, 25)`.
* `tukey_outliers(data, k=1.5)` → sorted list of the **values** outside the fences.

**Examples**
```python
percentile([1, 2, 3, 4, 10], 40)   # 2.6
iqr([1, 2, 3, 4, 10])              # 2.0
tukey_outliers([1, 2, 3, 4, 10])   # [10]
```
''',
"starter": r'''
import math


def percentile(data, q):
    # TODO
    pass


def iqr(data):
    # TODO
    pass


def tukey_outliers(data, k=1.5):
    # TODO
    return []
''',
"hints": [
    "`s = sorted(data)`, `r = q / 100 * (len(s) - 1)`.",
    "`i = math.floor(r)`, `f = r - i`; if `i + 1 < len(s)` interpolate, else return `s[i]`.",
    "Fences: `lo = p25 - k * iqr`, `hi = p75 + k * iqr`.",
],
"solution": r'''
import math


def percentile(data, q):
    if not data:
        raise ValueError("empty data")
    if not 0 <= q <= 100:
        raise ValueError("q must be in [0, 100]")
    s = sorted(data)
    r = q / 100 * (len(s) - 1)
    i = math.floor(r)
    f = r - i
    if i + 1 < len(s):
        return s[i] + f * (s[i + 1] - s[i])
    return float(s[i])


def iqr(data):
    return percentile(data, 75) - percentile(data, 25)


def tukey_outliers(data, k=1.5):
    q1, q3 = percentile(data, 25), percentile(data, 75)
    spread = q3 - q1
    lo, hi = q1 - k * spread, q3 + k * spread
    return sorted(x for x in data if x < lo or x > hi)
''',
"explanation": r'''
The fractional rank r locates the percentile between two neighbouring sorted values, and linear
interpolation blends them. The IQR and Tukey fences are built from the 25th and 75th percentiles.
''',
"tests": r'''
class TestPercentile(unittest.TestCase):
    def test_interp(self):
        self.assertAlmostEqual(S.percentile([1, 2, 3, 4, 10], 40), 2.6)

    def test_median(self):
        self.assertAlmostEqual(S.percentile([7, 1, 3, 5], 50), 4.0)

    def test_ends(self):
        self.assertEqual(S.percentile([5, 1, 9], 0), 1)
        self.assertEqual(S.percentile([5, 1, 9], 100), 9)

    def test_single(self):
        self.assertEqual(S.percentile([3], 37), 3.0)

    def test_iqr(self):
        self.assertAlmostEqual(S.iqr([1, 2, 3, 4, 10]), 2.0)

    def test_tukey(self):
        self.assertEqual(S.tukey_outliers([1, 2, 3, 4, 10]), [10])
        self.assertEqual(S.tukey_outliers([-20, 1, 2, 3, 4]), [-20])

    def test_bad_q(self):
        with self.assertRaises(ValueError):
            S.percentile([1, 2], 101)
        with self.assertRaises(ValueError):
            S.percentile([], 50)

    def test_known_values(self):
        d = list(range(1, 11))
        self.assertAlmostEqual(S.percentile(d, 25), 3.25)
        self.assertAlmostEqual(S.percentile(d, 90), 9.1)
''',
"feedback": [
    ("test_interp", "Use rank r = q/100·(n−1) and interpolate between s[i] and s[i+1]."),
    ("test_ends", "q = 100 gives the maximum; guard against indexing s[n]."),
    ("test_known_values", "Make sure you sort the data first."),
    ("test_tukey", "Return the outlying values (sorted), not their indices."),
],
},
# ---------------------------------------------------------------- bootstrap-ci
{
"slug": "bootstrap-ci", "title": "Bootstrap Confidence Interval",
"difficulty": "advanced", "prereqs": ["sampling-distribution", "percentiles"], "packages": [],
"objectives": ["Resample with replacement", "Build a percentile bootstrap interval",
               "Explain what a confidence interval does and does not mean"],
"tags": ["bootstrap", "confidence-interval", "resampling", "inference"],
"sources": ["S010", "S011", "S004"], "entry": "bootstrap_ci(data, n_boot=2000, alpha=0.05, seed=0, stat=None)",
"article": r'''
# The Bootstrap

## Intuition
We have one sample but want to know how much a statistic (e.g. the mean) would vary if we could
collect new samples. The bootstrap pretends the sample *is* the population and draws many
"new" samples from it, with replacement, recomputing the statistic each time. The spread of those
recomputed values estimates the statistic's uncertainty.

## Precise explanation
1. For $b = 1..B$: draw $n$ indices uniformly with replacement, form the resample, compute
   $\hat\theta^*_b$.
2. **Percentile interval** at level $1-\alpha$: the $\alpha/2$ and $1-\alpha/2$ percentiles of
   $\{\hat\theta^*_b\}$.

Index recipe used here (stable across Python versions): `int(rng.random() * n)`, drawn in order
for each position of each resample.

**Interpretation:** a 95% CI procedure captures the true parameter in about 95% of repeated
studies. It is *not* "a 95% probability that the parameter is in this particular interval" (that
is a Bayesian statement).

```mermaid
flowchart LR
  D[original sample n] --> R1[resample 1] --> T1[stat*]
  D --> R2[resample 2] --> T2[stat*]
  D --> RB[resample B] --> TB[stat*]
  T1 & T2 & TB --> P[percentiles α/2, 1−α/2] --> CI[interval]
```

## Worked example
For data [2, 4, 4, 5, 7, 9] (mean 5.17) the reference solution with `seed=0`,
B = 2000 gives a 95% bootstrap CI for the mean of about [3.50, 7.00]; other seeds or B give
slightly different endpoints.

## Common mistakes
* Resampling *without* replacement (that just permutes the data).
* Resamples of a different size than the original.
* Very small B (e.g. 50) — noisy interval endpoints.

## Why this matters
Bootstrapping gives error bars for any metric — accuracy, F1, AUC — without formulas, and it is
the idea behind bagging and random forests.
''',
"statement": r'''
Write `bootstrap_ci(data, n_boot=2000, alpha=0.05, seed=0, stat=None)` returning `(low, high)`.

* `stat` is a function of a list; default is the mean.
* `rng = random.Random(seed)`. For each of `n_boot` resamples, draw `len(data)` indices
  `int(rng.random() * n)` in order.
* Endpoints: percentiles `100*alpha/2` and `100*(1-alpha/2)` of the bootstrap statistics using
  the **linear-interpolation** definition from [[percentiles]].
* Raise `ValueError` if `data` is empty, `n_boot < 1`, or `alpha` not in `(0, 1)`.

**Examples**
```python
lo, hi = bootstrap_ci([2, 4, 4, 5, 7, 9], seed=0)
lo < sum([2, 4, 4, 5, 7, 9]) / 6 < hi     # True
bootstrap_ci([5, 5, 5], seed=1)           # (5.0, 5.0) — no variability
```
''',
"starter": r'''
import math
import random


def bootstrap_ci(data, n_boot=2000, alpha=0.05, seed=0, stat=None):
    # TODO
    pass
''',
"hints": [
    "Default `stat = lambda xs: sum(xs) / len(xs)`.",
    "Resample: `[data[int(rng.random() * n)] for _ in range(n)]`.",
    "Reuse a linear-interpolation percentile helper on the list of bootstrap stats.",
],
"solution": r'''
import math
import random


def _percentile(s_sorted, q):
    r = q / 100 * (len(s_sorted) - 1)
    i = math.floor(r)
    f = r - i
    if i + 1 < len(s_sorted):
        return s_sorted[i] + f * (s_sorted[i + 1] - s_sorted[i])
    return float(s_sorted[i])


def bootstrap_ci(data, n_boot=2000, alpha=0.05, seed=0, stat=None):
    if not data:
        raise ValueError("empty data")
    if n_boot < 1:
        raise ValueError("n_boot must be >= 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be in (0, 1)")
    if stat is None:
        stat = lambda xs: sum(xs) / len(xs)
    rng = random.Random(seed)
    n = len(data)
    boots = []
    for _ in range(n_boot):
        sample = [data[int(rng.random() * n)] for _ in range(n)]
        boots.append(stat(sample))
    boots.sort()
    return float(_percentile(boots, 100 * alpha / 2)), float(_percentile(boots, 100 * (1 - alpha / 2)))
''',
"explanation": r'''
Each bootstrap replicate resamples n values with replacement using the documented index recipe
and records the statistic. Sorting the replicates and reading off the α/2 and 1−α/2 percentiles
gives the percentile interval.
''',
"tests": r'''
import random
import statistics

def _ref(data, n_boot, alpha, seed):
    rng = random.Random(seed)
    n = len(data)
    b = sorted(sum(data[int(rng.random() * n)] for _ in range(n)) / n for _ in range(n_boot))
    def pct(q):
        r = q / 100 * (len(b) - 1); i = math.floor(r); f = r - i
        return b[i] + f * (b[i + 1] - b[i]) if i + 1 < len(b) else b[i]
    return pct(100 * alpha / 2), pct(100 * (1 - alpha / 2))

DATA = [2, 4, 4, 5, 7, 9]

class TestBootstrap(unittest.TestCase):
    def test_contains_mean(self):
        lo, hi = S.bootstrap_ci(DATA, seed=0)
        self.assertLess(lo, sum(DATA) / 6)
        self.assertGreater(hi, sum(DATA) / 6)

    def test_exact_recipe(self):
        got = S.bootstrap_ci(DATA, n_boot=500, alpha=0.1, seed=3)
        exp = _ref(DATA, 500, 0.1, 3)
        self.assertAlmostEqual(got[0], exp[0], places=12)
        self.assertAlmostEqual(got[1], exp[1], places=12)

    def test_constant(self):
        self.assertEqual(S.bootstrap_ci([5, 5, 5], seed=1), (5.0, 5.0))

    def test_reproducible(self):
        self.assertEqual(S.bootstrap_ci(DATA, seed=11), S.bootstrap_ci(DATA, seed=11))

    def test_wider_at_higher_confidence(self):
        lo90, hi90 = S.bootstrap_ci(DATA, alpha=0.10, seed=4)
        lo99, hi99 = S.bootstrap_ci(DATA, alpha=0.01, seed=4)
        self.assertLessEqual(lo99, lo90)
        self.assertGreaterEqual(hi99, hi90)

    def test_custom_stat(self):
        lo, hi = S.bootstrap_ci(DATA, seed=2, stat=statistics.median)
        self.assertTrue(lo <= 4.5 <= hi)

    def test_bad_args(self):
        with self.assertRaises(ValueError):
            S.bootstrap_ci([], seed=0)
        with self.assertRaises(ValueError):
            S.bootstrap_ci(DATA, alpha=1.0)
''',
"feedback": [
    ("test_exact_recipe", "Draw indices with int(rng.random()*n), n per resample, in order; sort the stats; use linear percentiles."),
    ("test_constant", "Constant data gives identical bootstrap stats; both endpoints equal the value."),
    ("test_wider_at_higher_confidence", "Lower alpha → percentiles further into the tails."),
    ("test_custom_stat", "Apply the provided stat function to each resample."),
],
},
# ---------------------------------------------------------------- chi-square-gof
{
"slug": "chi-square-gof", "title": "Chi-Square Goodness of Fit by Hand", "optional": True,
"difficulty": "advanced", "prereqs": ["binomial-pmf"], "packages": [],
"objectives": ["Compute expected counts from probabilities", "Compute the chi-square statistic and degrees of freedom",
               "Make a decision with a critical value"],
"tags": ["hypothesis-testing", "chi-square", "categorical-data"],
"sources": ["S011", "S010"], "entry": "chi_square_gof(observed, probs, critical=None)",
"article": r'''
# Chi-Square Goodness of Fit

## Intuition
Is a die fair? Roll it 60 times; a fair die should show each face about 10 times. The chi-square
statistic adds up how far each observed count is from its expected count, scaled by the expected
count, so that a gap of 5 matters more when you expected 10 than when you expected 1000.

## Precise explanation
With observed counts $O_i$ over $k$ categories, total $N = \sum O_i$, and hypothesised
probabilities $p_i$ (summing to 1), expected counts are $E_i = N p_i$ and
$$\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i},\qquad \text{df} = k - 1.$$
Under the null hypothesis (the probabilities are right), $\chi^2$ approximately follows a
chi-square distribution with df degrees of freedom. Reject at level α if $\chi^2$ exceeds the
critical value (e.g. 11.070 for df = 5, α = 0.05 — from standard tables).

Rule of thumb: every $E_i$ should be at least 5 for the approximation to be reliable.

## Worked example
Die rolled 60 times: O = [5, 8, 9, 8, 10, 20], E = 10 each.
χ² = (25 + 4 + 1 + 4 + 0 + 100)/10 = 13.4, df = 5 > 11.07 → reject fairness at 5%.

## Common mistakes
* Using proportions instead of counts.
* Dividing by $O_i$ instead of $E_i$.
* df = k instead of k − 1.

## Why this matters
Chi-square tests check categorical feature/label dependence (feature selection), detect drift in
class frequencies, and test random-number generators.
''',
"statement": r'''
Write `chi_square_gof(observed, probs, critical=None)` returning a dict
`{"statistic": float, "df": int, "expected": list[float], "reject": bool | None}`.

* `reject` is `statistic > critical` if `critical` is given, else `None`.
* Raise `ValueError` if lengths differ, fewer than 2 categories, any prob ≤ 0, probs don't sum to
  1 within 1e-9, any observed count is negative, or the total count is 0.

**Examples**
```python
chi_square_gof([5, 8, 9, 8, 10, 20], [1/6]*6, critical=11.070)
# {'statistic': 13.4, 'df': 5, 'expected': [10.0]*6, 'reject': True}
chi_square_gof([50, 50], [0.5, 0.5])
# {'statistic': 0.0, 'df': 1, 'expected': [50.0, 50.0], 'reject': None}
```
''',
"starter": r'''
def chi_square_gof(observed, probs, critical=None):
    # TODO
    pass
''',
"hints": [
    "Validate inputs, then `N = sum(observed)` and `expected = [N * p for p in probs]`.",
    "`stat = sum((o - e) ** 2 / e for o, e in zip(observed, expected))`.",
    "`df = len(observed) - 1`.",
],
"solution": r'''
def chi_square_gof(observed, probs, critical=None):
    if len(observed) != len(probs):
        raise ValueError("observed and probs must match in length")
    if len(observed) < 2:
        raise ValueError("need at least two categories")
    if any(p <= 0 for p in probs) or abs(sum(probs) - 1) > 1e-9:
        raise ValueError("probs must be positive and sum to 1")
    if any(o < 0 for o in observed):
        raise ValueError("counts must be non-negative")
    total = sum(observed)
    if total == 0:
        raise ValueError("total count is zero")
    expected = [total * p for p in probs]
    stat = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    return {"statistic": stat, "df": len(observed) - 1, "expected": expected,
            "reject": None if critical is None else stat > critical}
''',
"explanation": r'''
After validation, expected counts are the total times each probability. The statistic sums the
squared gaps scaled by expected counts; df is one less than the number of categories because the
counts are constrained to sum to N. The optional critical value turns the statistic into a decision.
''',
"tests": r'''
class TestChi(unittest.TestCase):
    def test_die(self):
        r = S.chi_square_gof([5, 8, 9, 8, 10, 20], [1 / 6] * 6, critical=11.070)
        self.assertAlmostEqual(r["statistic"], 13.4, places=9)
        self.assertEqual(r["df"], 5)
        self.assertTrue(r["reject"])
        for e in r["expected"]:
            self.assertAlmostEqual(e, 10.0)

    def test_perfect_fit(self):
        r = S.chi_square_gof([50, 50], [0.5, 0.5])
        self.assertEqual(r["statistic"], 0.0)
        self.assertIsNone(r["reject"])

    def test_not_reject(self):
        r = S.chi_square_gof([18, 22, 20], [1 / 3] * 3, critical=5.991)
        self.assertAlmostEqual(r["statistic"], 0.4)
        self.assertFalse(r["reject"])

    def test_unequal_probs(self):
        r = S.chi_square_gof([30, 50, 20], [0.25, 0.5, 0.25])
        self.assertAlmostEqual(r["statistic"], (25 / 25) + 0 + (25 / 25))

    def test_bad_probs(self):
        with self.assertRaises(ValueError):
            S.chi_square_gof([1, 2], [0.5, 0.6])

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            S.chi_square_gof([1, 2, 3], [0.5, 0.5])

    def test_zero_total(self):
        with self.assertRaises(ValueError):
            S.chi_square_gof([0, 0], [0.5, 0.5])
''',
"feedback": [
    ("test_die", "Divide each squared difference by the expected count, and df = k − 1."),
    ("test_unequal_probs", "Expected counts are N × p_i for each category."),
    ("test_bad_probs", "Check that probs sum to 1 (within 1e-9)."),
    ("test_not_reject", "reject is statistic > critical."),
],
},
# ---------------------------------------------------------------- welch-t
{
"slug": "welch-t", "title": "Welch's t-statistic by Hand", "optional": True,
"difficulty": "advanced", "prereqs": ["sampling-distribution"], "packages": [],
"objectives": ["Compute the standard error of a mean difference", "Compute Welch's t and Welch–Satterthwaite df",
               "Explain why Welch is preferred when variances differ"],
"tags": ["hypothesis-testing", "t-test", "two-sample", "standard-error"],
"sources": ["S011", "S010"], "entry": "welch_t(x, y)",
"article": r'''
# Comparing Two Means: Welch's t

## Intuition
Model A scores 0.82 on average across runs, model B 0.79. Is A really better, or is the gap just
noise? The t-statistic compares the difference in means to how much that difference would wobble
by chance (its standard error).

## Precise explanation
With sample means $\bar x, \bar y$, sample variances $s_x^2, s_y^2$ (n−1 denominators), sizes
$n_x, n_y$:
$$t = \frac{\bar x - \bar y}{\sqrt{s_x^2/n_x + s_y^2/n_y}}.$$
Welch's test does **not** assume equal variances. Its approximate degrees of freedom
(Welch–Satterthwaite):
$$\nu = \frac{\left(s_x^2/n_x + s_y^2/n_y\right)^2}{\dfrac{(s_x^2/n_x)^2}{n_x-1} + \dfrac{(s_y^2/n_y)^2}{n_y-1}}.$$
Large $|t|$ (compared with a t-distribution with ν df; roughly $|t| > 2$ for moderate ν at 5%)
suggests a real difference. ν is usually not an integer.

## Worked example
x = [1, 2, 3, 4, 5] (mean 3, s² 2.5), y = [3, 4, 5, 6, 7] (mean 5, s² 2.5):
SE = √(0.5 + 0.5) = 1, t = −2, ν = 1/(0.0625 + 0.0625) = 8.

## Common mistakes
* Using population variances.
* Pooling variances (Student's t) when spreads clearly differ.
* Reading "not significant" as "no difference".

## Why this matters
Comparing models across random seeds or cross-validation folds ([[k-fold-cv]]) calls for exactly this
kind of test — with care about non-independence of folds.
''',
"statement": r'''
Write `welch_t(x, y)` returning `(t, df)` as floats.

* Both samples need at least 2 values, else `ValueError`.
* If both sample variances are 0, raise `ValueError` (standard error is zero).

**Examples**
```python
welch_t([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])   # (-2.0, 8.0)
welch_t([10, 12, 14], [1, 2, 3, 4, 5, 6])   # (≈ 6.140, ≈ 3.839)
```
''',
"starter": r'''
import math


def welch_t(x, y):
    # TODO
    pass
''',
"hints": [
    "Write `_mean_var(a)` returning the mean and sample variance.",
    "`vx = sx2 / nx`, `vy = sy2 / ny`, `t = (mx - my) / math.sqrt(vx + vy)`.",
    "`df = (vx + vy) ** 2 / (vx ** 2 / (nx - 1) + vy ** 2 / (ny - 1))`.",
],
"solution": r'''
import math


def _mean_var(a):
    n = len(a)
    if n < 2:
        raise ValueError("each sample needs at least two values")
    m = sum(a) / n
    return m, sum((v - m) ** 2 for v in a) / (n - 1), n


def welch_t(x, y):
    mx, sx2, nx = _mean_var(x)
    my, sy2, ny = _mean_var(y)
    vx, vy = sx2 / nx, sy2 / ny
    if vx + vy == 0:
        raise ValueError("both samples have zero variance")
    t = (mx - my) / math.sqrt(vx + vy)
    df = (vx + vy) ** 2 / (vx ** 2 / (nx - 1) + vy ** 2 / (ny - 1))
    return t, df
''',
"explanation": r'''
Each group's squared standard error of the mean is its sample variance over its size. Their sum
is the variance of the difference in means; t divides the observed difference by its square
root. The Welch–Satterthwaite formula combines the two contributions into an effective df.
''',
"tests": r'''
class TestWelch(unittest.TestCase):
    def test_symmetric_example(self):
        t, df = S.welch_t([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
        self.assertAlmostEqual(t, -2.0)
        self.assertAlmostEqual(df, 8.0)

    def test_unequal(self):
        t, df = S.welch_t([10, 12, 14], [1, 2, 3, 4, 5, 6])
        vx, vy = 4 / 3, 3.5 / 6
        self.assertAlmostEqual(t, 8.5 / math.sqrt(vx + vy), places=10)
        self.assertAlmostEqual(df, (vx + vy) ** 2 / (vx ** 2 / 2 + vy ** 2 / 5), places=10)

    def test_antisymmetric(self):
        a, b = [2.0, 3.5, 4.0, 1.0], [5.0, 6.5, 4.5]
        t1, d1 = S.welch_t(a, b)
        t2, d2 = S.welch_t(b, a)
        self.assertAlmostEqual(t1, -t2)
        self.assertAlmostEqual(d1, d2)

    def test_same_means(self):
        t, _ = S.welch_t([1, 2, 3], [0, 2, 4])
        self.assertAlmostEqual(t, 0.0)

    def test_too_small(self):
        with self.assertRaises(ValueError):
            S.welch_t([1], [2, 3])

    def test_zero_variance(self):
        with self.assertRaises(ValueError):
            S.welch_t([2, 2], [2, 2])

    def test_one_zero_variance_ok(self):
        t, df = S.welch_t([5, 5, 5], [1, 2, 3])
        self.assertAlmostEqual(t, 3 / math.sqrt(1 / 3))
        self.assertAlmostEqual(df, 2.0)
''',
"feedback": [
    ("test_symmetric_example", "Use sample variances (n − 1) divided by each sample size."),
    ("test_unequal", "Do not pool variances; Welch keeps them separate."),
    ("test_one_zero_variance_ok", "Only raise when *both* variances are zero."),
    ("test_too_small", "Each sample needs n ≥ 2."),
],
},
# ---------------------------------------------------------------- permutation-test
{
"slug": "permutation-test", "title": "Permutation Test for a Mean Difference by Hand", "optional": True,
"difficulty": "advanced", "prereqs": ["bootstrap-ci", "welch-t"], "packages": [],
"objectives": ["State a null hypothesis as exchangeability", "Implement a seeded Fisher–Yates shuffle",
               "Compute a two-sided permutation p-value with the +1 correction"],
"tags": ["hypothesis-testing", "permutation-test", "p-value", "shuffling"],
"sources": ["S010", "S004"], "entry": "fisher_yates(items, rng); permutation_test(x, y, n_perm=5000, seed=0)",
"article": r'''
# Permutation Tests

## Intuition
If the group labels "A" and "B" don't matter (the null hypothesis), then shuffling the labels
should produce differences in means just as large as the one we observed, fairly often. If
almost no shuffle produces a difference as extreme as the real one, the labels probably *do*
matter.

## Precise explanation
1. Observed statistic $d_\text{obs} = \bar x - \bar y$.
2. Pool all values. For $b = 1..B$: shuffle the pool, call the first $n_x$ values "x" and the
   rest "y", compute $d_b$.
3. Two-sided p-value with the standard +1 correction (counts the observed arrangement, never 0):
$$p = \frac{1 + \#\{b: |d_b| \ge |d_\text{obs}|\}}{B + 1}.$$

**Fisher–Yates shuffle** (uniform over permutations) using only `rng.random()`:
```text
for i from n-1 down to 1:
    j = int(rng.random() * (i + 1))   # 0 <= j <= i
    swap items[i], items[j]
```
Floating-point noise can make $|d_b|$ differ from $|d_\text{obs}|$ in the last bits even for
identical arrangements; compare with a small tolerance (`>= abs_obs - 1e-12`).

## Worked example
x = [5, 6, 7], y = [1, 2, 3]: $d_\text{obs} = 4$. Only the 2 of the 20 equally likely splits
(x and y swapped) are as extreme, so the exact p-value is 2/20 = 0.1; a Monte Carlo estimate
with many shuffles is close to 0.1.

## Common mistakes
* Shuffling `x` and `y` separately (labels never move).
* Biased shuffles such as `j = int(rng.random() * n)` for every i.
* Reporting p = 0.

## Why this matters
Permutation tests make almost no distributional assumptions; they also underlie permutation
feature importance ([[permutation-importance]]), where shuffling a feature breaks its link with the target.
''',
"statement": r'''
Implement:
* `fisher_yates(items, rng)` → a **new** shuffled list using exactly the recipe above
  (input unchanged).
* `permutation_test(x, y, n_perm=5000, seed=0)` → dict `{"observed": d_obs, "p_value": p}`.
  Use `rng = random.Random(seed)`; each permutation shuffles the pooled list `x + y` with
  `fisher_yates` (starting from the original pool each time). Count `abs(d_b) >= abs(d_obs) - 1e-12`.
  Raise `ValueError` if either group is empty or `n_perm < 1`.

**Examples**
```python
r = permutation_test([5, 6, 7], [1, 2, 3], n_perm=4000, seed=0)
r["observed"]                      # 4.0
abs(r["p_value"] - 0.1) < 0.02     # True
permutation_test([1, 2, 3], [1, 2, 3], n_perm=100)["p_value"]   # 1.0
```
''',
"starter": r'''
import random


def fisher_yates(items, rng):
    # TODO
    return list(items)


def permutation_test(x, y, n_perm=5000, seed=0):
    # TODO
    pass
''',
"hints": [
    "Copy first: `a = list(items)`, then loop `for i in range(len(a) - 1, 0, -1)`.",
    "`j = int(rng.random() * (i + 1))`; `a[i], a[j] = a[j], a[i]`.",
    "Split each shuffled pool into `p[:nx]` and `p[nx:]` and compare absolute differences.",
],
"solution": r'''
import random


def fisher_yates(items, rng):
    a = list(items)
    for i in range(len(a) - 1, 0, -1):
        j = int(rng.random() * (i + 1))
        a[i], a[j] = a[j], a[i]
    return a


def permutation_test(x, y, n_perm=5000, seed=0):
    if not x or not y:
        raise ValueError("both groups must be non-empty")
    if n_perm < 1:
        raise ValueError("n_perm must be >= 1")
    nx = len(x)
    d_obs = sum(x) / nx - sum(y) / len(y)
    pool = list(x) + list(y)
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        p = fisher_yates(pool, rng)
        d = sum(p[:nx]) / nx - sum(p[nx:]) / (len(p) - nx)
        if abs(d) >= abs(d_obs) - 1e-12:
            hits += 1
    return {"observed": d_obs, "p_value": (hits + 1) / (n_perm + 1)}
''',
"explanation": r'''
The Fisher–Yates loop picks each position's element uniformly from the not-yet-fixed prefix,
giving every permutation equal probability. Each permutation reassigns labels at random; the
fraction of shuffles at least as extreme as the observed difference (plus the observed
arrangement itself) is the p-value.
''',
"tests": r'''
import random

class TestPermutation(unittest.TestCase):
    def test_fy_recipe(self):
        rng = random.Random(0)
        a = [0, 1, 2, 3, 4]
        for i in range(4, 0, -1):
            j = int(rng.random() * (i + 1)); a[i], a[j] = a[j], a[i]
        self.assertEqual(S.fisher_yates([0, 1, 2, 3, 4], random.Random(0)), a)

    def test_fy_is_permutation_and_copy(self):
        items = list(range(20))
        out = S.fisher_yates(items, random.Random(5))
        self.assertEqual(sorted(out), items)
        self.assertEqual(items, list(range(20)))

    def test_fy_uniform_first_position(self):
        rng = random.Random(1)
        counts = [0, 0, 0]
        for _ in range(30000):
            counts[S.fisher_yates([0, 1, 2], rng)[0]] += 1
        for c in counts:
            self.assertAlmostEqual(c / 30000, 1 / 3, delta=0.015)

    def test_exact_p_approx(self):
        r = S.permutation_test([5, 6, 7], [1, 2, 3], n_perm=4000, seed=0)
        self.assertAlmostEqual(r["observed"], 4.0)
        self.assertAlmostEqual(r["p_value"], 0.1, delta=0.02)

    def test_identical_groups(self):
        self.assertEqual(S.permutation_test([1, 2, 3], [1, 2, 3], n_perm=100)["p_value"], 1.0)

    def test_p_never_zero(self):
        r = S.permutation_test([100, 101, 102, 103], [0, 1, 2, 3], n_perm=10, seed=3)
        self.assertGreater(r["p_value"], 0)

    def test_bad(self):
        with self.assertRaises(ValueError):
            S.permutation_test([], [1])
''',
"feedback": [
    ("test_fy_recipe", "Loop i from n−1 down to 1 and use j = int(rng.random()*(i+1))."),
    ("test_fy_uniform_first_position", "A biased shuffle (j over the whole list) fails this check."),
    ("test_identical_groups", "Use abs(d) >= abs(d_obs) − 1e-12 so ties count."),
    ("test_p_never_zero", "Use (hits + 1) / (n_perm + 1)."),
],
},
]
