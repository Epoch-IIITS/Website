# Regularisation and Hyperparameter Search

## Learning outcomes

After this lesson you can:

- Regularise a linear model with Ridge and explain how alpha shrinks coefficients
- Search hyperparameters with GridSearchCV over a pipeline
- Read best_params_, best_score_ and cv_results_

## Intuition
A linear model with many features can fit noise with large, wobbly coefficients.
**Regularisation** adds a penalty for large coefficients: Ridge minimises
squared error + α·‖w‖². Larger α means smaller coefficients and a simpler model. Which α is best
is a question for cross-validation — and `GridSearchCV` asks it for every candidate.

## Precise explanation
```python
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, KFold

pipe = make_pipeline(StandardScaler(), Ridge())
search = GridSearchCV(pipe, {"ridge__alpha": [0.01, 0.1, 1, 10, 100]},
                      cv=KFold(5, shuffle=True, random_state=0), scoring="neg_mean_squared_error")
search.fit(X, y)
search.best_params_          # {'ridge__alpha': 1}
-search.best_score_          # mean validation MSE of the best setting
search.best_estimator_       # the pipeline refitted on ALL of X, y with the best alpha
search.cv_results_["mean_test_score"]   # one entry per candidate, in grid order
```

* Scale features before Ridge: the penalty treats all coefficients alike, so units matter.
* The classifier counterpart is `LogisticRegression(C=...)`, where **C = 1/α**: smaller C means
  *stronger* regularisation.
* Grids are usually logarithmic (0.01, 0.1, 1, 10, …) because the effect of α is multiplicative.
* `refit=True` (the default) retrains the best setting on all the data you passed.

## Worked example
With 30 features (only 3 useful) and 40 rows, α = 0.01 nearly reproduces least squares and overfits, α = 100
shrinks everything towards zero and underfits; a middle value such as α = 1–10 has the lowest
cross-validated MSE. The coefficient norm ‖w‖ falls steadily as α grows.

## What the library does inside
`Ridge` solves (XᵀX + αI)w = Xᵀy — the closed form in ML-20, the optional deep dive
after this step. `GridSearchCV` is a loop of ML-16 over every candidate.

## Common mistakes
* Searching on the test set, or reporting `best_score_` as the final test score.
* Forgetting the `<step>__` prefix in the grid keys.
* Reading a larger C as more regularisation in `LogisticRegression` (it is less).

## Why this matters
Almost every model has knobs. Searching them with cross-validation inside a pipeline is the
standard, leak-free way to choose them.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
