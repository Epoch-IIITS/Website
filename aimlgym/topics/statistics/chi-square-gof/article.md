# Chi-Square Goodness of Fit

## Learning outcomes

After this lesson you can:

- Compute expected counts from probabilities
- Compute the chi-square statistic and degrees of freedom
- Make a decision with a critical value

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

## Library implementation

`scipy.stats.chisquare(observed, f_exp=expected)` returns the same statistic together with a
p-value from the chi-square distribution with `len(observed) - 1` degrees of freedom, so you do not
need a critical-value table. The comparison runs only when SciPy is installed.

## References

- [OpenIntro Statistics](https://www.openintro.org/book/os/) — OpenIntro (`S011`)
- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
