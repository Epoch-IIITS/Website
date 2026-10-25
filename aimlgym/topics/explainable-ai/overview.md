# Explainable AI

**You will be able to:** Explain models with contributions, decision paths, ICE curves, scikit-learn partial dependence and permutation importance, occlusion, surrogates, Shapley values, LIME, counterfactuals and integrated gradients.

**Topic prerequisites:** Computer Vision

Explaining predictions, from models that explain themselves (linear contributions, decision
paths) to model-agnostic methods — ICE curves, partial dependence and permutation importance with
`sklearn.inspection`, occlusion, global surrogates, exact Shapley values, LIME, counterfactuals —
and a gradient method for neural networks (integrated gradients). Every model being explained is
small and defined in the test, so each attribution can be checked.

**Packages:** `numpy`, `pandas` and `scikit-learn`. The NumPy partial dependence and permutation
importance are **optional deep dives**. **Project idea:** explain your house-price model.

## Learning path

Work through the steps in order; each one uses only what earlier steps (and the topic prerequisites) taught.

| Step | ID | Title | Difficulty | Builds on |
|---|---|---|---|---|
| 1 | XA-01 | [Linear Model Contributions](linear-contributions/problem.md) | beginner | ML-09 |
| 2 | XA-02 | [Ranking Attributions](top-k-attributions/problem.md) | beginner | XA-01 |
| 3 | XA-03 | [Tracing a Decision Path](decision-path/problem.md) | beginner | ML-21 |
| 4 | XA-04 | [Individual Conditional Expectation](ice-curve/problem.md) | beginner | XA-01 |
| 5 | XA-05 | [Partial Dependence with sklearn.inspection](xai-partial-dependence/problem.md) | intermediate | XA-04, ML-22 |
| 6 | XA-06 | [Partial Dependence by Hand (optional deep dive)](partial-dependence/problem.md) | intermediate | XA-04 |
| 7 | XA-07 | [Permutation Importance with sklearn.inspection](xai-permutation-importance/problem.md) | intermediate | XA-05 |
| 8 | XA-08 | [Permutation Feature Importance by Hand (optional deep dive)](permutation-importance/problem.md) | intermediate | XA-06, ML-02 |
| 9 | XA-09 | [Occlusion Saliency Map](occlusion-saliency/problem.md) | intermediate | CV-13, XA-04 |
| 10 | XA-10 | [Global Surrogate and Fidelity](surrogate-fidelity/problem.md) | intermediate | XA-07, ML-09 |
| 11 | XA-11 | [Exact Shapley Values](exact-shapley/problem.md) | advanced | MA-07, XA-01 |
| 12 | XA-12 | [LIME-style Local Linear Explanation](lime-local/problem.md) | advanced | XA-10, ML-19 |
| 13 | XA-13 | [Minimal Counterfactual Search](counterfactual-search/problem.md) | advanced | XA-03 |
| 14 | XA-14 | [Integrated Gradients](integrated-gradients/problem.md) | advanced | XA-11, DL-10 |
| 15 | XA-P1 | [Project idea: Explain Your House-Price Model](explain-house-prices/project.md) | ungraded | XA-05, XA-07, XA-11, XA-12, XA-13 |
