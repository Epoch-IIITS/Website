# Partial Dependence with sklearn.inspection

## Learning outcomes

After this lesson you can:

- Compute partial dependence and ICE curves with sklearn.inspection.partial_dependence
- Control the grid with grid_resolution and percentiles
- Read the average effect of one feature from the curve

## Intuition
An ICE curve (XA-04) shows how one prediction changes as one feature is varied. Averaging the
ICE curves over the dataset gives the **partial dependence**: the model's average response to that
feature, with the other features left as they are in the data.

## Precise explanation
```python
from sklearn.inspection import partial_dependence

result = partial_dependence(model, X, features=[0], grid_resolution=20, kind="average")
result["grid_values"][0]       # the feature values tried
result["average"][0]           # mean prediction at each grid value
partial_dependence(model, X, features=[0], kind="individual")["individual"][0]   # (n_samples, n_grid) ICE curves
```

* The grid spans the 5th to 95th percentile of the feature by default (`percentiles=(0.05, 0.95)`),
  so extreme outliers do not stretch it; `grid_resolution` caps the number of points (fewer if the
  feature has fewer unique values).
* `kind="both"` returns averages and individual curves together. For most models the average is the
  mean of the ICE curves ("brute" method); for tree ensembles `kind="average"` uses a faster
  "recursion" method that can differ slightly from averaging the individual curves.
* It works with any fitted estimator, including pipelines; for classifiers it uses predicted
  probabilities (or the decision function) of the positive class.
* For a linear model the partial dependence is a straight line whose slope is the coefficient (in the
  original units). Curved or step-shaped curves reveal non-linear effects.
* Partial dependence assumes the varied feature is not strongly correlated with the others — otherwise
  it averages over impossible combinations.

## Worked example
For y = 2x₀ + x₁² and a linear-regression pipeline, the partial dependence of feature 0 rises with
slope ≈ 2; for a random forest trained on the same data, the curve for feature 1 is U-shaped.

## What the library does inside
For every grid value it sets the feature to that value in a copy of `X`, predicts, and averages —
the procedure of XA-06 (the optional deep dive after this step), with a faster
recursion method for tree ensembles.

## Common mistakes
* Reading a flat average curve as "no effect" when ICE curves cancel out (some up, some down).
* Ignoring correlated features.
* Using the `"values"` key from old scikit-learn versions; it is now `"grid_values"`.

## Why this matters
Partial dependence plots are the standard global explanation for tabular models; the house-price
explanation project idea uses them.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
