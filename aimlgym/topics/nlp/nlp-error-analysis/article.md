# Evaluating Text Classifiers

## Learning outcomes

After this lesson you can:

- Report per-class precision, recall and F1 with classification_report
- Read a confusion matrix for several classes
- Collect misclassified examples for error analysis

## Intuition
One accuracy number hides where a model fails. With several classes, look at precision and recall
per class, at which classes are confused with which, and at the actual misclassified texts — they
usually reveal the fix (missing negations, sarcasm, a mislabelled training example, a new topic).

## Precise explanation
```python
from sklearn.metrics import classification_report, confusion_matrix
confusion_matrix(y_true, y_pred, labels=labels)      # rows: true class, columns: predicted
classification_report(y_true, y_pred, labels=labels, output_dict=True, zero_division=0)
```

* Row i, column j of the confusion matrix counts examples of class labels[i] predicted as labels[j];
  the diagonal is correct predictions.
* `output_dict=True` returns per-class dicts with `precision`, `recall`, `f1-score` and `support`,
  plus `"macro avg"` (unweighted mean over classes) and `"weighted avg"`.
* **Macro F1** treats every class equally — important when classes are imbalanced, since a model can
  reach high accuracy by ignoring a rare class.
* `zero_division=0` avoids warnings for classes that are never predicted.

## Worked example
For true [pos, pos, neg, neu] and predicted [pos, neg, neg, neg] with labels [neg, neu, pos]: the
confusion matrix is [[1, 0, 0], [1, 0, 0], [1, 0, 1]]; neutral has recall 0, and the errors are the
second and fourth texts.

## Common mistakes
* Reading the confusion matrix with rows and columns swapped.
* Reporting weighted averages only, which hide poor minority classes.
* Fixing errors by editing the test set rather than understanding them.

## Why this matters
Error analysis decides what to do next — more data for a class, new features, or relabelling — and
is a standard part of every model report.

## References

- [Metrics and scoring (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/model_evaluation.html) — scikit-learn developers (`S091`)
- [Text feature extraction (scikit-learn 1.9.1)](https://scikit-learn.org/stable/modules/feature_extraction.html) — scikit-learn developers (`S126`)
