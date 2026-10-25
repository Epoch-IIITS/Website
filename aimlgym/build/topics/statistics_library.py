"""Statistics with scipy.stats (library revision, Phase 1).

These steps use SciPy for the tests built by hand in [[chi-square-gof]], [[welch-t]] and
[[permutation-test]], which follow each library step as optional deep dives.
"""

PROBLEMS = [
# ---------------------------------------------------------------- scipy-stats-intro
{
"slug": "scipy-stats-intro", "title": "Introducing scipy.stats",
"difficulty": "advanced", "prereqs": ["normal-distribution"], "packages": ["numpy", "scipy"],
"objectives": ["Create frozen distribution objects with scipy.stats.norm and scipy.stats.binom",
               "Use pdf/pmf, cdf, ppf, mean and std on a distribution object",
               "Check library results against the formulas you implemented by hand"],
"tags": ["scipy", "distributions", "normal", "binomial", "quantiles"],
"sources": ["S101", "S010"], "entry": "distribution_facts(kind, params, x, q)",
"article": r'''
# Introducing scipy.stats

## Intuition
In [[binomial-pmf]] and [[normal-distribution]] you wrote the probability formulas yourself. In
practice you reach for `scipy.stats`: one object per distribution that knows its density,
cumulative probability, quantiles, mean and spread, tested by thousands of users. Knowing the
formulas lets you check the library; knowing the library saves you from re-deriving them.

## Precise explanation
`scipy.stats` provides distribution families. Calling a family with its parameters returns a
**frozen** distribution:

```python
from scipy import stats
heights = stats.norm(loc=170, scale=10)   # normal, mean 170, standard deviation 10
coins = stats.binom(n=10, p=0.5)          # number of heads in 10 fair flips
```

| Method | Continuous (`norm`) | Discrete (`binom`) |
|---|---|---|
| density | `pdf(x)` — probability density | `pmf(k)` — P(X = k) |
| `cdf(x)` | P(X ≤ x) | P(X ≤ k) |
| `ppf(q)` | the x with cdf(x) = q (inverse cdf, the quantile) | smallest k with cdf(k) ≥ q |
| `sf(x)` | 1 − cdf(x), the upper tail, computed accurately | same |
| `mean()`, `std()` | μ, σ | np, √(np(1−p)) |

`loc` and `scale` are SciPy's general names for shift and stretch; for the normal they are μ and σ.
Results are NumPy floats; wrap them in `float()` when you need plain Python numbers.

## Worked example
```python
stats.norm(170, 10).cdf(180)     # 0.8413...: 84% of heights are below 180
stats.norm(170, 10).ppf(0.975)   # 189.6: 97.5% are below this
stats.binom(10, 0.5).pmf(5)      # 0.24609375 = C(10,5) / 2**10
stats.binom(10, 0.5).ppf(0.5)    # 5.0: the median number of heads
```

## What the library does inside
`norm.cdf` evaluates the same error-function formula as [[normal-distribution]], using special
functions that stay accurate far in the tails; `binom.pmf` evaluates C(n, k)pᵏ(1−p)ⁿ⁻ᵏ from
[[binomial-pmf]] in log space so large n does not overflow. `ppf` inverts the cdf numerically.

## Common mistakes
* Passing the variance as `scale`: `scale` is the standard deviation.
* Calling `pdf` on a discrete distribution: discrete ones have `pmf`.
* Using `1 - cdf(x)` for tiny tail probabilities: `sf(x)` keeps precision.
* Forgetting that `ppf` of a discrete distribution returns a float (`5.0`), not an `int`.

## Why this matters
Every test in the next steps turns a statistic into a p-value through one of these objects, and
machine-learning code uses them to sample noise, set priors and compute confidence intervals.
''',
"statement": r'''
Write `distribution_facts(kind, params, x, q)` returning a dict of plain floats
`{"density": ..., "cdf": ..., "quantile": ..., "mean": ..., "std": ...}`.

* `kind="norm"`: `params = (mu, sigma)`; density is the pdf at `x`.
* `kind="binom"`: `params = (n, p)`; density is the pmf at `x`.
* `cdf` is evaluated at `x`, `quantile` is the ppf at `q`.
* Raise `ValueError` for an unknown kind, `sigma <= 0`, `n < 0`, `p` outside [0, 1], or `q` not
  strictly between 0 and 1.

Use `scipy.stats`.

**Examples**
```python
distribution_facts("norm", (170, 10), 180, 0.975)
# {'density': 0.0241..., 'cdf': 0.8413..., 'quantile': 189.59..., 'mean': 170.0, 'std': 10.0}
distribution_facts("binom", (10, 0.5), 5, 0.5)
# {'density': 0.24609375, 'cdf': 0.623046875, 'quantile': 5.0, 'mean': 5.0, 'std': 1.5811...}
```
''',
"starter": r'''
from scipy import stats


def distribution_facts(kind, params, x, q):
    # TODO: build a frozen distribution, then read its facts
    pass
''',
"hints": [
    "Validate first, then build `dist = stats.norm(loc=mu, scale=sigma)` or `stats.binom(n, p)`.",
    "The density method is `dist.pdf(x)` for the normal and `dist.pmf(x)` for the binomial.",
    "Convert every result with `float(...)` before putting it in the dict.",
],
"solution": r'''
from scipy import stats


def distribution_facts(kind, params, x, q):
    if not 0 < q < 1:
        raise ValueError("q must be strictly between 0 and 1")
    if kind == "norm":
        mu, sigma = params
        if sigma <= 0:
            raise ValueError("sigma must be positive")
        dist = stats.norm(loc=mu, scale=sigma)
        density = dist.pdf(x)
    elif kind == "binom":
        n, p = params
        if n < 0 or not 0 <= p <= 1:
            raise ValueError("need n >= 0 and 0 <= p <= 1")
        dist = stats.binom(n, p)
        density = dist.pmf(x)
    else:
        raise ValueError("kind must be 'norm' or 'binom'")
    return {"density": float(density), "cdf": float(dist.cdf(x)), "quantile": float(dist.ppf(q)),
            "mean": float(dist.mean()), "std": float(dist.std())}
''',
"explanation": r'''
The frozen distribution holds the parameters, so every fact is one method call. Only the density
method differs between continuous (`pdf`) and discrete (`pmf`) families. Validation happens before
SciPy is called, because SciPy returns `nan` for invalid parameters instead of raising.
''',
"tests": r'''
class TestDistributionFacts(unittest.TestCase):
    def test_normal_matches_formulas(self):
        r = S.distribution_facts("norm", (170, 10), 180, 0.975)
        self.assertAlmostEqual(r["cdf"], 0.5 * (1 + math.erf(1 / math.sqrt(2))), places=10)
        self.assertAlmostEqual(r["density"], math.exp(-0.5) / (10 * math.sqrt(2 * math.pi)), places=12)
        self.assertAlmostEqual(r["quantile"], 170 + 10 * 1.959963984540054, places=6)

    def test_binomial_matches_formulas(self):
        r = S.distribution_facts("binom", (10, 0.5), 5, 0.5)
        self.assertAlmostEqual(r["density"], math.comb(10, 5) / 2 ** 10, places=12)
        self.assertAlmostEqual(r["cdf"], sum(math.comb(10, k) for k in range(6)) / 2 ** 10, places=12)
        self.assertEqual(r["quantile"], 5.0)

    def test_mean_and_std(self):
        r = S.distribution_facts("binom", (20, 0.3), 6, 0.5)
        self.assertAlmostEqual(r["mean"], 6.0)
        self.assertAlmostEqual(r["std"], math.sqrt(20 * 0.3 * 0.7))

    def test_plain_floats(self):
        r = S.distribution_facts("norm", (0, 1), 0, 0.5)
        self.assertEqual(set(r), {"density", "cdf", "quantile", "mean", "std"})
        self.assertTrue(all(type(v) is float for v in r.values()))
        self.assertAlmostEqual(r["quantile"], 0.0)

    def test_standard_normal_symmetry(self):
        low = S.distribution_facts("norm", (0, 1), -1.5, 0.1)
        high = S.distribution_facts("norm", (0, 1), 1.5, 0.9)
        self.assertAlmostEqual(low["cdf"] + high["cdf"], 1.0, places=12)
        self.assertAlmostEqual(low["quantile"], -high["quantile"], places=9)

    def test_invalid_parameters(self):
        for args in [("norm", (0, 0), 0, 0.5), ("binom", (10, 1.5), 1, 0.5), ("binom", (-1, 0.5), 0, 0.5),
                     ("norm", (0, 1), 0, 1.0), ("poisson", (3,), 1, 0.5)]:
            with self.assertRaises(ValueError):
                S.distribution_facts(*args)
''',
"feedback": [
    ("test_normal_matches_formulas", "`scale` is the standard deviation σ, and ppf takes a probability q."),
    ("test_binomial_matches_formulas", "Discrete distributions use `pmf`, not `pdf`."),
    ("test_plain_floats", "Wrap SciPy results in `float(...)`."),
    ("test_invalid_parameters", "Check the parameters yourself before calling SciPy; it returns nan instead of raising."),
],
},
# ---------------------------------------------------------------- chi-square-scipy
{
"slug": "chi-square-scipy", "title": "Chi-Square Test with SciPy",
"difficulty": "advanced", "prereqs": ["scipy-stats-intro"], "packages": ["numpy", "scipy"],
"objectives": ["Run a goodness-of-fit test with scipy.stats.chisquare",
               "Interpret a p-value and compare it with a significance level",
               "Relate the p-value to the chi-square distribution's upper tail"],
"tags": ["scipy", "hypothesis-testing", "chi-square", "p-value"],
"sources": ["S101", "S011"], "entry": "chi_square_test(observed, probs, alpha=0.05)",
"article": r'''
# Chi-Square Test with SciPy

## Intuition
A chi-square statistic says how far observed counts are from expected counts. On its own, 13.4
means little. The **p-value** turns it into a probability: if the hypothesised probabilities were
right, how often would random counts look at least this far off?

## Precise explanation
`scipy.stats.chisquare(f_obs, f_exp)` returns the statistic $\chi^2 = \sum (O_i - E_i)^2 / E_i$
and its p-value with $k - 1$ degrees of freedom:

```python
from scipy import stats
result = stats.chisquare([5, 8, 9, 8, 10, 20], f_exp=[10] * 6)
result.statistic   # 13.4
result.pvalue      # 0.0199
```

`f_exp` must be **counts** with the same total as `f_obs` (multiply probabilities by the total);
omitting it means "all categories equally likely". The p-value is the chi-square distribution's
upper tail, `stats.chi2(df).sf(statistic)`. With significance level α, reject the null hypothesis
when p < α. A p-value is **not** the probability that the null hypothesis is true.

## Worked example
For the die above, p ≈ 0.020. At α = 0.05 we reject fairness; at α = 0.01 we do not. The
evidence is the same; the decision depends on how strict the threshold is.

## What the library does inside
`chisquare` computes the same sum as your function in [[chi-square-gof]], which follows as an
optional deep dive, then calls the chi-square survival function instead of reading a table of
critical values. It also checks that observed and expected totals agree.

## Common mistakes
* Passing probabilities as `f_exp`: SciPy expects expected counts.
* Using proportions instead of counts for `f_obs`; the test needs the sample size.
* Rejecting when p > α, or reading 1 − p as the probability the hypothesis is false.
* Testing categories with expected counts below about 5, where the approximation is poor.

## Why this matters
Chi-square tests check whether class frequencies drifted between training and production data,
whether a random-number generator is uniform, and whether a feature's categories relate to labels.
''',
"statement": r'''
Write `chi_square_test(observed, probs, alpha=0.05)` returning
`{"statistic": float, "p_value": float, "df": int, "reject": bool}` where `reject` is
`p_value < alpha`.

* Expected counts are the total of `observed` times each probability.
* Raise `ValueError` if lengths differ, there are fewer than 2 categories, any probability is
  ≤ 0, probabilities do not sum to 1 within 1e-9, any count is negative, the total is 0, or
  `alpha` is not strictly between 0 and 1.

Use `scipy.stats.chisquare`.

**Examples**
```python
chi_square_test([5, 8, 9, 8, 10, 20], [1/6] * 6)
# {'statistic': 13.4, 'p_value': 0.0199..., 'df': 5, 'reject': True}
chi_square_test([5, 8, 9, 8, 10, 20], [1/6] * 6, alpha=0.01)["reject"]   # False
```
''',
"starter": r'''
from scipy import stats


def chi_square_test(observed, probs, alpha=0.05):
    # TODO: validate, build expected counts, call stats.chisquare
    pass
''',
"hints": [
    "Validate the inputs as in the hand-written test, plus `0 < alpha < 1`.",
    "`expected = [total * p for p in probs]`; then `result = stats.chisquare(observed, f_exp=expected)`.",
    "Return `float(result.statistic)`, `float(result.pvalue)`, `len(observed) - 1` and the comparison with alpha.",
],
"solution": r'''
from scipy import stats


def chi_square_test(observed, probs, alpha=0.05):
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if len(observed) != len(probs) or len(observed) < 2:
        raise ValueError("need matching observed and probs with at least two categories")
    if any(p <= 0 for p in probs) or abs(sum(probs) - 1) > 1e-9:
        raise ValueError("probs must be positive and sum to 1")
    if any(o < 0 for o in observed):
        raise ValueError("counts must be non-negative")
    total = sum(observed)
    if total == 0:
        raise ValueError("total count is zero")
    expected = [total * p for p in probs]
    result = stats.chisquare(observed, f_exp=expected)
    p_value = float(result.pvalue)
    return {"statistic": float(result.statistic), "p_value": p_value,
            "df": len(observed) - 1, "reject": p_value < alpha}
''',
"explanation": r'''
SciPy needs expected counts, so the probabilities are scaled by the total. `chisquare` returns the
statistic and the upper-tail probability under the chi-square distribution with k − 1 degrees of
freedom; comparing that p-value with α replaces the table lookup of a critical value.
''',
"tests": r'''
class TestChiSquareSciPy(unittest.TestCase):
    def test_die(self):
        r = S.chi_square_test([5, 8, 9, 8, 10, 20], [1 / 6] * 6)
        self.assertAlmostEqual(r["statistic"], 13.4, places=9)
        self.assertEqual(r["df"], 5)
        self.assertAlmostEqual(r["p_value"], 0.019905220334774, places=9)
        self.assertTrue(r["reject"])

    def test_stricter_alpha(self):
        self.assertFalse(S.chi_square_test([5, 8, 9, 8, 10, 20], [1 / 6] * 6, alpha=0.01)["reject"])

    def test_perfect_fit(self):
        r = S.chi_square_test([50, 50], [0.5, 0.5])
        self.assertEqual(r["statistic"], 0.0)
        self.assertAlmostEqual(r["p_value"], 1.0)
        self.assertFalse(r["reject"])

    def test_p_value_is_upper_tail(self):
        from scipy import stats
        r = S.chi_square_test([30, 50, 20], [0.25, 0.5, 0.25])
        self.assertAlmostEqual(r["statistic"], 2.0)
        self.assertAlmostEqual(r["p_value"], stats.chi2(2).sf(2.0), places=12)

    def test_plain_types(self):
        r = S.chi_square_test([18, 22, 20], [1 / 3] * 3)
        self.assertIs(type(r["statistic"]), float)
        self.assertIs(type(r["p_value"]), float)
        self.assertIs(type(r["reject"]), bool)

    def test_invalid_inputs(self):
        for args in [([1, 2], [0.5, 0.6]), ([1, 2, 3], [0.5, 0.5]), ([0, 0], [0.5, 0.5]),
                     ([3, -1], [0.5, 0.5]), ([5], [1.0])]:
            with self.assertRaises(ValueError):
                S.chi_square_test(*args)
        with self.assertRaises(ValueError):
            S.chi_square_test([5, 5], [0.5, 0.5], alpha=1.5)
''',
"feedback": [
    ("test_die", "Pass expected counts (total × p), not probabilities, as f_exp."),
    ("test_stricter_alpha", "reject is p_value < alpha."),
    ("test_plain_types", "Convert NumPy results with float(...); the comparison gives a bool."),
    ("test_invalid_inputs", "Validate before calling SciPy, including alpha."),
],
},
# ---------------------------------------------------------------- welch-t-scipy
{
"slug": "welch-t-scipy", "title": "Welch's t-test with SciPy",
"difficulty": "advanced", "prereqs": ["chi-square-scipy", "sampling-distribution"], "packages": ["numpy", "scipy"],
"objectives": ["Compare two means with scipy.stats.ttest_ind(equal_var=False)",
               "Choose a two-sided or one-sided alternative",
               "Report the mean difference alongside the p-value"],
"tags": ["scipy", "hypothesis-testing", "t-test", "two-sample"],
"sources": ["S101", "S011"], "entry": "compare_means(x, y, alternative=\"two-sided\", alpha=0.05)",
"article": r'''
# Welch's t-test with SciPy

## Intuition
Two groups have different averages. Is the gap larger than the noise in each group would
produce? The t-statistic measures the gap in units of its standard error; the p-value asks how
often chance alone would give a t at least that extreme.

## Precise explanation
```python
from scipy import stats
result = stats.ttest_ind(x, y, equal_var=False)       # Welch's test
result.statistic, result.pvalue, result.df
```

`equal_var=False` selects **Welch's** test: each group keeps its own variance, and the degrees of
freedom come from the Welch–Satterthwaite formula (usually not an integer). The default,
`equal_var=True`, is Student's test, which pools the variances and can be badly wrong when the
spreads or sizes differ — so always ask for Welch unless you have a reason not to.

`alternative` states the question:

| `alternative` | Null hypothesis rejected when … |
|---|---|
| `"two-sided"` | the means differ in either direction |
| `"greater"` | mean(x) > mean(y) |
| `"less"` | mean(x) < mean(y) |

A one-sided p-value is half the two-sided one when the difference points the hypothesised way.

## Worked example
x = [1, 2, 3, 4, 5] and y = [3, 4, 5, 6, 7]: t = −2, df = 8, two-sided p ≈ 0.081. Not
significant at α = 0.05; with `alternative="less"`, p ≈ 0.040 and it is. Decide the alternative
**before** looking at the data — switching afterwards halves p dishonestly.

## What the library does inside
SciPy computes the same standard error, t and degrees of freedom as [[welch-t]] (the optional
deep dive after this step), then reads the p-value from the t distribution's tails with `stats.t`.

## Common mistakes
* Leaving `equal_var=True` (Student's test) when group variances differ.
* Reporting only "p < 0.05" without the size of the difference.
* Picking the one-sided alternative after seeing which mean is larger.
* Using it on paired measurements (before/after on the same people): that is `ttest_rel`.

## Why this matters
Comparing two model variants across random seeds, or an A/B test of two page designs, ends with
exactly this test — and the mean difference tells you whether the effect is worth acting on.
''',
"statement": r'''
Write `compare_means(x, y, alternative="two-sided", alpha=0.05)` returning
`{"mean_diff": float, "t": float, "df": float, "p_value": float, "reject": bool}` where
`mean_diff = mean(x) - mean(y)` and `reject` is `p_value < alpha`.

* Use `scipy.stats.ttest_ind` with `equal_var=False` and the given `alternative`.
* Raise `ValueError` if either sample has fewer than 2 values, both samples have zero variance,
  `alternative` is not one of `"two-sided"`, `"less"`, `"greater"`, or `alpha` is not in (0, 1).

**Examples**
```python
compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
# {'mean_diff': -2.0, 't': -2.0, 'df': 8.0, 'p_value': 0.0805..., 'reject': False}
compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="less")["reject"]   # True
```
''',
"starter": r'''
from scipy import stats


def compare_means(x, y, alternative="two-sided", alpha=0.05):
    # TODO
    pass
''',
"hints": [
    "Check the sizes, the alternative and alpha; compute each sample's variance to reject the all-constant case.",
    "`result = stats.ttest_ind(x, y, equal_var=False, alternative=alternative)`.",
    "`result.df` holds the Welch degrees of freedom; convert everything with float().",
],
"solution": r'''
from scipy import stats


def _variance(values):
    m = sum(values) / len(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - 1)


def compare_means(x, y, alternative="two-sided", alpha=0.05):
    if len(x) < 2 or len(y) < 2:
        raise ValueError("each sample needs at least two values")
    if alternative not in ("two-sided", "less", "greater"):
        raise ValueError("unknown alternative")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if _variance(x) == 0 and _variance(y) == 0:
        raise ValueError("both samples have zero variance")
    result = stats.ttest_ind(x, y, equal_var=False, alternative=alternative)
    p_value = float(result.pvalue)
    return {"mean_diff": sum(x) / len(x) - sum(y) / len(y), "t": float(result.statistic),
            "df": float(result.df), "p_value": p_value, "reject": p_value < alpha}
''',
"explanation": r'''
`ttest_ind(..., equal_var=False)` is Welch's test; the alternative is passed straight through.
SciPy would return `nan` when both samples are constant, so that case is rejected first. The mean
difference is reported because a p-value alone says nothing about how large the effect is.
''',
"tests": r'''
class TestCompareMeans(unittest.TestCase):
    def test_symmetric_example(self):
        from scipy import stats
        r = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
        self.assertAlmostEqual(r["t"], -2.0)
        self.assertAlmostEqual(r["df"], 8.0)
        self.assertAlmostEqual(r["p_value"], 2 * stats.t(8).sf(2.0), places=12)
        self.assertAlmostEqual(r["mean_diff"], -2.0)
        self.assertFalse(r["reject"])

    def test_one_sided_halves_p(self):
        two = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7])
        less = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="less")
        greater = S.compare_means([1, 2, 3, 4, 5], [3, 4, 5, 6, 7], alternative="greater")
        self.assertAlmostEqual(less["p_value"], two["p_value"] / 2)
        self.assertTrue(less["reject"])
        self.assertAlmostEqual(greater["p_value"], 1 - less["p_value"])

    def test_welch_not_student(self):
        x, y = [10, 12, 14], [1, 2, 3, 4, 5, 6]
        r = S.compare_means(x, y)
        vx, vy = 4 / 3, 3.5 / 6
        self.assertAlmostEqual(r["t"], 8.5 / math.sqrt(vx + vy), places=10)
        self.assertAlmostEqual(r["df"], (vx + vy) ** 2 / (vx ** 2 / 2 + vy ** 2 / 5), places=10)

    def test_clear_difference(self):
        r = S.compare_means([20.1, 19.8, 20.4, 20.0, 19.9], [10.2, 9.9, 10.1, 10.0, 9.8])
        self.assertTrue(r["reject"])
        self.assertLess(r["p_value"], 1e-6)

    def test_plain_types(self):
        r = S.compare_means([1.0, 2.0, 4.0], [2.0, 3.0, 3.5])
        self.assertTrue(all(type(r[k]) is float for k in ("mean_diff", "t", "df", "p_value")))
        self.assertIs(type(r["reject"]), bool)

    def test_invalid_inputs(self):
        for args, kwargs in [(([1], [1, 2]), {}), (([2, 2], [3, 3]), {}),
                             (([1, 2], [3, 4]), {"alternative": "bigger"}), (([1, 2], [3, 5]), {"alpha": 0})]:
            with self.assertRaises(ValueError):
                S.compare_means(*args, **kwargs)
''',
"feedback": [
    ("test_symmetric_example", "Call ttest_ind with equal_var=False; read t, df and p from the result."),
    ("test_one_sided_halves_p", "Pass alternative through to SciPy."),
    ("test_welch_not_student", "equal_var=False gives Welch's test; the default pools variances."),
    ("test_invalid_inputs", "Raise ValueError for tiny or constant samples, a bad alternative or alpha."),
],
},
# ---------------------------------------------------------------- permutation-test-scipy
{
"slug": "permutation-test-scipy", "title": "Permutation Test with SciPy",
"difficulty": "advanced", "prereqs": ["welch-t-scipy"], "packages": ["scipy"],
"objectives": ["Run scipy.stats.permutation_test with a custom statistic",
               "Write a vectorised statistic that accepts an axis argument",
               "Make resampling results reproducible with a seed"],
"tags": ["scipy", "hypothesis-testing", "permutation-test", "resampling"],
"sources": ["S101", "S010"], "entry": "permutation_mean_diff(x, y, alternative=\"two-sided\", n_resamples=9999, seed=0)",
"article": r'''
# Permutation Test with SciPy

## Intuition
If the group labels did not matter, shuffling them should not change the difference in means
much. A permutation test shuffles the labels many times and asks how often a shuffled difference
is at least as extreme as the real one. No normal distribution is assumed.

## Precise explanation
```python
from scipy import stats

def mean_diff(a, b, axis):
    return a.mean(axis=axis) - b.mean(axis=axis)

result = stats.permutation_test((x, y), mean_diff, permutation_type="independent",
                                n_resamples=9999, alternative="two-sided", random_state=0)
result.statistic, result.pvalue
```

* `data` is a tuple of samples; `permutation_type="independent"` reassigns values between groups.
* The statistic receives the samples as arrays (NumPy arrays, the subject of the next topic)
  and an `axis` keyword. `a.mean(axis=axis)` averages along that axis, which lets SciPy evaluate
  many shuffles in one call (`vectorized=True` is assumed when the function accepts `axis`).
* When `n_resamples` is at least the number of distinct relabellings, SciPy enumerates all of
  them and the p-value is **exact**; otherwise it samples randomly, so pass a seed as
  `random_state`.
* `alternative` works as in [[welch-t-scipy]].

## Worked example
x = [1, 2, 3, 4, 5], y = [3, 4, 5, 6, 7.5]: the observed difference is −2.1. There are only
C(10, 5) = 252 ways to split ten values into two groups of five, so with `n_resamples=9999` SciPy
checks all of them; 32 of 252 splits give a difference at least 2.1 in size, p = 0.127.

## What the library does inside
It is the loop from [[permutation-test]] (the optional deep dive after this step) — shuffle,
recompute, count — written with arrays so that thousands of shuffles are computed at once, plus
exact enumeration for small samples.

## Common mistakes
* Writing a statistic without the `axis` argument, so it silently averages over the wrong axis.
* Leaving out `random_state` and getting a different p-value every run.
* Using `permutation_type="samples"` (paired data) for two independent groups.

## Why this matters
Resampling tests let you compare model metrics, A/B groups or feature effects without assuming
normal errors — and SciPy's version is fast enough to run inside an evaluation pipeline.
''',
"statement": r'''
Write `permutation_mean_diff(x, y, alternative="two-sided", n_resamples=9999, seed=0)` returning
`{"statistic": float, "p_value": float}` for the difference in means `mean(x) - mean(y)`.

* Use `scipy.stats.permutation_test` with `permutation_type="independent"`, a statistic that
  accepts `axis`, and `random_state=seed`.
* Raise `ValueError` if either sample is empty or `alternative` is invalid.

**Examples**
```python
permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5])
# {'statistic': -2.1, 'p_value': 0.1269...}   (exact: all 252 splits are checked)
```
''',
"starter": r'''
from scipy import stats


def permutation_mean_diff(x, y, alternative="two-sided", n_resamples=9999, seed=0):
    # TODO
    pass
''',
"hints": [
    "Define `def mean_diff(a, b, axis): return a.mean(axis=axis) - b.mean(axis=axis)`.",
    "Call `stats.permutation_test((x, y), mean_diff, permutation_type=\"independent\", ...)`.",
    "Pass `n_resamples`, `alternative` and `random_state=seed`; return floats.",
],
"solution": r'''
from scipy import stats


def mean_diff(a, b, axis):
    return a.mean(axis=axis) - b.mean(axis=axis)


def permutation_mean_diff(x, y, alternative="two-sided", n_resamples=9999, seed=0):
    if len(x) == 0 or len(y) == 0:
        raise ValueError("samples must not be empty")
    if alternative not in ("two-sided", "less", "greater"):
        raise ValueError("unknown alternative")
    result = stats.permutation_test((x, y), mean_diff, permutation_type="independent",
                                    n_resamples=n_resamples, alternative=alternative,
                                    random_state=seed)
    return {"statistic": float(result.statistic), "p_value": float(result.pvalue)}
''',
"explanation": r'''
The statistic takes an `axis` so SciPy can evaluate many relabellings at once. For small samples
SciPy enumerates every split, giving an exact p-value; for larger ones the seed makes the random
resamples reproducible.
''',
"tests": r'''
import itertools


def brute_force_p(x, y):
    """Exact two-sided p-value: the share of all splits with |difference| at least the observed."""
    values, k = list(x) + list(y), len(x)
    observed = abs(sum(x) / len(x) - sum(y) / len(y))
    hits = total = 0
    for chosen in itertools.combinations(range(len(values)), k):
        a = [values[i] for i in chosen]
        b = [values[i] for i in range(len(values)) if i not in chosen]
        total += 1
        hits += abs(sum(a) / len(a) - sum(b) / len(b)) >= observed - 1e-12
    return hits / total


class TestPermutationSciPy(unittest.TestCase):
    def test_exact_small_sample(self):
        r = S.permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5])
        self.assertAlmostEqual(r["statistic"], -2.1)
        self.assertAlmostEqual(r["p_value"], brute_force_p([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5]), places=9)

    def test_identical_groups(self):
        r = S.permutation_mean_diff([1, 2, 3], [1, 2, 3])
        self.assertEqual(r["statistic"], 0.0)
        self.assertAlmostEqual(r["p_value"], 1.0)

    def test_one_sided(self):
        less = S.permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5], alternative="less")
        greater = S.permutation_mean_diff([1, 2, 3, 4, 5], [3, 4, 5, 6, 7.5], alternative="greater")
        self.assertLess(less["p_value"], greater["p_value"])
        self.assertAlmostEqual(less["p_value"], 16 / 252, places=9)

    def test_reproducible_with_seed(self):
        x = [0.1 * i for i in range(20)]
        y = [0.1 * i + 0.4 for i in range(20)]
        a = S.permutation_mean_diff(x, y, n_resamples=500, seed=3)
        b = S.permutation_mean_diff(x, y, n_resamples=500, seed=3)
        self.assertEqual(a, b)

    def test_large_shift_is_significant(self):
        x = [10 + 0.01 * i for i in range(12)]
        y = [0.01 * i for i in range(12)]
        r = S.permutation_mean_diff(x, y, n_resamples=999, seed=0)
        self.assertLess(r["p_value"], 0.01)
        self.assertAlmostEqual(r["statistic"], 10.0)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            S.permutation_mean_diff([], [1, 2])
        with self.assertRaises(ValueError):
            S.permutation_mean_diff([1, 2], [3, 4], alternative="sideways")
''',
"feedback": [
    ("test_exact_small_sample", "Use permutation_type='independent' and a statistic of mean(x) - mean(y)."),
    ("test_one_sided", "Pass the alternative through to permutation_test."),
    ("test_reproducible_with_seed", "Pass random_state=seed."),
    ("test_invalid_inputs", "Raise ValueError for empty samples and unknown alternatives."),
],
},
]

