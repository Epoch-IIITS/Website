"""Mathematics steps added in the 2026-10 revision: notation, exponentials and logarithms, the
sigmoid, and derivative rules with the chain rule."""

PROBLEMS = [
# ---------------------------------------------------------------- summation
{
"slug": "summation", "title": "Summation and Product Notation",
"difficulty": "beginner", "prereqs": ["functions-as-values"], "packages": [],
"objectives": ["Read Σ and Π notation and translate it into a loop",
               "Check a closed-form formula against a loop",
               "Explain why math.fsum is more accurate than repeated +"],
"tags": ["summation", "sigma-notation", "product-notation", "floating-point"],
"sources": ["S009", "S050"], "entry": "summation(f, start, stop); product(f, start, stop); mean(xs); sum_of_squares(n); accurate_sum(xs)",
"article": r'''
# Summation and Product Notation

## Intuition
Mathematics writes "add up these terms" with a big Greek S, **Σ** (sigma), and "multiply
them" with a big P, **Π** (pi). Almost every formula in ML — means, losses, dot products,
likelihoods — is a Σ or a Π, and each one is just a loop.

## Precise explanation
$$\sum_{i=a}^{b} f(i) = f(a) + f(a+1) + \dots + f(b), \qquad
  \prod_{i=a}^{b} f(i) = f(a)\,f(a+1)\cdots f(b).$$
* The index $i$ runs over every integer from $a$ to $b$ **inclusive**. If $b < a$ the sum is
  empty and equals 0; the empty product equals 1.
* In Python: `total = 0; for i in range(a, b + 1): total += f(i)`.
* The mean of $x_1, \dots, x_n$ is $\bar x = \frac{1}{n}\sum_{i=1}^{n} x_i$. Code indexes from 0,
  maths usually from 1: $x_1$ is `xs[0]`.
* Closed forms replace a loop with a formula, e.g. $\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$.
  Checking a formula against a loop is a reliable way to catch algebra mistakes.

**Floating-point sums.** Floats are stored in binary, so `0.1` is slightly off and errors add
up: `0.1 + 0.1 + ... (10 times)` is `0.9999999999999999`. `math.fsum` tracks the lost low-order
digits and returns the correctly rounded `1.0`.

## Worked example
$\sum_{i=1}^{4} (2i + 1) = 3 + 5 + 7 + 9 = 24$; $\prod_{i=1}^{4} i = 24 = 4!$.

## Common mistakes
* `range(a, b)` misses the last term $b$.
* Starting a product at 0 instead of 1.
* Using `//` in closed forms and losing the fraction before multiplying: compute
  `n * (n + 1) * (2 * n + 1) // 6`, not `n // 6 * ...`.

## Why this matters
Losses average a Σ over examples, likelihoods are a Π over observations ([[exp-log]] turns them
into sums), and [[dot-product]] is a Σ over coordinates.
''',
"statement": r'''
Implement:

1. `summation(f, start, stop)` — $\sum_{i=start}^{stop} f(i)$ with a loop (0 if `stop < start`).
2. `product(f, start, stop)` — $\prod_{i=start}^{stop} f(i)$ with a loop (1 if `stop < start`).
3. `mean(xs)` — $\frac1n\sum x_i$ using your `summation` over indices; raise `ValueError` for an
   empty list.
4. `sum_of_squares(n)` — the closed form $n(n+1)(2n+1)/6$ as an `int`.
5. `accurate_sum(xs)` — the sum computed with `math.fsum`.

**Examples**
```python
summation(lambda i: 2 * i + 1, 1, 4)   # 24
product(lambda i: i, 1, 5)             # 120
mean([2, 4, 9])                        # 5.0
sum_of_squares(3)                      # 14
accurate_sum([0.1] * 10)               # 1.0
```
''',
"starter": r'''
import math


def summation(f, start, stop):
    total = 0
    # TODO
    return total


def product(f, start, stop):
    # TODO
    return 0


def mean(xs):
    # TODO
    return 0.0


def sum_of_squares(n):
    # TODO: closed form
    return 0


def accurate_sum(xs):
    # TODO: math.fsum
    return sum(xs)
''',
"hints": [
    "`for i in range(start, stop + 1): total += f(i)` — note the `+ 1`.",
    "A product starts from 1. For the mean, `summation(lambda i: xs[i], 0, len(xs) - 1) / len(xs)`.",
    "`n * (n + 1) * (2 * n + 1) // 6` is exact because the product is always divisible by 6.",
],
"solution": r'''
import math


def summation(f, start, stop):
    total = 0
    for i in range(start, stop + 1):
        total += f(i)
    return total


def product(f, start, stop):
    result = 1
    for i in range(start, stop + 1):
        result *= f(i)
    return result


def mean(xs):
    if not xs:
        raise ValueError("mean of empty data")
    return summation(lambda i: xs[i], 0, len(xs) - 1) / len(xs)


def sum_of_squares(n):
    return n * (n + 1) * (2 * n + 1) // 6


def accurate_sum(xs):
    return math.fsum(xs)
''',
"explanation": r'''
Σ and Π become loops over `range(start, stop + 1)` starting from their identity elements 0 and
1, which also gives the correct empty results. The mean reuses `summation` over list indices.
The closed form uses integer arithmetic on the full product before dividing, and `math.fsum`
compensates for rounding errors that a plain loop accumulates.
''',
"tests": r'''
class TestSummation(unittest.TestCase):
    def test_sum_odd_numbers(self):
        self.assertEqual(S.summation(lambda i: 2 * i + 1, 1, 4), 24)

    def test_empty_ranges(self):
        self.assertEqual(S.summation(lambda i: i, 5, 4), 0)
        self.assertEqual(S.product(lambda i: i, 5, 4), 1)

    def test_product_factorial(self):
        self.assertEqual(S.product(lambda i: i, 1, 5), 120)
        self.assertAlmostEqual(S.product(lambda i: 0.5, 1, 3), 0.125)

    def test_mean(self):
        self.assertEqual(S.mean([2, 4, 9]), 5.0)
        with self.assertRaises(ValueError):
            S.mean([])

    def test_closed_form_matches_loop(self):
        for n in range(0, 60):
            self.assertEqual(S.sum_of_squares(n), S.summation(lambda i: i * i, 1, n))
        self.assertIsInstance(S.sum_of_squares(10), int)

    def test_accurate_sum(self):
        self.assertEqual(S.accurate_sum([0.1] * 10), 1.0)
        self.assertNotEqual(S.summation(lambda i: 0.1, 1, 10), 1.0)

    def test_matches_builtins(self):
        f = lambda i: i ** 3 - 2 * i
        self.assertEqual(S.summation(f, -3, 7), sum(f(i) for i in range(-3, 8)))
        self.assertEqual(S.product(lambda i: i, 1, 10), math.prod(range(1, 11)))
''',
"feedback": [
    ("test_sum_odd_numbers", "Include the last index: loop over `range(start, stop + 1)`."),
    ("test_empty_ranges", "Start the sum at 0 and the product at 1; an empty range leaves them unchanged."),
    ("test_mean", "Divide the sum by the number of items and raise ValueError for an empty list."),
    ("test_closed_form_matches_loop", "Use `n * (n + 1) * (2 * n + 1) // 6`."),
    ("test_accurate_sum", "Return `math.fsum(xs)`."),
],
"library": {
"text": r'''
Python's built-ins already implement these loops:

```python
sum(f(i) for i in range(a, b + 1))   # Σ — the built-in sum
math.prod(f(i) for i in range(a, b + 1))  # Π
math.fsum(xs)                        # Σ with correctly rounded floating-point result
statistics.fmean(xs)                 # mean, using an accurate float sum
```
`sum` and `math.prod` behave exactly like your loops (same rounding); `math.fsum` and
`statistics.fmean` are more accurate for floats. The test below checks your `mean` against
`statistics.fmean`.
''',
"tests": r'''
import statistics


class TestAgainstLibrary(unittest.TestCase):
    def test_mean_matches_statistics(self):
        data = [1.5, 2.25, -4.0, 10.125, 3.0]
        self.assertAlmostEqual(S.mean(data), statistics.fmean(data), places=12)
''',
},
},
# ---------------------------------------------------------------- exp-log
{
"slug": "exp-log", "title": "Exponentials and Logarithms",
"difficulty": "beginner", "prereqs": ["summation"], "packages": [],
"objectives": ["Use the rules log(ab) = log a + log b and log_b x = ln x / ln b",
               "Avoid underflow by adding log-probabilities instead of multiplying probabilities",
               "Compute log-sum-exp stably by subtracting the maximum"],
"tags": ["exponential", "logarithm", "log-likelihood", "underflow", "log-sum-exp"],
"sources": ["S009", "S050"], "entry": "log_base(x, base); doubling_time(rate); log_likelihood(probs); logsumexp(values)",
"article": r'''
# Exponentials and Logarithms

## Intuition
The exponential $e^x$ grows by the same *factor* for each step in $x$; the natural logarithm
$\ln x$ undoes it, answering "what power of $e$ gives $x$?". Logs turn multiplication into
addition, which is why ML works with **log-probabilities**: multiplying hundreds of small
probabilities underflows to 0, but adding their logs is perfectly stable.

## Precise explanation
* $e \approx 2.71828$; `math.exp(x)` is $e^x$ and `math.log(x)` is $\ln x$ (only for $x > 0$).
* Rules: $\ln(ab) = \ln a + \ln b$, $\ln(a^k) = k\ln a$, $\ln 1 = 0$, $e^{\ln x} = x$.
* Change of base: $\log_b x = \dfrac{\ln x}{\ln b}$, e.g. $\log_2 8 = 3$.
* Compound growth: an amount growing by rate $r$ per step doubles after
  $t = \dfrac{\ln 2}{\ln(1+r)}$ steps.
* **Log-likelihood**: $\ln \prod_i p_i = \sum_i \ln p_i$.
* **Log-sum-exp**: $\mathrm{LSE}(v) = \ln \sum_i e^{v_i}$. Computing $e^{1000}$ overflows, so
  use $\mathrm{LSE}(v) = m + \ln\sum_i e^{v_i - m}$ with $m = \max_i v_i$; every exponent is then
  at most $e^0 = 1$.

## Worked example
Probabilities `[1e-5] * 1000`: the product is $10^{-5000}$, which a float stores as `0.0`, and
`math.log(0.0)` raises `ValueError`. The sum of logs is $1000 \ln 10^{-5} \approx -11512.9$.
`logsumexp([1000, 1000])` $= 1000 + \ln 2 \approx 1000.693$.

## Common mistakes
* `math.log(x, 10)` vs `math.log10(x)` — both work; `math.log(x)` alone is base $e$, not 10.
* Taking the log of 0 or a negative number.
* Implementing log-sum-exp directly, which overflows for large inputs or underflows to
  `log(0)` for very negative ones.

## Why this matters
Cross-entropy loss, perplexity, Naive Bayes and softmax ([[stable-softmax]]) all rely on these
identities, and [[sigmoid-function]] is built from $e^{-x}$.
''',
"statement": r'''
Implement with the `math` module:

1. `log_base(x, base)` — $\log_{base} x$ via the change-of-base rule (use `math.log(x)` only).
2. `doubling_time(rate)` — $\ln 2 / \ln(1 + rate)$.
3. `log_likelihood(probs)` — $\sum \ln p_i$; raise `ValueError` if any $p \le 0$ or $p > 1$.
   It must work for 1000 probabilities of `1e-5` (where the plain product underflows).
4. `logsumexp(values)` — the stable form $m + \ln\sum e^{v_i - m}$; raise `ValueError` for an
   empty list.

**Examples**
```python
log_base(8, 2)                 # 3.0 (within rounding)
doubling_time(0.07)            # ≈ 10.24
log_likelihood([0.5, 0.25])    # ln(0.125) ≈ -2.0794
logsumexp([1000, 1000])        # ≈ 1000.6931
```
''',
"starter": r'''
import math


def log_base(x, base):
    # TODO
    return 0.0


def doubling_time(rate):
    # TODO
    return 0.0


def log_likelihood(probs):
    # TODO: sum of logs, with validation
    return math.log(math.prod(probs))


def logsumexp(values):
    # TODO: subtract the maximum first
    return math.log(sum(math.exp(v) for v in values))
''',
"hints": [
    "`math.log(x) / math.log(base)`; `math.log(2) / math.log(1 + rate)`.",
    "Loop over the probabilities, check `0 < p <= 1`, and add `math.log(p)`.",
    "`m = max(values)`, then `m + math.log(sum(math.exp(v - m) for v in values))`.",
],
"solution": r'''
import math


def log_base(x, base):
    return math.log(x) / math.log(base)


def doubling_time(rate):
    return math.log(2) / math.log(1 + rate)


def log_likelihood(probs):
    total = 0.0
    for p in probs:
        if not 0 < p <= 1:
            raise ValueError("probabilities must be in (0, 1]")
        total += math.log(p)
    return total


def logsumexp(values):
    if not values:
        raise ValueError("logsumexp of empty sequence")
    m = max(values)
    return m + math.log(sum(math.exp(v - m) for v in values))
''',
"explanation": r'''
The change-of-base and doubling formulas are direct translations. The log-likelihood never forms
the tiny product, so it cannot underflow, and invalid probabilities are rejected before taking
logs. Subtracting the maximum in log-sum-exp makes the largest exponent exactly 1, so the sum is
between 1 and n and its logarithm is always finite.
''',
"tests": r'''
class TestExpLog(unittest.TestCase):
    def test_log_base(self):
        self.assertAlmostEqual(S.log_base(8, 2), 3.0)
        self.assertAlmostEqual(S.log_base(1000, 10), 3.0)
        self.assertAlmostEqual(S.log_base(1, 7), 0.0)

    def test_doubling_time(self):
        self.assertAlmostEqual(S.doubling_time(1.0), 1.0)
        self.assertAlmostEqual(S.doubling_time(0.07), 10.244768351058712, places=9)

    def test_log_likelihood_small(self):
        self.assertAlmostEqual(S.log_likelihood([0.5, 0.25]), math.log(0.125))
        self.assertEqual(S.log_likelihood([]), 0.0)

    def test_log_likelihood_no_underflow(self):
        probs = [1e-5] * 1000
        self.assertEqual(math.prod(probs), 0.0)
        self.assertAlmostEqual(S.log_likelihood(probs), 1000 * math.log(1e-5), places=6)

    def test_log_likelihood_validates(self):
        for bad in ([0.5, 0.0], [1.5], [-0.1]):
            with self.assertRaises(ValueError):
                S.log_likelihood(bad)

    def test_logsumexp_small(self):
        v = [0.1, -2.0, 1.5]
        self.assertAlmostEqual(S.logsumexp(v), math.log(sum(math.exp(x) for x in v)))

    def test_logsumexp_large_and_negative(self):
        self.assertAlmostEqual(S.logsumexp([1000, 1000]), 1000 + math.log(2))
        self.assertAlmostEqual(S.logsumexp([-1000, -1000]), -1000 + math.log(2))
        with self.assertRaises(ValueError):
            S.logsumexp([])
''',
"feedback": [
    ("test_log_base", "Divide `math.log(x)` by `math.log(base)`."),
    ("test_log_likelihood_no_underflow", "Add logs one by one instead of taking the log of the product."),
    ("test_log_likelihood_validates", "Raise ValueError for any p that is not in (0, 1]."),
    ("test_logsumexp_large_and_negative", "Subtract the maximum before exponentiating and add it back after the log."),
],
"library": {
"text": r'''
The `math` module already provides `math.log(x, base)`, `math.log2`, `math.log10` and
`math.log1p(r)` (an accurate $\ln(1 + r)$ for small $r$). For log-sum-exp, SciPy offers
`scipy.special.logsumexp`, which uses the same max-subtraction trick (it also handles arrays and
weights). The tests below compare your functions with these when they are available; the SciPy
comparison is skipped if SciPy is not installed.
''',
"optional": ["scipy"],
"tests": r'''
try:
    import scipy.special as _special
except ImportError:
    _special = None


class TestAgainstLibrary(unittest.TestCase):
    def test_log_base_matches_math(self):
        for x, b in [(8, 2), (81, 3), (0.5, 10)]:
            self.assertAlmostEqual(S.log_base(x, b), math.log(x, b), places=12)

    def test_doubling_uses_same_value_as_log1p(self):
        self.assertAlmostEqual(S.doubling_time(1e-6), math.log(2) / math.log1p(1e-6), delta=1e-3)

    @unittest.skipIf(_special is None, "SciPy not installed")
    def test_logsumexp_matches_scipy(self):
        v = [3.0, -1.0, 700.0, 699.5]
        self.assertAlmostEqual(S.logsumexp(v), float(_special.logsumexp(v)), places=9)
''',
},
},
# ---------------------------------------------------------------- sigmoid-function
{
"slug": "sigmoid-function", "title": "The Sigmoid Function",
"difficulty": "beginner", "prereqs": ["exp-log"], "packages": [],
"objectives": ["Compute σ(x) = 1 / (1 + e^(−x)) without overflow",
               "Use the derivative σ'(x) = σ(x)(1 − σ(x))",
               "Invert the sigmoid with the logit function"],
"tags": ["sigmoid", "logistic-function", "logit", "numerical-stability"],
"sources": ["S009", "S013", "S050"], "entry": "sigmoid(x); sigmoid_derivative(x); logit(p)",
"article": r'''
# The Sigmoid Function

## Intuition
The sigmoid squashes any real number into the interval (0, 1): very negative inputs give values
near 0, very positive inputs give values near 1, and 0 gives exactly 0.5. That makes it a
natural way to turn a score into a probability.

## Precise explanation
$$\sigma(x) = \frac{1}{1 + e^{-x}}, \qquad \sigma(-x) = 1 - \sigma(x), \qquad
  \sigma'(x) = \sigma(x)\,(1 - \sigma(x)).$$
* The derivative is largest at $x = 0$ ($0.25$) and nearly 0 for large $|x|$ — the reason deep
  sigmoid networks learn slowly ("vanishing gradients").
* **Inverse (logit)**: $\operatorname{logit}(p) = \ln\dfrac{p}{1-p}$ for $0 < p < 1$, and
  $\sigma(\operatorname{logit}(p)) = p$.
* **Overflow**: Python's `math.exp(1000)` raises `OverflowError`. For $x < 0$ compute
  $\sigma(x) = \dfrac{e^{x}}{1 + e^{x}}$ instead (multiply top and bottom by $e^x$); then the
  exponent is always $\le 0$ and nothing overflows.

## Worked example
$\sigma(0) = 1/2$; $\sigma(2) = 1/(1 + e^{-2}) \approx 0.8808$; $\sigma(-2) \approx 0.1192 = 1 - 0.8808$;
$\sigma'(0) = 0.5 \cdot 0.5 = 0.25$; $\operatorname{logit}(0.8808) \approx 2$.

## Common mistakes
* Writing `1 / 1 + math.exp(-x)` — precedence makes it $1 + e^{-x}$.
* Using the one-line formula for $x = -1000$ and crashing with `OverflowError`.
* Calling `logit(0)` or `logit(1)`, which are infinite.

## Why this matters
Logistic regression ([[logistic-regression]]) predicts $\sigma(w\cdot x + b)$, the derivative
formula gives its gradient, and neural-network activations ([[activations]]) start here.
''',
"statement": r'''
Implement with the `math` module:

1. `sigmoid(x)` — numerically stable for any float, including `±1000`: use
   $1/(1+e^{-x})$ for $x \ge 0$ and $e^{x}/(1+e^{x})$ for $x < 0$.
2. `sigmoid_derivative(x)` — $\sigma(x)(1-\sigma(x))$.
3. `logit(p)` — $\ln(p/(1-p))$; raise `ValueError` unless `0 < p < 1`.

**Examples**
```python
sigmoid(0)              # 0.5
sigmoid(-1000)          # 0.0 (no OverflowError)
sigmoid_derivative(0)   # 0.25
logit(0.5)              # 0.0
```
''',
"starter": r'''
import math


def sigmoid(x):
    # TODO: make this stable for very negative x
    return 1 / (1 + math.exp(-x))


def sigmoid_derivative(x):
    # TODO
    return 0.0


def logit(p):
    # TODO
    return 0.0
''',
"hints": [
    "Branch on the sign: `if x >= 0:` use the usual formula, else compute `z = math.exp(x)` and return `z / (1 + z)`.",
    "`s = sigmoid(x); return s * (1 - s)`.",
    "Validate with `if not 0 < p < 1: raise ValueError(...)`, then `math.log(p / (1 - p))`.",
],
"solution": r'''
import math


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    z = math.exp(x)
    return z / (1 + z)


def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)


def logit(p):
    if not 0 < p < 1:
        raise ValueError("p must be strictly between 0 and 1")
    return math.log(p / (1 - p))
''',
"explanation": r'''
Each branch of `sigmoid` only exponentiates a non-positive number, so `math.exp` never
overflows; the two formulas are algebraically equal. The derivative reuses the forward value,
which is how backpropagation computes it cheaply. `logit` validates its domain before the log.
''',
"tests": r'''
class TestSigmoid(unittest.TestCase):
    def test_known_values(self):
        self.assertEqual(S.sigmoid(0), 0.5)
        self.assertAlmostEqual(S.sigmoid(2), 1 / (1 + math.exp(-2)))

    def test_symmetry(self):
        for x in (-5.0, -0.3, 0.7, 4.0):
            self.assertAlmostEqual(S.sigmoid(-x), 1 - S.sigmoid(x))

    def test_extremes_no_overflow(self):
        self.assertEqual(S.sigmoid(1000), 1.0)
        self.assertEqual(S.sigmoid(-1000), 0.0)
        self.assertGreater(S.sigmoid(-30), 0.0)

    def test_derivative(self):
        self.assertAlmostEqual(S.sigmoid_derivative(0), 0.25)
        h = 1e-6
        for x in (-3.0, 0.5, 2.0):
            numeric = (S.sigmoid(x + h) - S.sigmoid(x - h)) / (2 * h)
            self.assertAlmostEqual(S.sigmoid_derivative(x), numeric, places=8)

    def test_logit_inverse(self):
        self.assertAlmostEqual(S.logit(0.5), 0.0)
        for p in (0.01, 0.3, 0.9):
            self.assertAlmostEqual(S.sigmoid(S.logit(p)), p)

    def test_logit_domain(self):
        for bad in (0, 1, -0.2, 1.5):
            with self.assertRaises(ValueError):
                S.logit(bad)
''',
"feedback": [
    ("test_extremes_no_overflow", "For negative x use `math.exp(x) / (1 + math.exp(x))` so the exponent never becomes huge."),
    ("test_derivative", "Return `s * (1 - s)` where `s = sigmoid(x)`."),
    ("test_logit_inverse", "logit(p) is `math.log(p / (1 - p))`."),
    ("test_logit_domain", "Raise ValueError unless 0 < p < 1."),
],
"library": {
"text": r'''
SciPy implements both functions as `scipy.special.expit` (the sigmoid) and
`scipy.special.logit`, vectorised over NumPy arrays and stable for large inputs. In NumPy code
later on ([[activations]]) you will write the same branch with `np.where`. The comparison
below runs only when SciPy is installed.
''',
"optional": ["scipy"],
"tests": r'''
try:
    import scipy.special as _special
except ImportError:
    _special = None


class TestAgainstLibrary(unittest.TestCase):
    @unittest.skipIf(_special is None, "SciPy not installed")
    def test_matches_scipy(self):
        for x in (-50.0, -1.0, 0.0, 3.5, 40.0):
            self.assertAlmostEqual(S.sigmoid(x), float(_special.expit(x)), places=12)
        for p in (0.1, 0.5, 0.75):
            self.assertAlmostEqual(S.logit(p), float(_special.logit(p)), places=12)
''',
},
},
# ---------------------------------------------------------------- derivative-rules
{
"slug": "derivative-rules", "title": "Derivative Rules and the Chain Rule",
"difficulty": "intermediate", "prereqs": ["central-difference", "sigmoid-function"], "packages": [],
"objectives": ["Apply the power, sum, product and chain rules",
               "Represent a function together with its derivative as a pair",
               "Verify an analytic derivative against a central-difference estimate"],
"tags": ["derivatives", "chain-rule", "product-rule", "calculus", "backpropagation"],
"sources": ["S009", "S016"], "entry": "power_rule(n); sum_rule(f, df, g, dg); product_rule(f, df, g, dg); chain_rule(f, df, g, dg); sigmoid_of_linear(a, b)",
"article": r'''
# Derivative Rules and the Chain Rule

## Intuition
[[central-difference]] *estimates* a derivative by nudging the input. Rules give the *exact*
derivative of a formula built from simpler pieces. The most important is the **chain rule**:
when one function feeds another, their rates of change multiply — the idea behind
backpropagation.

## Precise explanation
| Rule | Function | Derivative |
|---|---|---|
| power | $x^n$ | $n x^{n-1}$ |
| sum | $f + g$ | $f' + g'$ |
| product | $f g$ | $f' g + f g'$ |
| chain | $f(g(x))$ | $f'(g(x))\, g'(x)$ |
| exp, log | $e^x$, $\ln x$ | $e^x$, $1/x$ |
| sigmoid | $\sigma(x)$ | $\sigma(x)(1-\sigma(x))$ |

In code, represent a differentiable function as a **pair** `(f, df)` of Python functions. Each
rule takes pairs and returns a new pair, so you can build derivatives of complicated formulas
from small, tested pieces.

```python
def chain_rule(f, df, g, dg):
    h = lambda x: f(g(x))
    dh = lambda x: df(g(x)) * dg(x)
    return h, dh
```

## Worked example
$h(x) = \sigma(3x + 1)$: outer $f = \sigma$, inner $g(x) = 3x + 1$ with $g' = 3$, so
$h'(x) = \sigma(3x+1)(1-\sigma(3x+1)) \cdot 3$. At $x = 0$: $\sigma(1) \approx 0.7311$ and
$h'(0) \approx 0.7311 \cdot 0.2689 \cdot 3 \approx 0.5898$.

## Common mistakes
* Forgetting the inner derivative: $\frac{d}{dx}\sigma(3x) \ne \sigma'(3x)$; multiply by 3.
* Evaluating the outer derivative at $x$ instead of at $g(x)$.
* Product rule as $f' g'$.

## Why this matters
Backpropagation ([[neuron-backprop]], [[scalar-autograd]]) is the chain rule applied repeatedly,
and gradient descent ([[gradient-descent-1d]]) needs these derivatives.
''',
"statement": r'''
Each function below returns a pair `(h, dh)` of one-argument functions.

1. `power_rule(n)` → $(x^n,\; n x^{n-1})$.
2. `sum_rule(f, df, g, dg)` → $(f+g,\; f'+g')$.
3. `product_rule(f, df, g, dg)` → $(fg,\; f'g + fg')$.
4. `chain_rule(f, df, g, dg)` → $(f\circ g,\; (f'\circ g)\cdot g')$.
5. `sigmoid_of_linear(a, b)` → the pair for $\sigma(ax + b)$, built with `chain_rule` from the
   sigmoid pair and the linear pair $(ax+b,\; a)$. Use a stable sigmoid as in [[sigmoid-function]].

**Example**
```python
h, dh = sigmoid_of_linear(3, 1)
h(0)     # ≈ 0.7311
dh(0)    # ≈ 0.5898
```
''',
"starter": r'''
import math


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    z = math.exp(x)
    return z / (1 + z)


def power_rule(n):
    return (lambda x: x ** n), (lambda x: n * x ** (n - 1))


def sum_rule(f, df, g, dg):
    # TODO
    return f, df


def product_rule(f, df, g, dg):
    # TODO
    return f, df


def chain_rule(f, df, g, dg):
    # TODO
    return f, df


def sigmoid_of_linear(a, b):
    # TODO: use chain_rule
    return sigmoid, sigmoid
''',
"hints": [
    "Each rule returns two lambdas, e.g. `(lambda x: f(x) + g(x)), (lambda x: df(x) + dg(x))`.",
    "Chain rule: `dh = lambda x: df(g(x)) * dg(x)` — the outer derivative is evaluated at g(x).",
    "The sigmoid's derivative is `lambda u: sigmoid(u) * (1 - sigmoid(u))`; the linear pair is `(lambda x: a * x + b, lambda x: a)`.",
],
"solution": r'''
import math


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    z = math.exp(x)
    return z / (1 + z)


def power_rule(n):
    return (lambda x: x ** n), (lambda x: n * x ** (n - 1))


def sum_rule(f, df, g, dg):
    return (lambda x: f(x) + g(x)), (lambda x: df(x) + dg(x))


def product_rule(f, df, g, dg):
    return (lambda x: f(x) * g(x)), (lambda x: df(x) * g(x) + f(x) * dg(x))


def chain_rule(f, df, g, dg):
    return (lambda x: f(g(x))), (lambda x: df(g(x)) * dg(x))


def sigmoid_of_linear(a, b):
    dsigmoid = lambda u: sigmoid(u) * (1 - sigmoid(u))
    return chain_rule(sigmoid, dsigmoid, lambda x: a * x + b, lambda x: a)
''',
"explanation": r'''
Every rule is a direct translation of its formula into a pair of closures. Because rules accept
and return pairs, they compose: `sigmoid_of_linear` is one call to `chain_rule`, and the tests
build larger expressions (products of chains) the same way and confirm them numerically.
''',
"tests": r'''
def numeric(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)


class TestDerivativeRules(unittest.TestCase):
    def test_power(self):
        f, df = S.power_rule(3)
        self.assertEqual(f(2), 8)
        self.assertEqual(df(2), 12)

    def test_sum(self):
        f, df = S.sum_rule(math.sin, math.cos, *S.power_rule(2))
        for x in (-1.0, 0.3, 2.0):
            self.assertAlmostEqual(f(x), math.sin(x) + x * x)
            self.assertAlmostEqual(df(x), numeric(f, x), places=6)

    def test_product(self):
        f, df = S.product_rule(math.exp, math.exp, *S.power_rule(2))
        self.assertAlmostEqual(df(1.0), 3 * math.e)
        self.assertAlmostEqual(df(-0.5), numeric(f, -0.5), places=6)

    def test_chain(self):
        f, df = S.chain_rule(math.sin, math.cos, *S.power_rule(2))
        for x in (0.0, 0.7, -1.3):
            self.assertAlmostEqual(f(x), math.sin(x * x))
            self.assertAlmostEqual(df(x), math.cos(x * x) * 2 * x)

    def test_sigmoid_of_linear(self):
        h, dh = S.sigmoid_of_linear(3, 1)
        self.assertAlmostEqual(h(0), 1 / (1 + math.exp(-1)))
        s = 1 / (1 + math.exp(-1))
        self.assertAlmostEqual(dh(0), 3 * s * (1 - s))
        self.assertAlmostEqual(dh(-0.4), numeric(h, -0.4), places=6)

    def test_sigmoid_of_linear_stable(self):
        h, dh = S.sigmoid_of_linear(10, 0)
        self.assertEqual(h(-500), 0.0)
        self.assertEqual(dh(-500), 0.0)

    def test_rules_compose(self):
        inner = S.sigmoid_of_linear(2, -1)
        f, df = S.product_rule(*inner, *S.power_rule(3))
        for x in (-1.0, 0.25, 1.5):
            self.assertAlmostEqual(df(x), numeric(f, x), places=5)
''',
"feedback": [
    ("test_sum", "Return the sum of the functions and the sum of their derivatives."),
    ("test_product", "Product rule: `df(x) * g(x) + f(x) * dg(x)`."),
    ("test_chain", "Evaluate the outer derivative at `g(x)` and multiply by `dg(x)`."),
    ("test_sigmoid_of_linear", "Build the pair with `chain_rule(sigmoid, dsigmoid, linear, dlinear)`."),
    ("test_sigmoid_of_linear_stable", "Use the stable sigmoid from the starter for both the value and the derivative."),
],
},
]
