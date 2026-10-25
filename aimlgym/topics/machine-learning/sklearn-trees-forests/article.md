# Decision Trees and Random Forests

## Learning outcomes

After this lesson you can:

- Train a DecisionTreeClassifier and limit its depth
- Train a RandomForestClassifier and read feature_importances_
- Explain why averaging many randomised trees reduces variance

## Intuition
Your decision stump (ML-21) asked one question. A **decision tree** keeps
asking: split, then split each side, until the leaves are pure or a depth limit stops it. A deep
tree memorises the training set. A **random forest** trains many trees, each on a bootstrap
sample with random subsets of features at each split, and lets them vote: the individual errors
partly cancel.

## Precise explanation
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train)
tree.get_depth(), tree.get_n_leaves()
forest = RandomForestClassifier(n_estimators=200, random_state=0).fit(X_train, y_train)
forest.feature_importances_        # one value per feature, summing to 1
```

* Trees need **no scaling**: a split compares one feature with a threshold.
* `max_depth`, `min_samples_leaf` and `max_features` limit complexity; with no limits, a tree
  reaches 100% training accuracy whenever no two identical rows disagree.
* `feature_importances_` is the total impurity decrease contributed by each feature, averaged
  over trees and normalised to sum to 1. It is biased towards features with many split points;
  XA-08 (later) is a more reliable check.
* `random_state` fixes the bootstrap samples and feature choices, making results reproducible.

## Worked example
On data where only feature 0 matters plus label noise, an unlimited tree scores 1.00 on training
and about 0.80 on test; a 200-tree forest scores about 0.90 on test, and feature 0 receives most of
the importance.

## What the library does inside
Each split chooses the feature and threshold with the lowest weighted Gini impurity — your stump's
search, applied recursively. The forest repeats that on bootstrap samples, like ST-13
resamples data, and averages the trees' class probabilities.

## Common mistakes
* Judging a deep tree by its training accuracy.
* Treating impurity-based importances as causal effects.
* Comparing a tree and a forest trained with different random states or data.

## Why this matters
Forests and boosted trees (ML-23) are the strongest general-purpose models
for tabular data, and the usual baseline before trying neural networks.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Getting Started (scikit-learn 1.9.1)](https://scikit-learn.org/stable/getting_started.html) — scikit-learn developers (`S089`)