# ---------------------------------------------------------------- project ideas (ungraded)
PROBLEMS += [
{
"kind": "project", "slug": "ab-test-analyser", "title": "A/B Test Analyser",
"tags": ["a-b-testing", "hypothesis-testing", "confidence-intervals"],
"brief": r'''
Build a small tool that a product team could use after an experiment: give it the results for
version A and version B of a page (conversions or a numeric metric such as time on page) and it
reports the effect size, a confidence interval, and whether the difference is statistically
significant — in plain language a non-statistician can act on.
''',
"uses": ["bootstrap-ci", "scipy-stats-intro", "chi-square-scipy", "welch-t-scipy", "permutation-test-scipy"],
"milestones": [
    "Read two groups of numbers from a CSV file and print their sizes, means and standard deviations.",
    "Report the difference in means with a 95% bootstrap confidence interval.",
    "Add Welch's t-test and a permutation test and print both p-values side by side.",
    "Support conversion data (converted yes/no) with a chi-square test on the 2×2 table of counts.",
    "Write a one-paragraph summary: effect, interval, p-value and a recommendation with its caveats.",
],
"stretch": [
    "Estimate the sample size needed to detect a given effect (power analysis) by simulation.",
    "Show what goes wrong when you check the p-value every day and stop early ('peeking').",
    "Handle more than two variants and correct for multiple comparisons.",
],
"data": r'''
Generate data yourself with NumPy: for example 2,000 visitors per version with conversion rates
of 10% and 11% (`rng.random(2000) < 0.11`), or times drawn from `rng.lognormal`. Changing the true
effect and the sample size shows when a test can and cannot detect it.
''',
"setup": r'''
```bash
pip install numpy scipy pandas
python ab_test.py results.csv
```
Keep the analysis in functions so you can test each one with `unittest`, as in the course steps.
''',
},
{
"kind": "project", "slug": "dice-coin-simulator", "title": "Dice and Coin Simulator",
"tags": ["simulation", "law-of-large-numbers", "distributions"],
"brief": r'''
Build a simulator that rolls dice and flips coins thousands of times and shows, in numbers and
simple text charts, how averages settle down (the law of large numbers), how sums of dice become
bell-shaped (the central limit theorem), and how often "unlikely" streaks really happen.
''',
"uses": ["dice-lln", "histogram-bins", "binomial-pmf", "sampling-distribution", "scipy-stats-intro"],
"milestones": [
    "Simulate n fair coin flips with a seeded generator and print the running proportion of heads.",
    "Roll k dice many times and print a text histogram of the sums.",
    "Compare the simulated frequencies with the exact binomial probabilities from scipy.stats.",
    "Measure the longest run of heads in 100 flips across many trials and report how often it is 6 or more.",
],
"stretch": [
    "Add loaded dice and use a chi-square test to see how many rolls it takes to detect them.",
    "Plot the running mean with matplotlib and show the ±2 standard error band shrinking like 1/√n.",
    "Turn it into a small command-line game where players bet on outcomes.",
],
"data": r'''
No data is needed: everything is simulated with `numpy.random.default_rng(seed)`, so every run with
the same seed gives the same results.
''',
"setup": r'''
```bash
pip install numpy scipy
python simulator.py --dice 3 --rolls 10000 --seed 1
```
Optional: `pip install matplotlib` for charts.
''',
},
]
