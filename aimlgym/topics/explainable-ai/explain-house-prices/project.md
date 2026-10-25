# XA-P1 · Project idea: Explain Your House-Price Model

**Topic:** Explainable AI · ungraded

## Brief

Write an explanation report for the house-price model from the Machine Learning project: which
features matter, how each one moves the price, why one particular house got its estimate, and where
the explanations disagree.

## You will use

- XA-05 Partial Dependence with sklearn.inspection
- XA-07 Permutation Importance with sklearn.inspection
- XA-11 Exact Shapley Values
- XA-12 LIME-style Local Linear Explanation
- XA-13 Minimal Counterfactual Search

## Milestones

1. Load your trained pipeline and a held-out test set.
2. Rank features with permutation importance (mean ± std) and plot the top ten.
3. Plot partial dependence and ICE curves for the three most important features.
4. Explain five individual predictions with SHAP values and compare them with LIME-style local fits.
5. Write a one-page report: findings, surprising effects, and the limits of each method.

## Stretch goals

- Find counterfactuals: the smallest change that moves a house into a different price band.
- Check whether correlated features (rooms and area) split their importance.
- Build a small web page that shows the explanation for any house id.

## Data

Use the house-price project's data (California housing or Ames). The [SHAP library](https://shap.readthedocs.io/en/latest/)
computes Shapley values efficiently for tree models; it is not part of the graded course because it
needs compiled dependencies.

## Run it yourself

```bash
pip install scikit-learn pandas matplotlib shap
python explain.py
```
