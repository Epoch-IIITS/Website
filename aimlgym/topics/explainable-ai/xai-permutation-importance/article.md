# Permutation Importance with sklearn.inspection

## Learning outcomes

After this lesson you can:

- Measure feature importance with permutation_importance on held-out data
- Apply it to a whole pipeline so importances refer to the original columns
- Report the mean and spread over repeats

## Intuition
How much does a model rely on a feature? Shuffle that feature's column — breaking its link with the
target while keeping its distribution — and see how much the score drops. A big drop means the model
needed the feature; no drop means it did not.

## Precise explanation
```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=0, scoring="r2")
result.importances_mean        # mean score drop per feature
result.importances_std         # spread over the repeats
```

* Compute it on **held-out** data: on training data an overfitted model looks dependent on noise.
* Passing the **pipeline** (preprocessing + model) and a DataFrame gives importances for the original
  columns, even when a ColumnTransformer expands categories into many encoded columns.
* `n_repeats` shuffles each column several times; report mean ± standard deviation. Importances near
  zero (or slightly negative) mean "not used".
* Correlated features share importance: shuffling one leaves the other to carry the information, so
  both can look unimportant.
* Unlike tree `feature_importances_`, it works for any model and any scorer.

## Worked example
For y = 3·x₀ + 0.5·x₁ + noise, with x₂ pure noise, the importances on a test set are roughly
x₀ ≫ x₁ > 0 ≈ x₂.

## What the library does inside
For each feature and repeat it permutes the column with a seeded generator, re-scores the model and
subtracts from the baseline score — the loop of XA-08 (the optional deep dive
after this step).

## Common mistakes
* Computing importances on the training set.
* Reading importance as causal effect or as the direction of the effect (use partial dependence).
* Dropping two correlated features because each looked unimportant alone.

## Why this matters
Permutation importance is the standard model-agnostic check of what a model relies on; it often
exposes leakage features that are "too important".

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
