# ST-P1 · Project idea: A/B Test Analyser

**Topic:** Statistics · ungraded

## Brief

Build a small tool that a product team could use after an experiment: give it the results for
version A and version B of a page (conversions or a numeric metric such as time on page) and it
reports the effect size, a confidence interval, and whether the difference is statistically
significant — in plain language a non-statistician can act on.

## You will use

- ST-13 Bootstrap Confidence Interval
- ST-14 Introducing scipy.stats
- ST-15 Chi-Square Test with SciPy
- ST-17 Welch's t-test with SciPy
- ST-19 Permutation Test with SciPy

## Milestones

1. Read two groups of numbers from a CSV file and print their sizes, means and standard deviations.
2. Report the difference in means with a 95% bootstrap confidence interval.
3. Add Welch's t-test and a permutation test and print both p-values side by side.
4. Support conversion data (converted yes/no) with a chi-square test on the 2×2 table of counts.
5. Write a one-paragraph summary: effect, interval, p-value and a recommendation with its caveats.

## Stretch goals

- Estimate the sample size needed to detect a given effect (power analysis) by simulation.
- Show what goes wrong when you check the p-value every day and stop early ('peeking').
- Handle more than two variants and correct for multiple comparisons.

## Data

Generate data yourself with NumPy: for example 2,000 visitors per version with conversion rates
of 10% and 11% (`rng.random(2000) < 0.11`), or times drawn from `rng.lognormal`. Changing the true
effect and the sample size shows when a test can and cannot detect it.

## Run it yourself

```bash
pip install numpy scipy pandas
python ab_test.py results.csv
```
Keep the analysis in functions so you can test each one with `unittest`, as in the course steps.
