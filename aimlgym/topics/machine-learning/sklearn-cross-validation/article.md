# Cross-Validation with scikit-learn

## Learning outcomes

After this lesson you can:

- Estimate performance with cross_val_score and a shuffled KFold
- Use StratifiedKFold for classification
- Report the mean and spread of fold scores

## Intuition
One train/test split gives one noisy number. k-fold cross-validation splits the data into k
folds, trains on k − 1 of them and tests on the remaining one, k times. Every row is tested once,
and the spread of the k scores tells you how much to trust the mean.

## Precise explanation
```python
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score

cv = KFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(model, X, y, cv=cv)          # one score per fold
scores.mean(), scores.std()
```

* `cross_val_score` clones the model for each fold, so the model you pass is never fitted.
* `KFold(shuffle=True, random_state=...)` shuffles once before cutting folds; without `shuffle`
  the folds follow the row order, which is wrong for sorted data.
* `StratifiedKFold` keeps the class ratio in every fold — the right default for classification.
* `scoring` chooses the metric (`"accuracy"`, `"r2"`, `"neg_mean_squared_error"`, …); by default
  it is the estimator's own `score`.

## Worked example
Five fold accuracies [0.90, 0.85, 0.95, 0.80, 0.90] give 0.88 ± 0.05. A rival model at 0.89 ±
0.06 is not clearly better: the difference is smaller than the fold-to-fold spread.

## What the library does inside
The fold loop is the one you write in ML-17 (the optional deep dive after this step):
split the indices, fit a fresh model, score, repeat.

## Common mistakes
* Preprocessing (scaling, imputing) before cross-validation instead of inside a pipeline.
* Reporting the best fold instead of the mean.
* Comparing models on different fold splits; fix `random_state` so they see the same folds.

## Why this matters
Hyperparameter search (ML-19) runs exactly this loop for every candidate
setting, and the capstone reports a cross-validated score next to the final test score.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
