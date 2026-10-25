# Permutation Feature Importance

## Learning outcomes

After this lesson you can:

- Measure importance as the score drop after permuting a feature
- Repeat permutations with a seeded generator and report mean/std
- Interpret near-zero and negative importances

## Intuition
If shuffling a feature's column (destroying its relationship with the target) makes the model much
worse, the model relied on that feature. If nothing changes, the feature didn't matter *to this
model*.

## Precise explanation
1. Baseline score $s_0 = \text{score}(y, f(X))$ (higher = better, e.g. R² or accuracy).
2. For each feature $j$ and repeat $r$: permute column j (rows shuffled with
   `rng.permutation(n)`), compute $s_{j,r}$.
3. Importance $I_j = s_0 - \text{mean}_r\, s_{j,r}$, with standard deviation across repeats.
Use **one** generator `default_rng(seed)`, iterating features in order and repeats inside.
Small negative values mean "no importance" (noise). Correlated features share importance — permuting
one can be compensated by the other. Computing on held-out data measures importance for
*generalisation*.

## Worked example
y = 3x₀ + noise, x₁ pure noise, linear model: permuting x₀ drops R² from ≈1 to ≈−1; permuting x₁ ≈ 0.

## Common mistakes
* Re-fitting the model after permuting (that is drop-column importance, a different method).
* Permuting all features at once.
* Reporting a single permutation without variability.

## Why this matters
Model-agnostic, cheap and widely used (scikit-learn `permutation_importance`); it also connects to the
permutation test idea from ST-20.

## Library implementation

`sklearn.inspection.permutation_importance(estimator, X, y, n_repeats=..., random_state=...)`
implements the same algorithm for fitted scikit-learn models (and pipelines). It uses its own
random shuffles, so individual numbers differ slightly from yours, but the ranking of clearly
important features agrees. The comparison runs when scikit-learn is installed.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
