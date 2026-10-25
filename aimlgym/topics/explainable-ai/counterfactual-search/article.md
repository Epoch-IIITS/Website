# Counterfactual Explanations

## Learning outcomes

After this lesson you can:

- Define a counterfactual as a minimal change that flips a decision
- Search a grid of actionable changes exhaustively
- Respect immutable features and bounds

## Intuition
"Your loan was rejected. If your income were 5 000 higher, it would have been approved." A
counterfactual explains a decision by the smallest realistic change to the input that changes the
outcome — and tells the person what they could do (recourse).

## Precise explanation
For a classifier `predict(X) -> labels`, an instance $x$ with label $c$, and per-feature step sizes
$\delta_j$ (0 = immutable, e.g. age or ethnicity):
* candidate changes: $x_j + k_j\delta_j$ with integers $|k_j| \le K$;
* cost: $\sum_j |k_j|$ (number of unit steps, an L1 distance in step units);
* find the minimum-cost candidate whose label differs from $c$, staying within optional bounds.
Exhaustive search over $(2K+1)^{d_\text{mutable}}$ candidates is fine for small problems and gives the
true minimum; real systems use optimisation or heuristics. Ties: smallest cost, then lexicographically
smallest step vector $k$.

## Worked example
predict = 1 if income + 2·savings ≥ 10; x = (4, 2) → 8 → class 0. Steps (1, 1): cost-1 options
(5, 2) → 9 ✗, (4, 3) → 10 ✓ → counterfactual: savings + 1.

## Common mistakes
* Changing immutable features.
* Returning any flipping point instead of the minimal one.
* Ignoring plausibility (bounds, realistic values).

## Why this matters
Counterfactuals are human-friendly, actionable explanations and relate to legal discussions of a
"right to explanation"; they also expose how close decisions are to the boundary.

## References

- [Interpretable Machine Learning (3rd edition)](https://christophm.github.io/interpretable-ml-book/) — Christoph Molnar (`S024`)
