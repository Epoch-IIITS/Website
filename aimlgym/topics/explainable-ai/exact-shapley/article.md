# Shapley Values

## Learning outcomes

After this lesson you can:

- Define a coalition value function with a baseline
- Compute exact Shapley values by enumerating subsets
- Verify efficiency, symmetry and dummy properties

## Intuition
Features are players in a cooperative game whose payout is the prediction. A fair split gives each
player their average marginal contribution over every order in which players could join.

## Precise explanation
Value of a coalition $S$ (baseline/interventional version): evaluate the model on an input that takes
$x_j$ for $j\in S$ and the baseline $x'_j$ otherwise: $v(S) = f(x_S, x'_{\bar S})$.
Shapley value of feature $j$ among $d$ features:
$$\phi_j = \sum_{S\subseteq N\setminus\{j\}} \frac{|S|!\,(d-|S|-1)!}{d!}\,\big[v(S\cup\{j\}) - v(S)\big].$$
Properties (Lundberg & Lee 2017; Molnar ch. "Shapley values"):
* **Efficiency:** $\sum_j\phi_j = f(x) - f(x')$.
* **Symmetry:** interchangeable features get equal values.
* **Dummy:** a feature that never changes $v$ gets 0.
For a linear model, $\phi_j = w_j(x_j - x'_j)$ (XA-01). Exact computation needs $2^d$ model calls —
feasible only for small d; SHAP approximates it for larger models.

## Worked example
f(x) = x₀·x₁, x = (1, 1), baseline (0, 0): v(∅) = 0, v({0}) = 0, v({1}) = 0, v({0,1}) = 1 →
φ₀ = ½(0 − 0) + ½(1 − 0) = 0.5, φ₁ = 0.5. The interaction is split equally.

## Common mistakes
* Wrong weights (use $|S|!(d-|S|-1)!/d!$).
* Forgetting the empty coalition.
* Different baselines give different (both valid) explanations — report which you used.

## Why this matters
SHAP is one of the most widely used explanation tools; implementing the exact formula shows what the
approximations approximate.

## References

- [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874) — Scott Lundberg, Su-In Lee (`S026`)
- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
