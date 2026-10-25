# Statistics

**You will be able to:** Describe data, reason with probability, conditional probability and Bayes' rule, use the binomial and normal distributions, simulate, and run interval estimates and hypothesis tests by hand and with scipy.stats.

**Topic prerequisites:** Mathematics for AI/ML

Describing data first (mean, variance, median, percentiles, histograms, z-scores), then
probability (sample spaces, conditional probability, Bayes' rule), two named distributions
(binomial and normal), simulation and the law of large numbers, correlation, sampling
distributions and standard errors, and bootstrap intervals. The topic ends with
`scipy.stats`: distribution objects, then the chi-square test, Welch's t-test and the
permutation test, each followed by an optional deep dive that computes the same test by hand.

**Packages:** standard library, then `scipy` for the last four required steps. Random
simulations use `random.Random(seed).random()`, whose sequence Python documents as reproducible.
**Project ideas:** an A/B test analyser and a dice-and-coin simulator.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | ST-01 | [Mean and Variance (Population vs Sample)](mean-variance/problem.md) | beginner | MA-01 |
| 2 | ST-02 | [Median and Mode](median-mode/problem.md) | beginner | ST-01 |
| 3 | ST-03 | [Percentiles by Linear Interpolation](percentiles/problem.md) | beginner | ST-02 |
| 4 | ST-04 | [Histogram with Equal-Width Bins](histogram-bins/problem.md) | beginner | ST-01 |
| 5 | ST-05 | [Standardize to z-scores](z-scores/problem.md) | beginner | ST-01 |
| 6 | ST-06 | [Probability by Counting Outcomes](probability-basics/problem.md) | intermediate | ST-04 |
| 7 | ST-07 | [Conditional Probability and Bayes' Rule](conditional-bayes/problem.md) | intermediate | ST-06 |
| 8 | ST-08 | [Binomial Probabilities](binomial-pmf/problem.md) | intermediate | ST-06, MA-07 |
| 9 | ST-09 | [The Normal Distribution](normal-distribution/problem.md) | intermediate | ST-05, ST-08 |
| 10 | ST-10 | [Dice Simulation and the Law of Large Numbers](dice-lln/problem.md) | intermediate | ST-06 |
| 11 | ST-11 | [Covariance and Pearson Correlation](covariance-correlation/problem.md) | intermediate | ST-05, MA-04 |
| 12 | ST-12 | [Sampling Distributions and Standard Error](sampling-distribution/problem.md) | advanced | ST-10, ST-09 |
| 13 | ST-13 | [Bootstrap Confidence Interval](bootstrap-ci/problem.md) | advanced | ST-12, ST-03 |
| 14 | ST-14 | [Introducing scipy.stats](scipy-stats-intro/problem.md) | advanced | ST-09 |
| 15 | ST-15 | [Chi-Square Test with SciPy](chi-square-scipy/problem.md) | advanced | ST-14 |
| 16 | ST-16 | [Chi-Square Goodness of Fit by Hand (optional deep dive)](chi-square-gof/problem.md) | advanced | ST-08 |
| 17 | ST-17 | [Welch's t-test with SciPy](welch-t-scipy/problem.md) | advanced | ST-15, ST-12 |
| 18 | ST-18 | [Welch's t-statistic by Hand (optional deep dive)](welch-t/problem.md) | advanced | ST-12 |
| 19 | ST-19 | [Permutation Test with SciPy](permutation-test-scipy/problem.md) | advanced | ST-17 |
| 20 | ST-20 | [Permutation Test for a Mean Difference by Hand (optional deep dive)](permutation-test/problem.md) | advanced | ST-13, ST-18 |
| 21 | ST-P1 | [Project idea: A/B Test Analyser](ab-test-analyser/project.md) | ungraded | ST-13, ST-14, ST-15, ST-17, ST-19 |
| 22 | ST-P2 | [Project idea: Dice and Coin Simulator](dice-coin-simulator/project.md) | ungraded | ST-10, ST-04, ST-08, ST-12, ST-14 |
