# Partial Dependence Plots

## Learning outcomes

After this lesson you can:

- Average ICE curves over a dataset to get partial dependence
- Centre curves at the first grid point
- Detect interactions via ICE spread

## Intuition
An ICE curve shows one instance; the **partial dependence** (PD) curve averages ICE curves over the
whole dataset — the model's average response to a feature, marginalising the others.

## Precise explanation
$$\text{PD}_j(g) = \frac1n\sum_{i=1}^{n} f(x_i \text{ with } x_{ij} := g).$$
Vectorised: for each grid value, set column j of a copy of X to g and average predictions (or build
one big `(m·n, d)` batch). **Centred** PD subtracts the value at the first grid point, so curves start
at 0. If ICE curves have very different shapes (large spread after centring), the feature
**interacts** with others and the PD average hides it.
scikit-learn's `inspection.partial_dependence` implements the same estimator.

## Worked example
f(X) = X₀·X₁, data X₁ ∈ {−1, +1} (mean 0): every ICE curve has slope ±1, the PD curve is flat (0) —
a pure interaction that PD alone would misread as "no effect".

## Common mistakes
* Averaging features instead of predictions.
* Extrapolating the grid far outside the data.
* Reading PD causally.

## Why this matters
PD plots are the most common global explanation for tabular models.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
