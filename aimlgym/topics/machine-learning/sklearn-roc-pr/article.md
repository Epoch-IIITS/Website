# Thresholds, ROC and Precision–Recall Curves

## Learning outcomes

After this lesson you can:

- Summarise a classifier's scores with ROC AUC and average precision
- Read precision and recall at every threshold with precision_recall_curve
- Choose a decision threshold that meets a recall target

## Intuition
A classifier outputs a score; you turn it into "yes" when the score passes a **threshold**. A
lower threshold catches more positives (higher recall) but raises more false alarms (lower
precision). Curves show every threshold at once, and the right threshold depends on what a miss
costs compared with a false alarm.

## Precise explanation
* **ROC curve**: true-positive rate (recall) against false-positive rate as the threshold falls.
  `roc_auc_score(y, scores)` is the area under it: the probability that a random positive scores
  higher than a random negative (ties count half). 1.0 is perfect ranking; 0.5 is chance.
* **Precision–recall curve**: precision against recall. `average_precision_score` summarises it.
  On imbalanced data (1% fraud) PR is more informative: ROC AUC can look excellent while
  precision is poor.
* `precision_recall_curve(y, scores)` returns `precision, recall, thresholds`; `precision[i]` and
  `recall[i]` belong to predicting positive when `score >= thresholds[i]` (the arrays have one
  extra final point, precision 1 and recall 0, with no threshold).

```python
from sklearn.metrics import average_precision_score, precision_recall_curve, roc_auc_score
precision, recall, thresholds = precision_recall_curve(y, scores)
```

## Worked example
Scores [0.9, 0.8, 0.7, 0.6, 0.4, 0.2] for labels [1, 1, 0, 1, 0, 0]: thresholds 0.9, 0.8, 0.7, 0.6
give recall 1/3, 2/3, 2/3, 1 and precision 1, 1, 2/3, 3/4. To guarantee recall ≥ 0.9, the highest
usable threshold is 0.6, with precision 0.75. Eight of the nine positive–negative pairs are
ordered correctly, so ROC AUC = 8/9.

## What the library does inside
It sorts by score once and sweeps the threshold down, updating true- and false-positive counts —
the confusion-matrix counts from ML-06 at every cut.

## Common mistakes
* Always using 0.5 as the threshold, whatever the costs.
* Reporting only accuracy on imbalanced data.
* Passing predicted labels instead of scores or probabilities to `roc_auc_score`.
* Choosing the threshold on the test set and then reporting test precision as unbiased.

## Why this matters
Medical screening, fraud and spam filters all pick thresholds from these curves; the spam/fraud
project idea at the end of this topic is built around them.

## References

- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
- [User Guide (scikit-learn 1.9.1)](https://scikit-learn.org/stable/user_guide.html) — scikit-learn developers (`S012`)
