"""Statistics steps added in the 2026-10 revision: probability, conditional probability and
Bayes' rule, the normal distribution, and sampling distributions."""

PROBLEMS = [
# ---------------------------------------------------------------- probability-basics
{
"slug": "probability-basics", "title": "Probability by Counting Outcomes",
"difficulty": "intermediate", "prereqs": ["histogram-bins"], "packages": [],
"objectives": ["Describe a sample space and events as Python data and predicates",
               "Compute exact probabilities with fractions.Fraction",
               "Apply the complement and inclusion–exclusion rules",
               "Test two events for independence"],
"tags": ["probability", "sample-space", "events", "independence", "fractions"],
"sources": ["S011", "S010", "S058"], "entry": "two_dice(); probability(space, event); complement(space, event); union(space, a, b); independent(space, a, b)",
"article": r'''
# Probability by Counting Outcomes

## Intuition
Roll two fair dice. There are 36 equally likely outcomes. The probability of an event such as
"the total is 7" is simply the fraction of outcomes in which it happens: 6 of 36, so 1/6.
When outcomes are equally likely, probability is counting.

## Precise explanation
* **Sample space** $\Omega$: the list of all outcomes, e.g. pairs `(d1, d2)`.
* **Event**: a set of outcomes — in code, a predicate function `lambda o: o[0] + o[1] == 7`.
* With equally likely outcomes, $P(A) = \dfrac{|A|}{|\Omega|}$.
* **Complement**: $P(\text{not } A) = 1 - P(A)$.
* **Union** (inclusion–exclusion): $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ — outcomes in both
  would otherwise be counted twice.
* **Independence**: $A$ and $B$ are independent when $P(A \cap B) = P(A)\,P(B)$.

`fractions.Fraction(6, 36)` stores the exact value `Fraction(1, 6)`, so equality tests like
independence are exact; with floats, `0.1 * 3 == 0.3` is False.

## Worked example
$A$ = "first die is even" (18 outcomes), $B$ = "total is 7" (6 outcomes),
$A \cap B$ = {(2,5), (4,3), (6,1)} (3 outcomes). $P(A)P(B) = \frac12 \cdot \frac16 = \frac1{12}
= \frac{3}{36} = P(A \cap B)$, so they are independent. $P(A \cup B) = \frac{18 + 6 - 3}{36} = \frac{21}{36}$.

## Common mistakes
* Assuming outcomes are equally likely when they are not (the *totals* 2..12 are not).
* Adding $P(A) + P(B)$ for overlapping events.
* Confusing independent with mutually exclusive: exclusive events with non-zero probability are
  never independent.

## Why this matters
Probability is the language of classification ("70% spam"), of [[conditional-bayes]] and Naive
Bayes, and of every simulation in this topic.
''',
"statement": r'''
Implement:

1. `two_dice()` → list of all 36 outcomes `(d1, d2)` with `d1, d2` in 1..6, ordered by `d1`
   then `d2`.
2. `probability(space, event)` → `Fraction` of outcomes where `event(outcome)` is true. Raise
   `ValueError` for an empty space.
3. `complement(space, event)` → probability that the event does **not** happen.
4. `union(space, a, b)` → $P(A \cup B)$ computed by inclusion–exclusion (call `probability`
   three times).
5. `independent(space, a, b)` → `True` if $P(A \cap B) = P(A)P(B)$ exactly.

**Examples**
```python
space = two_dice()
probability(space, lambda o: sum(o) == 7)          # Fraction(1, 6)
union(space, lambda o: o[0] == 6, lambda o: o[1] == 6)   # Fraction(11, 36)
independent(space, lambda o: o[0] % 2 == 0, lambda o: sum(o) == 7)   # True
```
''',
"starter": r'''
from fractions import Fraction


def two_dice():
    # TODO
    return []


def probability(space, event):
    # TODO
    return Fraction(0)


def complement(space, event):
    # TODO
    return Fraction(0)


def union(space, a, b):
    # TODO: inclusion-exclusion
    return Fraction(0)


def independent(space, a, b):
    # TODO
    return False
''',
"hints": [
    "`[(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7)]` builds the space in the right order.",
    "`Fraction(sum(1 for o in space if event(o)), len(space))` is the probability.",
    "The intersection event is `lambda o: a(o) and b(o)`.",
],
"solution": r'''
from fractions import Fraction


def two_dice():
    return [(d1, d2) for d1 in range(1, 7) for d2 in range(1, 7)]


def probability(space, event):
    if not space:
        raise ValueError("empty sample space")
    return Fraction(sum(1 for o in space if event(o)), len(space))


def complement(space, event):
    return 1 - probability(space, event)


def union(space, a, b):
    both = probability(space, lambda o: a(o) and b(o))
    return probability(space, a) + probability(space, b) - both


def independent(space, a, b):
    both = probability(space, lambda o: a(o) and b(o))
    return both == probability(space, a) * probability(space, b)
''',
"explanation": r'''
Events are predicates, so intersections are built by combining predicates with `and`. Every
probability is an exact `Fraction`, which makes the independence test an exact equality, and the
union follows the inclusion–exclusion formula rather than counting directly.
''',
"tests": r'''
from fractions import Fraction


class TestProbability(unittest.TestCase):
    def setUp(self):
        self.space = S.two_dice()

    def test_space(self):
        self.assertEqual(len(self.space), 36)
        self.assertEqual(self.space[:3], [(1, 1), (1, 2), (1, 3)])
        self.assertEqual(self.space[-1], (6, 6))

    def test_probability_exact(self):
        p = S.probability(self.space, lambda o: sum(o) == 7)
        self.assertIsInstance(p, Fraction)
        self.assertEqual(p, Fraction(1, 6))
        self.assertEqual(S.probability(self.space, lambda o: sum(o) == 13), 0)

    def test_complement(self):
        self.assertEqual(S.complement(self.space, lambda o: o == (6, 6)), Fraction(35, 36))

    def test_union_overlap(self):
        p = S.union(self.space, lambda o: o[0] == 6, lambda o: o[1] == 6)
        self.assertEqual(p, Fraction(11, 36))

    def test_union_matches_direct_count(self):
        a = lambda o: sum(o) >= 10
        b = lambda o: o[0] == o[1]
        direct = S.probability(self.space, lambda o: a(o) or b(o))
        self.assertEqual(S.union(self.space, a, b), direct)

    def test_independence(self):
        even_first = lambda o: o[0] % 2 == 0
        self.assertTrue(S.independent(self.space, even_first, lambda o: sum(o) == 7))
        self.assertFalse(S.independent(self.space, even_first, lambda o: sum(o) == 12))
        coin = ["H", "T"]
        self.assertFalse(S.independent(coin, lambda o: o == "H", lambda o: o == "T"))

    def test_empty_space(self):
        with self.assertRaises(ValueError):
            S.probability([], lambda o: True)
''',
"feedback": [
    ("test_space", "Use two nested loops (or a nested comprehension) over 1..6, first die outer."),
    ("test_probability_exact", "Return `Fraction(count, len(space))`, not a float."),
    ("test_union_overlap", "Subtract the probability of both events, which inclusion–exclusion counts twice."),
    ("test_independence", "Compare P(A and B) with P(A) * P(B) using Fractions."),
    ("test_empty_space", "Raise ValueError when the sample space is empty."),
],
"library": {
"text": r'''
The nested comprehension in `two_dice` is what `itertools.product(range(1, 7), repeat=2)`
generates, and `Fraction` is the standard library's exact rational type. There is no library
function for "probability of a predicate" — counting is the method. The test below confirms
the `itertools` version gives the same space.
''',
"tests": r'''
import itertools


class TestAgainstLibrary(unittest.TestCase):
    def test_space_matches_itertools(self):
        self.assertEqual(S.two_dice(), list(itertools.product(range(1, 7), repeat=2)))
''',
},
},
# ---------------------------------------------------------------- conditional-bayes
{
"slug": "conditional-bayes", "title": "Conditional Probability and Bayes' Rule",
"difficulty": "intermediate", "prereqs": ["probability-basics"], "packages": [],
"objectives": ["Compute P(A | B) by restricting the sample space",
               "Derive and apply Bayes' rule with the law of total probability",
               "Explain the base-rate effect", "Update a belief after several observations"],
"tags": ["conditional-probability", "bayes-rule", "base-rate", "posterior"],
"sources": ["S011", "S010"], "entry": "conditional(space, a, b); posterior(prior, sensitivity, false_positive_rate); update(prior, sensitivity, false_positive_rate, results)",
"article": r'''
# Conditional Probability and Bayes' Rule

## Intuition
Knowing something changes the odds. Among two-dice rolls, $P(\text{total} = 8)$ is 5/36, but if
you are told the first die shows 6, only the 6 outcomes starting with 6 remain and one of them
totals 8: the probability becomes 1/6. Conditioning means *shrinking the sample space* to the
outcomes consistent with what you know.

## Precise explanation
$$P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0.$$
**Bayes' rule** reverses a conditional:
$$P(D \mid +) = \frac{P(+ \mid D)\,P(D)}{P(+)}, \qquad
  P(+) = P(+ \mid D)P(D) + P(+ \mid \neg D)P(\neg D).$$
For a medical test: $P(D)$ is the **prior** (how common the disease is), $P(+ \mid D)$ the
**sensitivity**, $P(+ \mid \neg D)$ the **false-positive rate**, and $P(D \mid +)$ the
**posterior**. For a negative result use $P(- \mid D) = 1 - \text{sensitivity}$ and
$P(- \mid \neg D) = 1 - \text{false-positive rate}$.

**Sequential updating**: after one result, the posterior becomes the prior for the next
(assuming results are independent given the true state).

## Worked example
Prior 1%, sensitivity 90%, false-positive rate 5%:
$P(+) = 0.9 \cdot 0.01 + 0.05 \cdot 0.99 = 0.0585$, so $P(D \mid +) = 0.009 / 0.0585 \approx 0.154$.
A positive test raises the probability from 1% to only about 15% because healthy people vastly
outnumber sick ones — the **base-rate effect**.

## Common mistakes
* Confusing $P(+ \mid D)$ (90%) with $P(D \mid +)$ (15%).
* Forgetting the false positives in the denominator.
* Dividing by $P(B) = 0$.

## Why this matters
Naive Bayes text classification ([[naive-bayes-text]]) is Bayes' rule applied to words, and
reasoning about precision versus recall ([[classification-metrics]]) is reasoning about base rates.
''',
"statement": r'''
Implement:

1. `conditional(space, a, b)` → $P(A \mid B)$ as a `Fraction`, counting outcomes in a list of
   equally likely outcomes; raise `ValueError` if no outcome satisfies `b`.
2. `posterior(prior, sensitivity, false_positive_rate)` → $P(D \mid +)$ as a float.
3. `update(prior, sensitivity, false_positive_rate, results)` → the probability of $D$ after
   applying Bayes' rule once per result in `results` (a list of booleans: `True` = positive,
   `False` = negative), in order. An empty list returns the prior.

**Examples**
```python
dice = [(a, b) for a in range(1, 7) for b in range(1, 7)]
conditional(dice, lambda o: sum(o) == 8, lambda o: o[0] == 6)   # Fraction(1, 6)
posterior(0.01, 0.9, 0.05)                                     # ≈ 0.1538
update(0.01, 0.9, 0.05, [True, True])                          # ≈ 0.7660
```
''',
"starter": r'''
from fractions import Fraction


def conditional(space, a, b):
    # TODO
    return Fraction(0)


def posterior(prior, sensitivity, false_positive_rate):
    # TODO: Bayes' rule
    return prior


def update(prior, sensitivity, false_positive_rate, results):
    # TODO: one Bayes update per result
    return prior
''',
"hints": [
    "Count outcomes where `b` holds, and among those where `a` also holds; divide.",
    "`evidence = sensitivity * prior + false_positive_rate * (1 - prior)`; posterior = numerator / evidence.",
    "For a negative result use `1 - sensitivity` and `1 - false_positive_rate` as the likelihoods.",
],
"solution": r'''
from fractions import Fraction


def conditional(space, a, b):
    given = [o for o in space if b(o)]
    if not given:
        raise ValueError("conditioning event has probability 0")
    return Fraction(sum(1 for o in given if a(o)), len(given))


def posterior(prior, sensitivity, false_positive_rate):
    evidence = sensitivity * prior + false_positive_rate * (1 - prior)
    return sensitivity * prior / evidence


def update(prior, sensitivity, false_positive_rate, results):
    p = prior
    for positive in results:
        if positive:
            like_d, like_not = sensitivity, false_positive_rate
        else:
            like_d, like_not = 1 - sensitivity, 1 - false_positive_rate
        p = like_d * p / (like_d * p + like_not * (1 - p))
    return p
''',
"explanation": r'''
Conditioning keeps only the outcomes where `b` holds and counts `a` among them, which equals
$P(A\cap B)/P(B)$. The posterior divides the true-positive mass by all positive mass. `update`
reuses the same formula with likelihoods chosen by each result, feeding each posterior forward as
the next prior.
''',
"tests": r'''
from fractions import Fraction

DICE = [(a, b) for a in range(1, 7) for b in range(1, 7)]


class TestBayes(unittest.TestCase):
    def test_conditional_dice(self):
        self.assertEqual(S.conditional(DICE, lambda o: sum(o) == 8, lambda o: o[0] == 6), Fraction(1, 6))
        self.assertEqual(S.conditional(DICE, lambda o: o[0] == 6, lambda o: sum(o) == 12), 1)

    def test_conditional_matches_definition(self):
        a = lambda o: o[0] > o[1]
        b = lambda o: sum(o) >= 9
        both = Fraction(sum(1 for o in DICE if a(o) and b(o)), 36)
        pb = Fraction(sum(1 for o in DICE if b(o)), 36)
        self.assertEqual(S.conditional(DICE, a, b), both / pb)

    def test_conditional_zero(self):
        with self.assertRaises(ValueError):
            S.conditional(DICE, lambda o: True, lambda o: sum(o) > 12)

    def test_posterior_base_rate(self):
        self.assertAlmostEqual(S.posterior(0.01, 0.9, 0.05), 0.009 / 0.0585, places=12)

    def test_posterior_edge(self):
        self.assertAlmostEqual(S.posterior(0.5, 0.8, 0.8), 0.5)
        self.assertAlmostEqual(S.posterior(0.2, 1.0, 0.0), 1.0)

    def test_update_two_positives(self):
        p1 = S.posterior(0.01, 0.9, 0.05)
        self.assertAlmostEqual(S.update(0.01, 0.9, 0.05, [True, True]), S.posterior(p1, 0.9, 0.05))
        self.assertAlmostEqual(S.update(0.01, 0.9, 0.05, [True, True]), 0.7659574468, places=8)

    def test_update_negative_and_empty(self):
        self.assertEqual(S.update(0.3, 0.9, 0.05, []), 0.3)
        neg = S.update(0.3, 0.9, 0.05, [False])
        self.assertAlmostEqual(neg, 0.1 * 0.3 / (0.1 * 0.3 + 0.95 * 0.7))
        self.assertLess(neg, 0.3)
''',
"feedback": [
    ("test_conditional_dice", "Restrict to outcomes where `b` holds, then count `a` among them."),
    ("test_conditional_zero", "Raise ValueError when no outcome satisfies the condition."),
    ("test_posterior_base_rate", "The denominator must include false positives from the healthy group: `fpr * (1 - prior)`."),
    ("test_update_two_positives", "Use each posterior as the prior for the next result."),
    ("test_update_negative_and_empty", "For a negative result the likelihoods are `1 - sensitivity` and `1 - false_positive_rate`."),
],
},
# ---------------------------------------------------------------- normal-distribution
{
"slug": "normal-distribution", "title": "The Normal Distribution",
"difficulty": "intermediate", "prereqs": ["z-scores", "binomial-pmf"], "packages": [],
"objectives": ["Evaluate the normal density and cumulative probability with math.exp and math.erf",
               "Compute interval probabilities and the 68–95–99.7 rule",
               "Approximate a binomial probability with a continuity correction",
               "Compare a manual formula with statistics.NormalDist"],
"tags": ["normal-distribution", "pdf", "cdf", "erf", "normal-approximation"],
"sources": ["S011", "S003", "S050"], "entry": "normal_pdf(x, mu, sigma); normal_cdf(x, mu, sigma); prob_between(a, b, mu, sigma); empirical_rule(); binomial_cdf_approx(k, n, p)",
"article": r'''
# The Normal Distribution

## Intuition
Heights, measurement errors and averages of many small effects pile up in a symmetric bell
shape. The **normal distribution** $\mathcal N(\mu, \sigma^2)$ describes that bell: $\mu$ is its
centre and $\sigma$ its width. Because it is continuous, we ask for the probability of an
*interval*, which is the area under the curve.

## Precise explanation
**Density (pdf)**
$$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right).$$
**Cumulative probability (cdf)**, using the error function `math.erf`:
$$F(x) = P(X \le x) = \tfrac12\left[1 + \operatorname{erf}\!\left(\frac{x-\mu}{\sigma\sqrt2}\right)\right].$$
* $P(a \le X \le b) = F(b) - F(a)$. A single point has probability 0; $f(x)$ is a density, not a
  probability, and can exceed 1 when $\sigma$ is small.
* Standardising with $z = (x - \mu)/\sigma$ ([[z-scores]]) turns any normal into $\mathcal N(0, 1)$.
* **68–95–99.7 rule**: about 68.27%, 95.45% and 99.73% of the mass lies within 1, 2 and 3
  standard deviations of the mean.
* **Normal approximation to the binomial** ([[binomial-pmf]]): for large $n$,
  $X \sim \text{Bin}(n, p)$ is close to $\mathcal N(np,\, np(1-p))$, and
  $P(X \le k) \approx F(k + 0.5)$ — the $+0.5$ **continuity correction** accounts for replacing
  bars at integers with a smooth curve.

## Worked example
$\mathcal N(170, 10^2)$: $P(X \le 180) = F(180) = \frac12[1 + \operatorname{erf}(1/\sqrt2)] \approx 0.8413$;
$P(160 \le X \le 180) \approx 0.8413 - 0.1587 = 0.6827$.

## Common mistakes
* Passing the variance where the standard deviation is expected.
* Treating $f(x)$ as $P(X = x)$.
* Forgetting the $\sqrt2$ inside the erf.

## Why this matters
Confidence intervals ([[sampling-distribution]]), the t-test ([[welch-t]]), weight
initialisation and Gaussian noise for privacy all use the normal distribution.
''',
"statement": r'''
Implement with `math` only:

1. `normal_pdf(x, mu=0.0, sigma=1.0)` and 2. `normal_cdf(x, mu=0.0, sigma=1.0)` from the formulas
   above; raise `ValueError` if `sigma <= 0`.
3. `prob_between(a, b, mu=0.0, sigma=1.0)` → $F(b) - F(a)$ (raise `ValueError` if `b < a`).
4. `empirical_rule()` → `{1: p1, 2: p2, 3: p3}`, the probabilities of lying within 1, 2, 3
   standard deviations of the mean.
5. `binomial_cdf_approx(k, n, p)` → normal approximation of $P(X \le k)$ for
   $X \sim \text{Bin}(n, p)$ with the continuity correction.

**Examples**
```python
normal_cdf(0)                    # 0.5
prob_between(160, 180, 170, 10)  # ≈ 0.6827
empirical_rule()[2]              # ≈ 0.9545
binomial_cdf_approx(55, 100, 0.5)  # ≈ 0.8643
```
''',
"starter": r'''
import math


def normal_pdf(x, mu=0.0, sigma=1.0):
    # TODO
    return 0.0


def normal_cdf(x, mu=0.0, sigma=1.0):
    # TODO: use math.erf
    return 0.0


def prob_between(a, b, mu=0.0, sigma=1.0):
    # TODO
    return 0.0


def empirical_rule():
    # TODO
    return {}


def binomial_cdf_approx(k, n, p):
    # TODO: mean n*p, sd sqrt(n*p*(1-p)), continuity correction k + 0.5
    return 0.0
''',
"hints": [
    "pdf: `math.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))`.",
    "cdf: `0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))`.",
    "The empirical rule is `prob_between(-k, k)` for k = 1, 2, 3.",
],
"solution": r'''
import math


def _check(sigma):
    if sigma <= 0:
        raise ValueError("sigma must be positive")


def normal_pdf(x, mu=0.0, sigma=1.0):
    _check(sigma)
    return math.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * math.pi))


def normal_cdf(x, mu=0.0, sigma=1.0):
    _check(sigma)
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))


def prob_between(a, b, mu=0.0, sigma=1.0):
    if b < a:
        raise ValueError("need a <= b")
    return normal_cdf(b, mu, sigma) - normal_cdf(a, mu, sigma)


def empirical_rule():
    return {k: prob_between(-k, k) for k in (1, 2, 3)}


def binomial_cdf_approx(k, n, p):
    mu = n * p
    sigma = math.sqrt(n * p * (1 - p))
    return normal_cdf(k + 0.5, mu, sigma)
''',
"explanation": r'''
The density and cdf are direct translations of their formulas; the cdf relies on `math.erf`,
which the standard library computes accurately. Interval probabilities are differences of the
cdf, the empirical rule reuses that on the standard normal, and the binomial approximation plugs
the binomial mean and standard deviation into the normal cdf at $k + 0.5$.
''',
"tests": r'''
class TestNormal(unittest.TestCase):
    def test_pdf(self):
        self.assertAlmostEqual(S.normal_pdf(0), 1 / math.sqrt(2 * math.pi))
        self.assertAlmostEqual(S.normal_pdf(172, 170, 2), math.exp(-0.5) / (2 * math.sqrt(2 * math.pi)))
        self.assertGreater(S.normal_pdf(0, 0, 0.1), 1)

    def test_cdf(self):
        self.assertAlmostEqual(S.normal_cdf(0), 0.5)
        self.assertAlmostEqual(S.normal_cdf(180, 170, 10), 0.8413447460685429, places=12)
        self.assertAlmostEqual(S.normal_cdf(-1.5) + S.normal_cdf(1.5), 1.0)

    def test_between(self):
        self.assertAlmostEqual(S.prob_between(160, 180, 170, 10), 0.6826894921370859, places=12)
        with self.assertRaises(ValueError):
            S.prob_between(2, 1)

    def test_empirical_rule(self):
        r = S.empirical_rule()
        self.assertEqual(sorted(r), [1, 2, 3])
        self.assertAlmostEqual(r[1], 0.6827, places=4)
        self.assertAlmostEqual(r[2], 0.9545, places=4)
        self.assertAlmostEqual(r[3], 0.9973, places=4)

    def test_invalid_sigma(self):
        for f in (S.normal_pdf, S.normal_cdf):
            with self.assertRaises(ValueError):
                f(0, 0, 0)

    def test_binomial_approx_close_to_exact(self):
        exact = sum(math.comb(100, i) for i in range(56)) / 2 ** 100
        approx = S.binomial_cdf_approx(55, 100, 0.5)
        self.assertAlmostEqual(approx, S.normal_cdf(55.5, 50, 5))
        self.assertLess(abs(approx - exact), 0.002)
''',
"feedback": [
    ("test_pdf", "Divide by `sigma * sqrt(2*pi)` and square `(x - mu)` inside the exponent."),
    ("test_cdf", "Use `0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))`."),
    ("test_empirical_rule", "Return a dict keyed by 1, 2 and 3 with `prob_between(-k, k)`."),
    ("test_invalid_sigma", "Raise ValueError when sigma <= 0."),
    ("test_binomial_approx_close_to_exact", "Use mean n*p, standard deviation sqrt(n*p*(1-p)) and evaluate at k + 0.5."),
],
"library": {
"text": r'''
`statistics.NormalDist(mu, sigma)` provides `.pdf(x)`, `.cdf(x)` and `.inv_cdf(p)` (the
quantile function you will use for confidence intervals), plus arithmetic on independent normal
variables. `scipy.stats.norm` offers the same functions vectorised over arrays. The tests compare
your functions with `NormalDist`, and with SciPy if it is installed.
''',
"optional": ["scipy"],
"tests": r'''
from statistics import NormalDist

try:
    import scipy.stats as _stats
except ImportError:
    _stats = None


class TestAgainstLibrary(unittest.TestCase):
    def test_matches_normaldist(self):
        d = NormalDist(3, 2)
        for x in (-4.0, 0.0, 3.0, 5.5):
            self.assertAlmostEqual(S.normal_pdf(x, 3, 2), d.pdf(x), places=12)
            self.assertAlmostEqual(S.normal_cdf(x, 3, 2), d.cdf(x), places=12)

    @unittest.skipIf(_stats is None, "SciPy not installed")
    def test_matches_scipy(self):
        self.assertAlmostEqual(S.normal_cdf(1.2, 0.5, 0.8), float(_stats.norm.cdf(1.2, 0.5, 0.8)), places=12)
''',
},
},
# ---------------------------------------------------------------- sampling-distribution
{
"slug": "sampling-distribution", "title": "Sampling Distributions and Standard Error",
"difficulty": "advanced", "prereqs": ["dice-lln", "normal-distribution"], "packages": [],
"objectives": ["Simulate the sampling distribution of the mean with a seeded generator",
               "Compute the standard error s / √n and explain how it shrinks with n",
               "Build a normal-approximation 95% confidence interval",
               "Describe what the central limit theorem does and does not promise"],
"tags": ["sampling-distribution", "standard-error", "central-limit-theorem", "confidence-interval"],
"sources": ["S011", "S010", "S003", "S004"], "entry": "sample_means(population, n, reps, seed); standard_error(sample); mean_ci95(sample)",
"article": r'''
# Sampling Distributions and Standard Error

## Intuition
Take a random sample of 30 students and compute their mean height. Take another sample and the
mean changes a little. The **sampling distribution** is the distribution of that mean over all
possible samples. It is narrower than the population — averages vary less than individuals — and
it gets narrower as the sample grows.

## Precise explanation
* If individual values have standard deviation $\sigma$, the mean of $n$ independent values has
  standard deviation $\sigma / \sqrt n$. Quadrupling $n$ halves it.
* We rarely know $\sigma$, so we estimate it with the sample standard deviation $s$ (dividing by
  $n-1$, [[mean-variance]]): the **standard error** is $\mathrm{SE} = s / \sqrt n$.
* **Central limit theorem (CLT)**: for large $n$ the sampling distribution of the mean is
  approximately normal ([[normal-distribution]]), even when the data are not. It says nothing
  about small samples or heavy outliers, and it assumes independent draws.
* **Normal-approximation 95% interval**: $\bar x \pm z\,\mathrm{SE}$ with $z \approx 1.96$
  (`NormalDist().inv_cdf(0.975)`). "95%" describes the *procedure*: about 95% of intervals built
  this way contain the true mean.

**Simulating sampling with replacement** (reproducibly): with `rng = random.Random(seed)`, draw
an index `int(rng.random() * len(population))` for each of the $n$ values.

## Worked example
Population of die faces 1..6: $\sigma = \sqrt{35/12} \approx 1.708$. For $n = 25$, the means of many
samples have standard deviation about $1.708/5 \approx 0.342$, and their histogram is close to a
bell even though each face is uniform.

## Common mistakes
* Using $\sigma$ of the data as the uncertainty of the mean (forgetting $\sqrt n$).
* Dividing by $n$ instead of $n - 1$ when estimating $s$.
* Saying "there is a 95% probability the true mean is in *this* interval".

## Why this matters
Standard errors are the denominator of the t-statistic ([[welch-t]]), and the bootstrap
([[bootstrap-ci]]) estimates the same sampling distribution by resampling your data.
''',
"statement": r'''
Implement:

1. `sample_means(population, n, reps, seed)` → a list of `reps` sample means. Use one
   `rng = random.Random(seed)`; for each repetition draw `n` values with replacement, each as
   `population[int(rng.random() * len(population))]`, and record their mean.
2. `standard_error(sample)` → $s / \sqrt n$ with the $n-1$ sample standard deviation; raise
   `ValueError` if the sample has fewer than 2 values.
3. `mean_ci95(sample)` → `(low, high)` = mean ∓ z · SE with `z = NormalDist().inv_cdf(0.975)`.

**Example**
```python
means = sample_means([1, 2, 3, 4, 5, 6], 25, 2000, seed=0)
len(means)                 # 2000
# their standard deviation is close to 1.708 / 5 ≈ 0.342
standard_error([2, 4, 4, 4, 5, 5, 7, 9])   # ≈ 0.7559
```
''',
"starter": r'''
import math
import random
from statistics import NormalDist


def sample_means(population, n, reps, seed):
    # TODO
    return []


def standard_error(sample):
    # TODO
    return 0.0


def mean_ci95(sample):
    # TODO
    return (0.0, 0.0)
''',
"hints": [
    "Create the generator once, outside the repetitions loop, so each repetition continues the stream.",
    "Sample variance: `sum((x - m) ** 2 for x in sample) / (n - 1)`; SE is `sqrt(var) / sqrt(n)`.",
    "`z = NormalDist().inv_cdf(0.975)`; return `(m - z * se, m + z * se)`.",
],
"solution": r'''
import math
import random
from statistics import NormalDist


def sample_means(population, n, reps, seed):
    rng = random.Random(seed)
    size = len(population)
    means = []
    for _ in range(reps):
        total = 0
        for _ in range(n):
            total += population[int(rng.random() * size)]
        means.append(total / n)
    return means


def standard_error(sample):
    n = len(sample)
    if n < 2:
        raise ValueError("need at least two values")
    m = sum(sample) / n
    var = sum((x - m) ** 2 for x in sample) / (n - 1)
    return math.sqrt(var) / math.sqrt(n)


def mean_ci95(sample):
    m = sum(sample) / len(sample)
    se = standard_error(sample)
    z = NormalDist().inv_cdf(0.975)
    return (m - z * se, m + z * se)
''',
"explanation": r'''
A single seeded generator produces every draw, so the whole simulation is reproducible and
uses only `random()`, whose output Python guarantees across versions. The standard error uses the
unbiased $n-1$ variance, and the interval combines it with the exact 97.5% normal quantile.
''',
"tests": r'''
import random
import statistics


def reference_means(population, n, reps, seed):
    rng = random.Random(seed)
    out = []
    for _ in range(reps):
        out.append(sum(population[int(rng.random() * len(population))] for _ in range(n)) / n)
    return out


class TestSamplingDistribution(unittest.TestCase):
    def test_recipe_matches(self):
        pop = [3, 1, 4, 1, 5, 9, 2, 6]
        self.assertEqual(S.sample_means(pop, 5, 50, seed=11), reference_means(pop, 5, 50, 11))

    def test_reproducible(self):
        a = S.sample_means([1, 2, 3], 4, 10, seed=3)
        self.assertEqual(a, S.sample_means([1, 2, 3], 4, 10, seed=3))
        self.assertNotEqual(a, S.sample_means([1, 2, 3], 4, 10, seed=4))

    def test_spread_shrinks_like_sqrt_n(self):
        die = [1, 2, 3, 4, 5, 6]
        sigma = statistics.pstdev(die)
        for n in (4, 25):
            sd = statistics.pstdev(S.sample_means(die, n, 3000, seed=1))
            self.assertAlmostEqual(sd / (sigma / math.sqrt(n)), 1.0, delta=0.06)

    def test_centre(self):
        means = S.sample_means([1, 2, 3, 4, 5, 6], 10, 3000, seed=2)
        self.assertAlmostEqual(statistics.fmean(means), 3.5, delta=0.05)

    def test_standard_error(self):
        self.assertAlmostEqual(S.standard_error([2, 4, 4, 4, 5, 5, 7, 9]), statistics.stdev([2, 4, 4, 4, 5, 5, 7, 9]) / math.sqrt(8))
        with self.assertRaises(ValueError):
            S.standard_error([1])

    def test_ci95(self):
        data = [2, 4, 4, 4, 5, 5, 7, 9]
        low, high = S.mean_ci95(data)
        se = S.standard_error(data)
        self.assertAlmostEqual((low + high) / 2, 5.0)
        self.assertAlmostEqual(high - low, 2 * 1.959963984540054 * se, places=9)
''',
"feedback": [
    ("test_recipe_matches", "Create one `random.Random(seed)` and draw indices with `int(rng.random() * len(population))`, n per repetition."),
    ("test_spread_shrinks_like_sqrt_n", "Each repetition must draw n values with replacement and record their mean."),
    ("test_standard_error", "Use the n - 1 sample standard deviation divided by sqrt(n)."),
    ("test_ci95", "Use `NormalDist().inv_cdf(0.975)` (≈ 1.96) times the standard error on both sides of the mean."),
],
"library": {
"text": r'''
`statistics.stdev(sample) / math.sqrt(len(sample))` gives the same standard error, and
`random.Random(seed).choices(population, k=n)` draws with replacement in one call (its exact
sequence is not guaranteed across Python versions, which is why the graded version builds
indices from `random()`). `scipy.stats.sem` computes the standard error for arrays.
''',
"optional": ["scipy"],
"tests": r'''
try:
    import scipy.stats as _stats
except ImportError:
    _stats = None


class TestAgainstLibrary(unittest.TestCase):
    def test_matches_statistics_stdev(self):
        data = [1.2, 3.4, 2.2, 5.0, 4.1]
        self.assertAlmostEqual(S.standard_error(data), statistics.stdev(data) / math.sqrt(5), places=12)

    @unittest.skipIf(_stats is None, "SciPy not installed")
    def test_matches_scipy_sem(self):
        data = [1.2, 3.4, 2.2, 5.0, 4.1]
        self.assertAlmostEqual(S.standard_error(data), float(_stats.sem(data)), places=12)
''',
},
},
]
