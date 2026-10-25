# k-Nearest Neighbours with scikit-learn

## Learning outcomes

After this lesson you can:

- Fit KNeighborsClassifier inside a scaling pipeline
- Compare test accuracy across values of k
- Explain how k trades variance for bias

## Intuition
k-NN predicts the majority label among the k training points closest to a query. Small k follows
every quirk of the training data; large k smooths decisions until it predicts the majority
class everywhere. Distances mix features, so scaling matters.

## Precise explanation
```python
from sklearn.neighbors import KNeighborsClassifier
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
```

* `make_pipeline` names steps automatically (`"standardscaler"`, `"kneighborsclassifier"`).
* `n_neighbors` is k; `weights="distance"` lets closer neighbours count more; the default metric
  is Euclidean distance.
* `fit` just stores the (scaled) training data; the work happens in `predict`, which searches
  for neighbours with a tree or brute force.
* `accuracy_score(y_true, y_pred)` from `sklearn.metrics` is the share of correct predictions.

## Worked example
On two overlapping clusters, k = 1 might reach training accuracy 1.0 but test accuracy 0.80;
k = 7 might give 0.90 on test; k = n predicts the majority class and drops to the base rate.
Choosing k by the test score, as here, is acceptable for exploring — for a final choice, use
cross-validation (ML-16).

## What the library does inside
Your ML-13 (the optional deep dive after this step) computes all distances and takes
the k smallest; scikit-learn does the same with faster neighbour search structures.

## Common mistakes
* Forgetting to scale: one large-range feature dominates the distance.
* Even k for two classes, which allows ties.
* Picking k on the test set and then reporting that same test score as final.

## Why this matters
k-NN is a strong baseline for small datasets and the idea behind nearest-neighbour search used by
retrieval systems later in the course.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
