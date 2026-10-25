# Gradient Boosting

## Learning outcomes

After this lesson you can:

- Train HistGradientBoostingClassifier and explain how boosting adds trees
- Track validation log-loss as trees are added
- Choose the number of boosting iterations from a validation curve

## Intuition
A forest grows trees independently and averages them. **Boosting** grows them one after another:
each new small tree is trained to correct the mistakes of the ensemble so far, and its vote is
scaled down by a learning rate. Early trees fix big errors; later ones fine-tune — and eventually
start fitting noise.

## Precise explanation
For classification, the model keeps a score F(x) whose sigmoid is P(y = 1). Each iteration fits
a regression tree to the **gradient of the log-loss** (how much each prediction should move) and
adds `learning_rate × tree` to F. That is gradient descent (ML-10) where
each step is a tree.

```python
from sklearn.ensemble import HistGradientBoostingClassifier

model = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1,
                                       early_stopping=False, random_state=0).fit(X, y)
for proba in model.staged_predict_proba(X_val):   # after 1 tree, 2 trees, ...
    ...
```

* "Hist" means features are bucketed into at most 255 bins first, which makes training fast and
  lets the model handle missing values natively.
* `max_iter` is the number of trees; `learning_rate` trades speed for smoothness; `max_depth`
  or `max_leaf_nodes` keep each tree small.
* `early_stopping=True` holds out part of the training data and stops when the validation loss
  stops improving; here we switch it off to see the whole curve.
* `log_loss(y_true, proba)` from `sklearn.metrics` measures probabilistic predictions; lower is better.

## Worked example
With learning rate 0.3 on noisy data, validation log-loss might fall from 0.62 after one tree to
0.35 after 20, then creep back up to 0.40 by 200 trees while training loss keeps falling. The best
number of iterations is near 20.

## What the library does inside
Each tree is grown greedily like the trees in ML-22, but on the binned features
and against gradients rather than class labels.

## Common mistakes
* A large learning rate with many trees: fast overfitting.
* Choosing `max_iter` by the test score; use a separate validation set or early stopping.
* Expecting identical results across library versions; compare trends, not exact numbers.

## Why this matters
Gradient-boosted trees win most tabular competitions and power many production systems in
ranking, fraud detection and forecasting.

## References

- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
