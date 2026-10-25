# z-scores

## Learning outcomes

After this lesson you can:

- Standardize data
- Interpret z-scores
- Flag outliers with a |z| threshold

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

## References

- [Think Stats (3rd edition)](https://greenteapress.com/wp/think-stats-3e/) — Allen B. Downey (`S010`)
