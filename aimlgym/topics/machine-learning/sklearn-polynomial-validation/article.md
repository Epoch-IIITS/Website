# Polynomial Features and Validation Curves

## Learning outcomes

After this lesson you can:

- Build polynomial models with PolynomialFeatures in a pipeline
- Compute training and validation error for each degree with validation_curve
- Recognise underfitting and overfitting in a validation curve

## Intuition
A straight line cannot follow a curve (underfitting); a degree-15 polynomial follows every noisy
point (overfitting). Plot error against model complexity for both the data the model trained on
and data it did not: training error keeps falling, validation error falls and then rises. The
bottom of the validation curve is the complexity to choose.

## Precise explanation
```python
from sklearn.model_selection import KFold, validation_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

model = make_pipeline(PolynomialFeatures(include_bias=False), LinearRegression())
train, val = validation_curve(model, X, y, param_name="polynomialfeatures__degree",
                              param_range=[1, 2, 3], cv=KFold(5, shuffle=True, random_state=0),
                              scoring="neg_mean_squared_error")
```

* `PolynomialFeatures(degree=d)` turns a column x into x, x², …, xᵈ; `include_bias=False` leaves
  the constant to the linear model's intercept.
* In a pipeline, a step's parameter is addressed as `<step name>__<parameter>`.
* `validation_curve` returns arrays of shape `(len(param_range), n_folds)`: one score per
  setting and fold, for the training folds and the held-out fold.
* scikit-learn always **maximises** scores, so errors appear negated (`neg_mean_squared_error`);
  multiply by −1 to get MSE.

## Worked example
For y = x² plus noise: degree 1 has high error on both curves (underfit); degree 2 has the lowest
validation error; degrees 8–10 have tiny training error but larger validation error (overfit).

## What the library does inside
It repeats the experiment of ML-15 (the optional deep dive after this step)
for every degree on every fold, refitting a clone of the pipeline each time.

## Common mistakes
* Forgetting to negate `neg_mean_squared_error` and picking the *largest* error.
* Passing `param_name="degree"` instead of `"polynomialfeatures__degree"`.
* Using an unshuffled `KFold` on data sorted by x: each fold extrapolates.

## Why this matters
Validation curves are the standard picture for any complexity knob — tree depth, k in k-NN,
regularisation strength — and they motivate the cross-validation and search tools next.

## References

- [Underfitting vs. Overfitting (scikit-learn example)](https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html) — scikit-learn developers (`S090`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
