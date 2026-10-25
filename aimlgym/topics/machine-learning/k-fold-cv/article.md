# k-Fold Cross-Validation

## Learning outcomes

After this lesson you can:

- Create k disjoint folds
- Train/evaluate k times and aggregate
- Use CV to choose a hyperparameter

## Intuition
One train/test split gives one noisy estimate. Cross-validation rotates: split the data into k
folds, train on k − 1 of them and test on the remaining one, k times. Every example is tested
exactly once.

## Precise explanation
* Shuffle indices (if seeded) and split them into k nearly equal folds: the first `n % k` folds
  get one extra element (same convention as `np.array_split`).
* For fold i: test = fold i, train = all others.
* Report the mean (and spread) of the k scores.
* Use CV on the **training** data to pick hyperparameters (k in k-NN, λ in ridge); keep the test
  set for the final estimate.

| fold | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| round 1 | test | train | train | train | train |
| round 2 | train | test | train | train | train |
| … | | | | | |

## Worked example
n = 7, k = 3 → fold sizes 3, 2, 2: [0,1,2], [3,4], [5,6] (without shuffling).

## Common mistakes
* Overlapping folds or leaving examples out.
* Preprocessing (scaling) on all data before CV — fit inside each training fold.
* Using CV scores of the tuned model as the final unbiased estimate.

## Why this matters
CV is the standard way to compare models and tune hyperparameters on small datasets.

## Library implementation

`sklearn.model_selection.KFold(n_splits=k)` (no shuffling) produces exactly the folds of
`np.array_split`: consecutive blocks, the first `n % k` folds one element larger.
`cross_val_score(estimator, X, y, cv=KFold(...))` runs the fit–score loop for you.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
