# LIME: Local Interpretable Model-agnostic Explanations

## Learning outcomes

After this lesson you can:

- Perturb an instance with binary feature masks
- Weight samples by proximity with an exponential kernel
- Fit a weighted linear model and read local coefficients

## Intuition
A complex model may be curved globally but almost linear in a small neighbourhood of one input. LIME
samples variations of the instance, asks the model about them, and fits a simple linear model that
is accurate *near* the instance.

## Precise explanation (Ribeiro et al., 2016, tabular variant used here)
1. **Interpretable representation:** binary masks $z \in \{0,1\}^d$; $z_j = 1$ keeps $x_j$, $z_j = 0$
   replaces it with the baseline value. Input for mask z: $x(z) = z\odot x + (1-z)\odot x'$.
2. **Sample** masks (always include the all-ones mask = the instance itself).
3. **Proximity weights:** with distance $D(z) = 1 - \frac{1}{d}\sum_j z_j$ (fraction of features
   removed), $\pi(z) = \exp(-D^2/\sigma^2)$, σ = kernel width.
4. **Weighted least squares:** fit $g(z) = \beta_0 + \beta\cdot z$ minimising
   $\sum \pi(z)(f(x(z)) - g(z))^2$: solve with rows scaled by $\sqrt{\pi}$.
The coefficient $\beta_j$ estimates the effect of including feature j. For a linear model $f$, LIME
recovers $\beta_j = w_j(x_j - x'_j)$ exactly (same as XA-01/XA-11).

## Worked example
f(x) = 2x₀ − x₁, x = (3, 1), baseline 0 → β = [6, −1], β₀ = 0, for any set of masks that spans the space.

## Common mistakes
* Fitting on raw perturbed features instead of the binary masks (changes what β means).
* Forgetting the weights (fits a global, not local, model).
* Too few samples → unstable explanations (re-run with other seeds to check).

## Why this matters
LIME is a widely used model-agnostic local explainer; implementing it shows exactly which design
choices (baseline, kernel width, sampling) affect explanations.

## References

- ["Why Should I Trust You?": Explaining the Predictions of Any Classifier](https://arxiv.org/abs/1602.04938) — Marco Tulio Ribeiro, Sameer Singh, Carlos Guestrin (`S025`)
- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
